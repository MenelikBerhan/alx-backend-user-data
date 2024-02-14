#!/usr/bin/env python3
"""Session authentication
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import Tuple, TypeVar, Union
from uuid import uuid4


class SessionAuth(Auth):
    """Implements a session authentication."""
    # stores `<session_id>:<user_id>` key, value pairs
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> Union[str, None]:
        """Creates a session id for `user_id` and stores it in
        `user_id_by_session_id`. Returns the created session id."""
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
