# -*- coding: utf-8 -*-
from nltk.tokenize import MWETokenizer
from . import filesystem
import os

class WordOps(object):

    turkish_pattern = []
    fs = filesystem.FileSystemOps()
    def __init__(self, db="default_db"):
        self.turkish_pattern = self.fs.read_json_from_file(os.path.dirname(__file__) + '/nltk/patterns.json')
   

    def string_tokenize(self, string):
        tokenizer = MWETokenizer([pattern.split() for pattern in self.turkish_pattern], separator=' ')
        return tokenizer.tokenize(string.split())
       