#!/usr/bin/env python3
"""Hashing password using bcrypt.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed byte string `password."""
    # encode password bfr passing to `haspw`
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password
