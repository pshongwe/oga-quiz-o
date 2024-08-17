#!/usr/bin/env python3
"""Authentication module for the API.
"""
#!/usr/bin/env python3
"""
Auth file using MongoDB
"""
import bcrypt
from libs.db import DB
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Create password Hash"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a uuid"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> dict:
        """Register a user"""
        try:
            cur_user = self._db.find_user_by(email=email)

            if cur_user:
                raise ValueError(f"User {email} already exists")
        except ValueError:
            pass

        hp = _hash_password(password)
        new_user = self._db.add_user(
            email=email, hashed_password=hp.decode('utf-8'))
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if a user's login details are valid."""
        try:
            user = self._db.find_user_by(email=email)
            hp = user["hashed_password"].encode("utf-8")
            if user and bcrypt.checkpw(password.encode("utf-8"), hp):
                return True
        except ValueError:
            return False
        return False

    def create_session(self, email: str) -> str:
        """Create a session"""
        try:
            cur_user = self._db.find_user_by(email=email)

            if not cur_user:
                return None
            session_id = _generate_uuid()
            self._db.update_user(cur_user["_id"], session_id=session_id)
            return session_id
        except ValueError:
            return None

    def get_user_from_session_id(self, session_id: str) -> dict:
        """Get user from session_id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except ValueError:
            return None

    def destroy_session(self, user_id: str) -> None:
        """Destroy user session"""
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate password reset token for user"""
        try:
            user = self._db.find_user_by(email=email)
            if user is None:
                raise ValueError()
            reset_token = _generate_uuid()
            self._db.update_user(user["_id"], reset_token=reset_token)
            return reset_token
        except ValueError:
            raise ValueError()

    def update_password(self, reset_token: str, password: str) -> None:
        """Update user password using reset token"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user is None:
                raise ValueError()
            new_password_hash = _hash_password(password)
            self._db.update_user(
                user["_id"],
                hashed_password=new_password_hash.decode("utf-8"),
                reset_token=None,
            )
        except ValueError:
            raise ValueError()