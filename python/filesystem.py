# -*- coding: utf-8 -*-
import os, sys, json
import os.path
import wget 
import zipfile

class FileSystemOps(object):
    def __init__(self):
        with open(os.path.dirname(__file__) + '/../config.json','r') as my_file:
            self.config = json.load(my_file)
    
    def read_json_from_file(self, file_name):
        with open(file_name,'r') as my_file:
            return json.load(my_file)
    
    def read_text_from_file(self, file_name):
        with open(file_name,'r') as my_file:
            return my_file.read()

    def write_json_to_file(self, file_name, package):
        with open(file_name,'a') as my_file:
            return json.dump(package, my_file)
    
    def write_text_to_file(self, file_name, string):
        with open(file_name,'a') as my_file:
            return my_file.write(string+"\n")
    
    def delete_file(self, file_name):
        os.remove(file_name)
    
    def download_file(self, file_url):
        try:
            return wget.download(file_url)
        except:
            return None
    
    def unzip_file(self, file_name, target="./"):
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall(target)