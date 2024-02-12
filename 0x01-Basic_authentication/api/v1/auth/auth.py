"""Class to manage API Authentication
"""
from flask import request


class Auth():
    """Template for all authentication system in the API.
    """
    def require_auth(self, path, excluded_paths):
        """Checks if authentication is required."""
        return False

    def authorization_header(self, request=None):
        """Extracts the authorize header from request."""
        return None

    def current_user(self, request=None):
        """Returns the current user."""
        return None
