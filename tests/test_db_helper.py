import pytest
import json
from .. import DBHelper

class TestDBHelper:

    def test_insert(self, pg_client):
        pg_client.insert("INSERT INTO test (field) values (%s)", ("test_char",))
        from_db = pg_client.fetch("SELECT field FROM test")
        assert from_db[0].get("field") == "test_char"
        
    def test_fetch(self, pg_client):
        pg_client.insert("INSERT INTO test (field) values (%s)", ("test_char",))
        from_db = pg_client.fetch("SELECT field FROM test")
        assert from_db[0].get("field") == "test_char"

    def test_query(self, pg_client):
        pass