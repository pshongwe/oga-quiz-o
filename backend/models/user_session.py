#!/usr/bin/env python3
"""
UserSession model using MongoDB
"""
from bson.objectid import ObjectId
from models.base import Base


class UserSession(Base):
    """UserSession class"""

    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a UserSession instance"""
        super().__init__(*args, **kwargs)
        self._id = ObjectId()
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

    def to_dict(self):
        """Converts the UserSession object to a dictionary."""
        return {
            "_id": self._id,
            "user_id": self.user_id,
            "session_id": self.session_id,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a UserSession object from a dictionary."""
        session = cls(
            user_id=data.get("user_id"),
            session_id=data.get("session_id"),
        )
        session._id = data["_id"]
        return session
