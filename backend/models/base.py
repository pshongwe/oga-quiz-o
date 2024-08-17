#!/usr/bin/env python3
"""Base module using MongoDB."""
from datetime import datetime
from typing import TypeVar, List, Iterable
from bson.objectid import ObjectId
from pymongo import MongoClient


TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"

class Base():
    """Base class."""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a Base instance."""
        self._id = kwargs.get('_id', ObjectId())
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        if isinstance(self.created_at, str):
            self.created_at = datetime.strptime(self.created_at, TIMESTAMP_FORMAT)
        self.updated_at = kwargs.get('updated_at', datetime.utcnow())
        if isinstance(self.updated_at, str):
            self.updated_at = datetime.strptime(self.updated_at, TIMESTAMP_FORMAT)

        # Assuming a common MongoDB collection for all derived classes
        self.collection_name = self.__class__.__name__.lower() + "s"

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """Equality."""
        if type(self) != type(other):
            return False
        if not isinstance(self, Base):
            return False
        return str(self._id) == str(other._id)

    def to_json(self, for_serialization: bool = False) -> dict:
        """Convert the object to a JSON dictionary."""
        result = {
            "_id": str(self._id),
            "created_at": self.created_at.strftime(TIMESTAMP_FORMAT),
            "updated_at": self.updated_at.strftime(TIMESTAMP_FORMAT),
        }
        for key, value in self.__dict__.items():
            if key.startswith("_") and not for_serialization:
                continue
            if isinstance(value, datetime):
                result[key] = value.strftime(TIMESTAMP_FORMAT)
            else:
                result[key] = value
        return result

    def save(self):
        """Save current object to MongoDB."""
        self.updated_at = datetime.utcnow()
        db = self.get_db()
        db[self.collection_name].update_one(
            {"_id": self._id},
            {"$set": self.to_json(True)},
            upsert=True
        )

    def remove(self):
        """Remove object from MongoDB."""
        db = self.get_db()
        db[self.collection_name].delete_one({"_id": self._id})

    @classmethod
    def get_db(cls):
        """Get MongoDB connection."""
        client = MongoClient("mongodb://localhost:27017/")
        return client["a_db"]

    @classmethod
    def count(cls) -> int:
        """Count all objects."""
        db = cls.get_db()
        return db[cls.__name__.lower() + "s"].count_documents({})

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """Return all objects."""
        return cls.search()

    @classmethod
    def get(cls, id: str) -> TypeVar('Base'):
        """Return one object by ID."""
        db = cls.get_db()
        data = db[cls.__name__.lower() + "s"].find_one({"_id": ObjectId(id)})
        if data:
            return cls(**data)
        return None

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """Search all objects with matching attributes."""
        db = cls.get_db()
        query = {k: v for k, v in attributes.items()}
        result = db[cls.__name__.lower() + "s"].find(query)
        return [cls(**item) for item in result]