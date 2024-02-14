#!/usr/bin/env python3
"""Session authentication
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import Tuple, TypeVar, Union


class SessionAuth(Auth):
    """Implements a session authentication."""
    pass
