from pymongo import MongoClient

_client = MongoClient("mongodb://localhost:27017/")
_db = _client["testdb"]
collection = _db["summoners"]