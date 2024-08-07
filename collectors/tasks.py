import json
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
    headers = source.source_headers.headers if source.source_headers else {}

    if source.query_params:
        complete_url += "?" + urlencode(source.query_params)

    if source.access_key:
        complete_url = _inject_key(complete_url, source)

        for header in headers:
            headers[header] = _inject_key(headers[header], source)

    if source.paginated:
        data = []
        total_count = 0
        content_type = "application/json"

        if "?" not in complete_url:
            complete_url += "?"
        else:
            complete_url += "&"

        # Not while True to avoid infinite loop
        for _ in range(100):
            response = method(
                complete_url
                + f"limit={source.pagination_limit}&{source.pagination_offset_key}={len(data)}",
                headers=headers,
            )

            if response.status_code != 200:
                response.raise_for_status()

            total_count = response.json().get(
                source.pagination_total_count, total_count
            )
            data.extend(response.json().get(source.pagination_result_key, []))

            if len(data) >= total_count:
                break

        content = json.dumps(data).encode("utf-8")
    else:
        response = method(complete_url, headers=headers)
        content_type = response.headers.get("content-type") or "application/json"
        content = response

    storage = _get_default_storage()

    file_name = f"{datetime.now().isoformat()}.{source.extension}"

    storage.save(
        content,
        str(os.path.join(source.group.storage_slug, source.storage_slug, file_name)),
        content_type,
    )

    # Clean up
    _remove_expired_task_history()
