from . import filesystem
import random, os

class ArrayOps(object):


    def __init__(self):
        pass
        
    def split_array(self, array, size):
        return [array[offs:offs+size] for offs in range(0, len(array), size)]

class CrawlerOps(object):

    fso = filesystem.FileSystemOps()
    def __init__(self):
        self.config = self.fso.read_json_from_file(os.path.dirname(__file__) + '/../config.json')
    def get_random_useragent(self):
        return random.choice(self.config["useragents"])

