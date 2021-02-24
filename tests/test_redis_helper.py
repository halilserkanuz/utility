import pytest
import json
from .. import RedisHelper

class TestRedisHelper:

    @pytest.fixture
    def item(self):
        with open('./utility/tests/fixtures/item.json', 'r') as f:
            return json.dumps(json.loads(f.read()))
    
    def test_get(self, redis_client: RedisHelper, item: str):
        redis_client.put('test-key', item)
        assert item == redis_client.get('test-key')

    def test_put(self, redis_client: RedisHelper, item: str):
        redis_client.put('test-key', item)
        assert item == redis_client.get('test-key')

    def test_rpush(self, redis_client: RedisHelper, item: str):
        redis_client.rpush('test-key', item)
        assert item == redis_client.lpop('test-key')

    def test_lpop(self, redis_client: RedisHelper, item: str):
        redis_client.rpush('test-key', item)
        assert item == redis_client.lpop('test-key')

    def test_search_keys(self, redis_client: RedisHelper, item: str):
        redis_client.put('test-key', item)
        search_result = redis_client.search_keys('test*')
        assert 'test-key' in search_result

    def test_search_keys(self, redis_client: RedisHelper, item: str):
        redis_client.put('test-key', item)
        memory_usage = redis_client.get_key_memory_usage('test*')
        assert memory_usage != 0
    

