from pymongo import MongoClient

class LoLStatsService:
    
    def __init__(self, mongo_client: MongoClient):
        self.mongo_client = mongo_client
        self.db = mongo_client.lol
        self.summoners_collection = self.db.summoners
        self.match_id_collection = self.db.match_ids
        self.match_data_collection = self.db.match_data
        
    def insert_summoner(self, summoner_name: str,puuid: str):
        try:
            result = self.summoners_collection.insert_one({summoner_name: puuid})
            return {"message": f"Inserted document with ID: {str(result.inserted_id)}", "success": True}
        except Exception as e:
            return {"error": f"An error occurred while inserting data: {e}", "success": False}
        
    def insert_many_summoners(self, summoner_data: list):
        try:
            summoners = self.summoners_collection.insert_many(summoner_data)
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
        
    def get_summoner(self, summoner_name: str, battle_tag: int):
        try:
            summoner = self.summoners_collection.find_one({"summoner_name": summoner_name, "battle_tag": battle_tag}, {"_id": 0})  # Exclude the MongoDB ObjectId from the results
            if not summoner:
                return {"message": "Summoner not found", "success": True}
            return summoner
        except Exception as e:
            return {"error": f"An error occurred while fetching the summoner: {e}", "success": False}

    def get_match_id(self, match_id: str):
        try:
            match = self.match_id_collection.find_one({"match_id": match_id}, {"_id": 0})  # Exclude the MongoDB ObjectId from the results
            if not match:
                return {"message": "Match not found", "success": True}
            return match
        except Exception as e:
            return {"error": f"An error occurred while fetching match IDs: {e}", "success": False}
        
    def insert_match_id(self, match_id: str):
        try:
            result = self.match_id_collection.insert_one({"match_id": match_id})
            return {"message": f"Inserted match document with ID: {str(result.inserted_id)}", "success": True}
        except Exception as e:
            return {"error": f"An error occurred while inserting match data: {e}", "success": False}
        
    def get_match_data_by_summoner(self, summoner_puuid: str):
        try:
            match_data = self.match_data_collection.find({"summoner_name": summoner_puuid}, {"_id": 0})  # Exclude the MongoDB ObjectId from the results
            matches = list(match_data)
            if not matches:
                return {"message": "No matches found for this summoner", "success": True}
            return matches
        except Exception as e:
            return {"error": f"An error occurred while fetching match data: {e}", "success": False}
    
    def get_match_data_by_id(self, match_id):
        try:
            match_data = self.match_data_collection.find_one({"match id": match_id}, {"_id": 0})
            if not match_data:
                return {"message": "match data not found", "success": True}
            return match_data
        except Exception as e:
            return {"error": f"An error occurred while fetching match data: {e}", "success": False}

