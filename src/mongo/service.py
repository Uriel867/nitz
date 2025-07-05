from mongo.db import collection

class MongoService():
    def insert_summoner(self,summoner_data: dict):
        try:
            result = collection.insert_one(summoner_data)
            return {"message": f"Inserted document with ID: {str(result.inserted_id)}", "success": True}
        except Exception as e:
            return {"error": f"An error occurred while inserting data: {e}", "success": False}
        
    def insert_many_summoners(self, summoner_data: list):
        try:
            summoners = collection.insert_many(summoner_data)
            return {"message": f"Inserted {len(summoners.inserted_ids)} documents", "success": True}
        except Exception as e:
            return {"error": f"An error occurred while inserting data: {e}", "success": False}
        
    def get_all_summoners(self):
        try:
            summoners = list(collection.find({}, {"_id": 0}))  # Exclude the MongoDB ObjectId from the results
            if not summoners:
                return {"message": "No summoners found", "success": True}   
            return summoners
        except Exception as e:
            return {"error": f"An error occurred while fetching summoners: {e}", "success": False}
        
    def get_summoner(self, summoner_name: str, battle_tag: int):
        try:
            summoner = collection.find_one({"summoner_name": summoner_name, "battle_tag": battle_tag}, {"_id": 0})  # Exclude the MongoDB ObjectId from the results
            if not summoner:
                return {"message": "Summoner not found", "success": True}
            return summoner
        except Exception as e:
            return {"error": f"An error occurred while fetching the summoner: {e}", "success": False}