__name__ = 'RedisOps Class'
__doc__ = 'Redis Operations'
__version__ = 'v1.0'
# Standart Libray
from . import filesystem
import json, redis, time, os


class RedisOps(object):
    fs = filesystem.FileSystemOps()
    """Simple Queue with Redis Backend"""
    def __init__(self, **redis_kwargs):
        self.config = self.fs.read_json_from_file(os.path.dirname(__file__) + '/../config.json')
        host = redis_kwargs.get("host", self.config["redis"]["host"])
        password = redis_kwargs.get("password", self.config["redis"]["password"])
        self.db = redis.StrictRedis(host=host, password=password, charset="utf-8", decode_responses=True)
        self.pipe = self.db.pipeline()

    def count(self, name):
        """Get item count in queue"""
        return self.db.scard(name)
    
    def get_key_list(self,  name):
        """Get keys with search name"""
        return self.db.keys(name)

    def get_key_list_like(self,  name):
        """Get keys with search name"""
        return self.db.keys(name+"*")

    def put_many(self, name, items):
        """Put many item into the queue."""
        print('Items adding to queue')
        if len(items)>0:
            for item in items:
                if item:
                    self.pipe.sadd(name, item)
            self.pipe.execute()
            print('adding items to queue finished')
        else:
            print('List to be loaded is empty')
    

    def put(self, name, item):
        self.db.sadd(name, item)

    def get_many(self, name, count=0):
        items = self.db.spop(name, count=count)
        
        return items

    def get(self, name):
        result = self.db.spop(name)
        
        return result

    def get_oldest_key_like(self, name):
        key_list = self.get_key_list_like(name)
        key_list = [key for key in key_list]
        key_list.sort()
        return key_list[0]
    
    def get_key_memory_usage(self, name):
        return self.db.memory_usage(name)
    