__name__ = 'BlobOps Class'
__doc__ = 'BlobOps Operations'
__version__ = 'v1.0'
# Standart Libray
import json
from . import filesystem
import time, os
from azure.storage.blob import (
    BlockBlobService,
    ContainerPermissions,
)


class BlobOps(object):
    fs = filesystem.FileSystemOps()
    def __init__(self, **kwargs):
        self.config = self.fs.read_json_from_file(os.path.dirname(__file__) + '/../config.json')
        print(':::::Blob Operations::::')
        self.blob = BlockBlobService(account_name=self.config["azure"]["storage_account"], account_key=self.config["azure"]["storage_account_key"]) 
    
    def create_container(self, container_name):
        self.blob.create_container(container_name) 
        self.blob.set_container_acl(container_name, public_access=ContainerPermissions.READ)

    def upload_file(self, container_name, file_name, full_path):
        self.blob.create_blob_from_path(container_name, file_name, full_path)

    
    def container_file_list(self, container_name):
        generator = self.blob.list_blobs(container_name)
        return generator
    
    def download_file(self, container_name, file_name, full_path):
        self.blob.get_blob_to_path(container_name, file_name, full_path)

    def delete_container(self, container_name):
        self.blob.delete_container(container_name)

    def delete_file(self, container_name, blob_name):
        self.blob.delete_blob(container_name, blob_name)

