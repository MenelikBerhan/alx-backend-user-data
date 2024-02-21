#!/usr/bin/env python3
"""User Authentication
"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """Returns a salted hash of the input password as bytes."""
    return hashpw(password.encode(), gensalt())
