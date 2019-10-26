from . import filesystem as fs
from datetime import datetime


class LogOps(object):
    def __init__(self):
        self.fso = fs.FileSystemOps()

    def write_log_with_timestamp(self, file_name, string):
        timestamp = datetime.utcnow().strftime("%d/%m/%Y, %H:%M:%S")
        self.fso.write_text_to_file(file_name, timestamp+"\t"+string)