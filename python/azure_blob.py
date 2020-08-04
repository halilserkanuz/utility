__name__ = 'BlobOps Class'
__doc__ = 'BlobOps Operations'
__version__ = 'v1.0'
# Standart Libray
import json
from . import filesystem
import time, os
from azure.storage.blob import BlobServiceClient


class BlobOps(object):
    fs = filesystem.FileSystemOps()
    def __init__(self, storage_account="trackstorage", **kwargs):
        self.config = self.fs.read_json_from_file(os.path.dirname(__file__) + '/../config.json')
        print(self.config)
        self.blob_service = BlobServiceClient.from_connection_string(self.config[storage_account]["connection_string"])
    
    def create_container(self, container_name):
        self.blob_service.create_container(container_name)


    def upload_file(self, container_name, file_name, full_path):
        blob_client = self.blob_service.get_blob_client(container=container_name, blob=file_name)
        with open(full_path, "rb") as data:
            blob_client.upload_blob(data)
    
    def container_file_list(self, container_name):
        container = self.blob_service.get_container_client(container=container_name)
        generator = container.list_blobs()
        return generator
    
    def download_file(self, container_name, file_name, full_path):
        blob_client = self.blob_service.get_blob_client(container=container_name, blob=file_name)
        with open(full_path, "wb") as f:
            f.writelines([blob_client.download_blob().readall()])

    def delete_container(self, container_name):
        self.blob_service.delete_container(container_name)

    def delete_file(self, container_name, blob_name):
        blob_client = self.blob_service.get_blob_client(container=container_name, blob=blob_name)
        blob_client.delete_blob()

