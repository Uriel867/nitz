from pymongo import MongoClient


def provide_mongo_client():
    mongo_client = MongoClient()
    
    yield mongo_client