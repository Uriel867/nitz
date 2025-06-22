from mongo.db import collection

class MongoService():
    def insert_user(self,user_data: dict):
        try:
            result = collection.insert_one(user_data)
            return {"message": f"Inserted document with ID: {str(result.inserted_id)}", "success": True}
        except Exception as e:
            return {"error": f"An error occurred while inserting data: {e}", "success": False}
        
    def insert_many_users(self, user_data: list):
        try:
            users = collection.insert_many(user_data)
            return {"message": f"Inserted {len(users.inserted_ids)} documents", "success": True}
        except Exception as e:
            return {"error": f"An error occurred while inserting data: {e}", "success": False}
        
    def get_all_users(self):
        try:
            users = list(collection.find({}, {"_id": 0}))  # Exclude the MongoDB ObjectId from the results
            if not users:
                return {"message": "No users found", "success": True}   
            return users
        except Exception as e:
            return {"error": f"An error occurred while fetching users: {e}", "success": False}
        
    def get_user(self, user_name: str, battle_tag: int):
        try:
            user = collection.find_one({"user_name": user_name, "battle_tag": battle_tag}, {"_id": 0})  # Exclude the MongoDB ObjectId from the results
            if not user:
                return {"message": "User not found", "success": True}
            return user
        except Exception as e:
            return {"error": f"An error occurred while fetching the user: {e}", "success": False}