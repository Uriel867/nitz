import json
from fastapi import FastAPI
from db import collection

app = FastAPI()

@app.post("/users")  
def insert_user_data(user_data: dict):
    """
    Inserts user data directly into the MongoDB collection.
    
    :param user_data: User data to be inserted (received from API request)
    """
    try:
            result = collection.insert_one(user_data)
            return {"message": f"Inserted document with ID: {str(result.inserted_id)}", "success": True}
    except Exception as e:
        return {"error": f"An error occurred while inserting data: {e}", "success": False}

@app.get("/users")
def get_all_users():
    try:
        users = list(collection.find({}, {"_id": 0}))  # Exclude the MongoDB ObjectId from the results
        if not users:
            return {"message": "No users found", "success": True}   
        return users
    except:
        return {"error": "Couldnt connect to db"}