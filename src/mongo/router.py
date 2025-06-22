import json
from fastapi import FastAPI,APIRouter
from typing import List, Dict
from mongo.service import MongoService

router = APIRouter(prefix="/users")
ms = MongoService()

@router.post("/insert")  
def insert_user(user_data: dict):
    """
    Inserts user data directly into the MongoDB collection.
    
    :param user_data: User data to be inserted (received from API request)
    """
    
    return ms.insert_user(user_data)

@router.post("/insert_many")
def insert_many_users(user_data: List[Dict]):
    """
    Inserts multiple user data into the MongoDB collection.
    
    :param user_data: List of user data to be inserted (received from API request)
    """
    
    return ms.insert_many_users(user_data)

@router.get("/all")
def get_all_users():
    """
    Retrieves all users from the MongoDB collection.
    
    :return: List of all users or a message if no users are found
    """
    
    return ms.get_all_users()

@router.get("/get")
def get_user(user_name: str,battle_tag: int):
    """
    Retrieves a user from the MongoDB collection based on user_name and battle_tag.
    
    :param user_name: The name of the user to retrieve
    :param battle_tag: The battle tag of the user to retrieve
    :return: The user data or a message if the user is not found
    """
    return ms.get_user(user_name, battle_tag)
