import os
from datetime import datetime
from urllib.parse import urlencode

import requests
from celery import shared_task
from django_celery_results.models import TaskResult

from collectors.models import Source, StorageInstance
from collectors.storage import GoogleCloudStorage, AzureBlobStorage


def _remove_expired_task_history():
    TaskResult.objects.delete_expired(expires=24 * 60 * 60)  # 24 hours


def _inject_key(string, source):
    return string.replace(f"[{source.access_key.key}]", source.access_key.value)


def _get_default_storage():
    instance = StorageInstance.objects.get(default=True)

    mapping = {
        StorageInstance.Provider.GOOGLE: GoogleCloudStorage,
        StorageInstance.Provider.AZURE: AzureBlobStorage,
    }

    return mapping[instance.provider](instance.credentials, instance.container_name)


@shared_task
def collect(source_id: int):
    source = Source.objects.get(pk=source_id)

    METHOD_MAP = {
        Source.Method.GET: requests.get,
        Source.Method.POST: requests.post,
        Source.Method.PUT: requests.put,
        Source.Method.PATCH: requests.patch,
        Source.Method.DELETE: requests.delete,
    }

    method = METHOD_MAP[source.method]

    # combine url with query parameters
    complete_url = source.url
    headers = source.headers or {}

    if source.query_params:
        complete_url += "?" + urlencode(source.query_params)

    if source.access_key:
        complete_url = _inject_key(complete_url, source)

        for header in headers:
            headers[header] = _inject_key(headers[header], source)

    response = method(
        complete_url,
        headers=headers,
        data=source.body,
    )

    content_type = response.headers.get("content-type") or "application/json"

    storage = _get_default_storage()

    file_name = f"{datetime.now().isoformat()}.{source.extension}"

    storage.save(
        response.content,
        str(os.path.join(source.group.storage_slug, source.storage_slug, file_name)),
        content_type,
    )

    # Clean up
    _remove_expired_task_history()
