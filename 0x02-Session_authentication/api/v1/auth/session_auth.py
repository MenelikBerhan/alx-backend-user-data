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

    def user_id_for_session_id(
            self, session_id: str = None) -> Union[str, None]:
        """Returns `user_id` based on `session_id`."""
        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> Union[User, None]:
        """Returns a `User` instance based on a cookie value for seesion id."""
        # get session id from cookie
        session_id = self.session_cookie(request)
        # get user id
        user_id = self.user_id_for_session_id(session_id)
        # get user
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """Deletes the user session / logout."""
        if request is None:
            return False
        # get session id from cookie
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        # check if session id is assosiated with user id
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        # logout by deleting session id entry
        del self.user_id_by_session_id[session_id]
        return True
