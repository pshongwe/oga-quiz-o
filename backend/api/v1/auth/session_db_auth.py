#!/usr/bin/env python3
"""
Session database authentication module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""
    def create_session(self, user_id=None):
        """Create a session and store it in the database"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        user_session = UserSession(user_id=user_id,
                                   session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Return user_id based on session_id from the database"""
        try:
            user_sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(user_sessions) <= 0:
            return None

        user_session = user_sessions[0]
        created_at = user_session.created_at
        exp_time = created_at + timedelta(seconds=self.session_duration)
        if exp_time < datetime.now():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroy a session based on the
        session_id from the request cookie"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_sessions = UserSession.search({'session_id': session_id})
        if not user_sessions:
            return False

        user_session = user_sessions[0]
        user_session.remove()
        return True
