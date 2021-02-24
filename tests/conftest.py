import pytest
from .. import RedisHelper
from .. import DBHelper


@pytest.fixture
def redis_client():
    # TODO: test kuyruğu sıfırlanacak.
    return RedisHelper()

@pytest.fixture
def pg_client():
    pg_client = DBHelper()
    pg_client.query("CREATE TABLE test (field VARCHAR ( 50 ) NOT NULL)")
    yield pg_client
    pg_client.query("DROP TABLE IF EXISTS test")


