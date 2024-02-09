#!/usr/bin/env python3
"""Hashing password using bcrypt.
"""
import bcrypt       # type: ignore


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed byte string `password."""
    # encode password bfr passing to `haspw`
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if `password` matches `hased_password`."""
    # encode password bfr passing to `checkpw`
    return bcrypt.checkpw(password.encode(), hashed_password)
