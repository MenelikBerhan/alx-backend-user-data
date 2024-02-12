"""Class to manage API Authentication
"""
from flask import request
from typing import List, TypeVar

class Auth():
    """Template for all authentication system in the API.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if authentication is required."""
        return False

    def authorization_header(self, request=None) -> str:
        """Extracts the authorize header from request."""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user."""
        return None
