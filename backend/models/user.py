#!/usr/bin/env python3
"""The `user` model's module using MongoDB.
"""
from bson.objectid import ObjectId


class User:
    """Represents a record from the `users` collection.
    """

    def __init__(self, email: str, hashed_password: str, session_id: str = None, reset_token: str = None):
        self._id = ObjectId()
        self.email = email
        self.hashed_password = hashed_password
        self.session_id = session_id
        self.reset_token = reset_token

    def to_dict(self):
        """Converts the User object to a dictionary."""
        return {
            "_id": self._id,
            "email": self.email,
            "hashed_password": self.hashed_password,
            "session_id": self.session_id,
            "reset_token": self.reset_token,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a User object from a dictionary."""
        user = cls(
            email=data["email"],
            hashed_password=data["hashed_password"],
            session_id=data.get("session_id"),
            reset_token=data.get("reset_token"),
        )
        user._id = data["_id"]
        return user
