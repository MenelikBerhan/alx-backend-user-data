#!/usr/bin/env python3
"""User Authentication
"""
from db import DB
from bcrypt import checkpw, hashpw, gensalt
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from user import User
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Returns a salted hash of the input password as bytes."""
    return hashpw(password.encode(), gensalt())


def _generate_uuid() -> str:
    """Returns a string representation of a new UUID."""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize instance"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """After hashing `password`, creates and stores a new `User` in DB,
        and returns the newly created user.

        Raises:
            `ValueError` if a user with same `email` already exist in DB."""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user
        else:       # user with same `email` already exists
            raise ValueError('User {} already exists'.format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if a user with given email & password exists."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return checkpw(password.encode(), user.hashed_password)

    def create_session(self, email: str) -> Union[str, None]:
        """If a user with given `email` exists, creates a
        session_id attribute for the user and returns the id."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """If a user with given `session_id` exists, returns the user."""
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys session by removing session id from user."""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Updates users `reset_token` attribute, and return the new token.
        
        Raises:
            `ValueError` if no user with given `email` exists."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        new_reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=new_reset_token)
        return new_reset_token
