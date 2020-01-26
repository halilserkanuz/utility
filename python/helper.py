from . import filesystem
import random, os,json

class ArrayOps(object):


    def __init__(self):
        pass
        
    def split_array(self, array, size):
        return [array[offs:offs+size] for offs in range(0, len(array), size)]
    
class JsonOps(object):

    def __init__(self):
        pass

    def clean_item(self, item):
        if isinstance(item, str):
            item=item.replace('\n','').replace('\t','').replace('\r','').replace('\'','').replace('\'','').replace('"','').replace('"','').replace('\u011f','ğ')\
                .replace('\u011e','Ğ').replace('\u0131','ı').replace('\u0130','i').replace('\u00f6','ö').replace('\u00d6','Ö')\
                .replace('\u00fc','ü').replace('\u00dc','Ü').replace('\u015f','ş').replace('\u015e','Ş').replace('\u00e7','ç').replace('\u00c7','Ç').replace("'","")
        elif isinstance(item, dict):
            for key, value in item.items():
                item[key]=self.clean_item(value)
        elif isinstance(item, list):
            arr = []
            for i in item:
                arr.append(self.clean_item(i))
            item=arr
        return item

class CrawlerOps(object):

    fso = filesystem.FileSystemOps()
    def __init__(self):
        self.config = self.fso.read_json_from_file(os.path.dirname(__file__) + '/../config.json')
    def get_random_useragent(self):
        return random.choice(self.config["useragents"])

