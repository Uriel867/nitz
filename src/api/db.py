from pymongo import MongoClient

_client = MongoClient("mongodb://localhost:27017/")
_db = _client["lol"]
summoners_collection = _db["summoners"]
match_id_collection = _db["match_id"]
match_data_collection = _db["match_data"]
