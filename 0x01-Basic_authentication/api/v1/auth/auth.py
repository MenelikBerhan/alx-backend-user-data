#!/usr/bin/env python3
"""Class to manage API Authentication
"""
from flask import request
from typing import List, TypeVar, Union


class Auth:
    """Template for all authentication system in the API.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if authentication is required. Returns `True`if `path`
        is not in `excluded_paths`, otherwise returns `False`."""
        if path is None or not excluded_paths:
            return True
        if not path.endswith('/'):
            path += '/'
        # return True if path is not in excluded_paths
        return not bool(excluded_paths.count(path))

    def authorization_header(self, request=None) -> Union[str, None]:
        """Returns the `Authorization` header value in `request`."""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):    # type: ignore
        """Returns the current user."""
        return None
