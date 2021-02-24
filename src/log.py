import glob
from typing import Text, List
from logging.config import fileConfig
import logging

class LogHelper:
    

    def get_logger(self) -> logging.Logger:
        fileConfig('logger_conf.ini')
        return logging.getLogger()

    def cleanup(self):
        """Cleanup processes for log"""
        files = self.get_files("*.log")
        for file in files:
            print(file)

    def upload(self):
        """Upload file to cloud"""

    def remove_file(self):
        """Remove file from storage."""

    def get_files(self, search_pattern: Text) -> List[Text]:
        return glob.glob(search_pattern)
