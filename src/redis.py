import redis
import os
from typing import Text, List


class RedisHelper(object):

    def __init__(self) -> None:
        self.client = redis.StrictRedis(
                            host=os.getenv("REDIS_HOST"), 
                            password=os.getenv("REDIS_PASSWORD"), 
                            encoding="utf-8", 
                            decode_responses=True)
    
    def create_pipeline(self) -> redis.StrictRedis.pipeline:
        """Create a pipeline using for multiple commands in single request."""
        return self.client.pipeline()
    
    def count(self, key_name: Text):
        """Get item count in list"""
        return self.client.scard(key_name)

    def get(self, key_name: Text, count: int = 1) -> str:
        """Popping random element from list"""
        return self.client.spop(key_name, count=count)

    def put(self, key_name: Text, item: str) -> None:
        """Putting element to list"""
        self.client.sadd(key_name, item)
    
    def put_many(self, key_name: Text, items: List[str]) -> None:
        """Put many items to the list"""
        with self.create_pipeline() as pipe:
            for item in items:
                pipe.sadd(key_name, item)
            pipe.execute()

    def rpush(self, key_name: Text, item: str) -> Text:
        """Pushing element to the right side of the list."""
        return self.client.rpush(key_name, item)
    
    def lpush(self, key_name: Text, item: str) -> Text:
        """Pushing element to the right side of the list."""
        return self.client.lpush(key_name, item)

    def rpop(self, key_name: Text) -> Text:
        """Popping element from the left side of the list."""
        return self.client.rpop(key_name)

    def lpop(self, key_name: Text) -> Text:
        """Popping element from the left side of the list."""
        return self.client.lpop(key_name)
    
    def lcount(self, key_name: Text) -> Text:
        return self.client.llen(key_name)
    
    def search_keys(self,  search_expression) -> List:
        """Search keys with search expression"""
        return self.client.keys(search_expression)

    def get_key_memory_usage(self, key_name: Text) -> Text:
        """Get memory usage of lists."""
        return self.client.memory_usage(key_name)

        



"""
class RedisOps(object):
    def set_expire(self, key, second):
        self.db.expire(key, second);
"""