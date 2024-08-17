#!/usr/bin/env python3
"""DB module using MongoDB.
"""
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
import os


MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_HOST = os.environ.get('MONGO_HOST')
MONGO_DBNAME = os.environ.get('MONGO_DBNAME')


class DB:
    """DB class.
    """

    def __init__(self, dbname: str = MONGO_DBNAME) -> None:
        """Initialize a new DB instance.
        """
        self._client = MongoClient(f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/{MONGO_DBNAME}?retryWrites=true&w=majority")
        self._db = self._client[dbname]
    
    def get_collection(self, collection_name: str):
        """Dynamically get a collection by name."""
        return self._db[collection_name]


    def add_user(self, email: str, hashed_password: str, collection_name: str = "users") -> dict:
        """Adds a new user to the database.
        """
        try:
            collection = self.get_collection(collection_name)
            collection.create_index("email", unique=True)
            user = {"email": email, "hashed_password": hashed_password}
            result = collection.insert_one(user)
            user["_id"] = result.inserted_id
            return user
        except DuplicateKeyError:
            return None

    def find_user_by(self, collection_name: str = "users", **kwargs) -> dict:
        """Finds a user based on a set of filters.
        """
        collection = self.get_collection(collection_name)
        user = collection.find_one(kwargs)
        if not user:
            raise ValueError("No user found with the given criteria.")
        return user

    def update_user(self, user_id: str, collection_name: str = "users", **kwargs) -> None:
        """Updates a user based on a given id.
        """
        collection = self.get_collection(collection_name)
        result = collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": kwargs}
        )
        if result.matched_count == 0:
            raise ValueError("No user found with the given id.")