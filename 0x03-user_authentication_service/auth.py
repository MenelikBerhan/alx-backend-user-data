#!/usr/bin/env python3
"""User Authentication
"""
from db import DB
from bcrypt import hashpw, gensalt
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    """Returns a salted hash of the input password as bytes."""
    return hashpw(password.encode(), gensalt())


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
