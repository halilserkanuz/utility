__name__ = 'RedisOps Class'
__doc__ = 'Redis Operations'
__version__ = 'v1.0'
# Standart Libray
import json
import redis
import time


class RedisQueue(object):
    """Simple Queue with Redis Backend"""
    def __init__(self, **redis_kwargs):
        self.config = self.fs.read_json_from_file(os.path.dirname(__file__) + '/../config.json')
        host = redis_kwargs.get("host", config["redis"]["host"])
        password = redis_kwargs.get("password", config["redis"]["password"])
        self.db = redis.Redis(host=host, password=password)
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
        for item in items:
            self.pipe.sadd(name, json.dumps(item))
        self.pipe.execute()
        print('adding items to queue finished')
    

    def put(self, name, item):
        self.db.sadd(name, item)

    def get_many(self, name, count=0):
        items = self.db.spop(name, count=count)
        items = [item.decode('utf-8') for item in items]
        return items

    def get(self, name):
        return self.db.spop(name)

    def get_oldest_key_like(self, name):
        key_list = self.get_key_list_like(name)
        key_list = [key.decode('utf-8') for key in key_list]
        key_list.sort()
        return key_list[0]
    
    