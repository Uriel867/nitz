from typing import Dict
from pymongo import MongoClient

class LoLStatsService:
    
    def __init__(self, mongo_client: MongoClient):
        self.mongo_client = mongo_client
        self.db = mongo_client.lol
        self.summoners_collection = self.db.summoners
        self.matches_collection = self.db.matches
        
    #summoners
    
    def insert_summoner(self, summoner_name: str, tag_line: str):
        try:
            result = self.summoners_collection.insert_one({"summoner_name": summoner_name, "tag_line": tag_line})
            return {"message": f"Inserted document with ID: {str(result.inserted_id)}", "success": True}
        except Exception as e:
            return {"error": f"An error occurred while inserting data: {e}", "success": False}
                
    def insert_many_summoners(self, summoners_list: list):
        try:
            summoners = self.summoners_collection.insert_many(summoners_list)
            return {"message": f"Inserted {len(summoners.inserted_ids)} documents", "success": True}
        except Exception as e:
            return {"error": f"An error occurred while inserting data: {e}", "success": False}
        
    def get_all_summoners(self):
        try:
            summoners = list(self.summoners_collection.find({}, {"_id": 0}))  # Exclude the MongoDB ObjectId from the results
            if not summoners:
                return {"message": "No summoners found", "success": True}   
            return summoners
        except Exception as e:
            return {"error": f"An error occurred while fetching summoners: {e}", "success": False}

   #matches
        
    def get_match_data_by_id(self, match_id: str):
        try:
            match_data = self.matches_collection.find_one({"match_id": match_id}, {"_id": 0})
            if not match_data:
                return {"message": "match data not found", "success": True}
            return match_data
        except Exception as e:
            return {"error": f"An error occurred while fetching match data: {e}", "success": False}
        
    def insert_match_data_by_id(self, match_id: str, match_data: Dict):
        try:
            result = self.matches_collection.insert_one({"match_id": match_id, "match_data": match_data})
            return {"message": f"Inserted match data with ID: {str(result.inserted_id)}", "success": True}
        except Exception as e:
            return {"error": f"An error occurred while inserting match data: {e}", "success": False}
