import json
from fastapi import FastAPI
from db import collection
from typing import List, Dict
app = FastAPI()

@app.post("/users/insert")  
def insert_user(user_data: dict):
    """
    Inserts user data directly into the MongoDB collection.
    
    :param user_data: User data to be inserted (received from API request)
    """
    try:
        result = collection.insert_one(user_data)
        return {"message": f"Inserted document with ID: {str(result.inserted_id)}", "success": True}
    except Exception as e:
        return {"error": f"An error occurred while inserting data: {e}", "success": False}
    
@app.post("/users/insert_many")
def insert_many_users(user_data: List[Dict]):
    try:
        users = collection.insert_many(user_data)
        return {"message": f"Inserted {len(users.inserted_ids)} documents", "success": True}
    except Exception as e:
        return {"error": f"An error occurred while inserting data: {e}", "success": False}

@app.get("/users/all")
def get_all_users():
    try:
        users = list(collection.find({}, {"_id": 0}))  # Exclude the MongoDB ObjectId from the results
        if not users:
            return {"message": "No users found", "success": True}   
        return users
    except Exception as e:
        return {"error": f"An error occurred while fetching users: {e}", "success": False}

@app.get("/users/get")
def get_user(user_name: str,battle_tag: int):
    try:
        user = collection.find_one({"user_name": user_name, "battle_tag": battle_tag}, {"_id": 0})
        if user:
            return user
        else:
            return {"message": "User not found", "success": True}
    except Exception as e:
        return {"error": f"An error occurred while fetching user: {e}", "success": False}
