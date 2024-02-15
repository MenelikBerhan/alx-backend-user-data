#!/usr/bin/env python3
"""Session authentication with expiration
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from typing import Union
from os import getenv


class SessionExpAuth(SessionAuth):
    """Implements a session authentication with expiration."""
    def __init__(self):
        """Initialize instance."""
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> Union[str, None]:
        """Creates a session id for `user_id` and stores it in
        `user_id_by_session_id`. Returns the created session id."""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(
            self, session_id: str = None) -> Union[str, None]:
        """Returns `user_id` based on `session_id`."""
        if session_id is None or type(session_id) != str:
            return None
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:  # no expiration time set
            return session_dict['user_id']

        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        expire_after = timedelta(seconds=self.session_duration)
        if created_at + expire_after < datetime.now():  # already expired
            return None
        return session_dict['user_id']
