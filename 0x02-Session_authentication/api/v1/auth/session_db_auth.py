#!/usr/bin/env python3
"""Session authentication with expiration using db.
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from datetime import datetime, timedelta
from models.user_session import UserSession
from typing import Union
from os import getenv
from uuid import uuid4


class SessionDBAuth(SessionExpAuth):
    """Implements a session authentication with expiration
    based on Session ID stored in database."""

    def create_session(self, user_id: str = None) -> Union[str, None]:
        """Creates and stores new instance of UserSession
        and returns the Session ID."""
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid4())
        session_dict = {
            'user_id': user_id,
            'session_id': session_id,
        }
        user_session = UserSession(**session_dict)
        user_session.save()
        return session_id

    def user_id_for_session_id(
            self, session_id: str = None) -> Union[str, None]:
        """Returns `user_id` based on `session_id`."""
        if session_id is None or type(session_id) != str:
            return None
        try:
            UserSession.load_from_file()
            user_session = UserSession.search({'session_id': session_id})[0]
        except (KeyError, IndexError):
            return None     # no user session for given session_id

        if self.session_duration <= 0:  # no expiration time set
            return user_session.user_id

        created_at = user_session.created_at
        if created_at is None:
            return None

        expire_after = timedelta(seconds=self.session_duration)
        if created_at + expire_after < datetime.utcnow():  # already expired
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """Deletes the user session / logout."""
        if request is None:
            return False
        # get session id from cookie
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        # check if session id is assosiated with user id
        try:
            user_session = UserSession.search({'session_id': session_id})[0]
        except (KeyError, IndexError):
            return False     # no user session for given session_id
        # logout by deleting user_session
        user_session.remove()
        return True
