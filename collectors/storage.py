import abc
import json

from azure.storage.blob import BlobServiceClient
from google.cloud import storage
from google.oauth2 import service_account


class Storage(abc.ABC):
    @abc.abstractmethod
    def save(self, data: bytes, path: str, content_type: str):
        pass


class AzureBlobStorage(Storage):
    def __init__(self, credentials: str, container_name: str):

        self.blob_service_client = BlobServiceClient.from_connection_string(credentials)
        self.container_name = container_name

    def save(self, data: bytes, path: str, content_type: str):
        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name, blob=path
        )
        blob_client.upload_blob(data, content_settings={"content_type": content_type})


class GoogleCloudStorage(Storage):
    def __init__(self, credentials: str, container_name: str):
        # Load the credentials from the JSON string
        credentials_info = json.loads(credentials)
        self.credentials = service_account.Credentials.from_service_account_info(
            credentials_info
        )

        # Create the storage client using the credentials
        self.client = storage.Client(credentials=self.credentials)
        self.bucket = self.client.get_bucket(container_name)

    def save(self, data: bytes, path: str, content_type: str):
        blob = self.bucket.blob(path)
        blob.upload_from_string(data, content_type=content_type)
