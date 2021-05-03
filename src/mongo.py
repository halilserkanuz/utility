from pymongo import MongoClient
import os



class MongoHelper(object):

    def __init__(self, db_name="datapare"):
        self.db_name = db_name

    def create_client(self):
        client = MongoClient('mongodb://{0}:{1}@{2}'.format(os.getenv("MONGO_USER"), os.getenv("MONGO_PASSWORD"), os.getenv("MONGO_HOST")))
        return client[self.db_name]

    def insert(self, collection: str, data: dict) -> None:
        db = self.create_client()
        _collection = db[collection]
        _collection.insert(data, check_keys=False)

    def query(self,  collection: str, data: dict) -> None:
        db = self.create_client()
        _collection = db[collection]
        return _collection.find(data)