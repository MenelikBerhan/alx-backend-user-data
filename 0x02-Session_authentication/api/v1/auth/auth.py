#!/usr/bin/env python3
"""Class to manage API Authentication
"""
from flask import request
from typing import List, TypeVar, Union
from os import getenv


class Auth:
    """Template for all authentication system in the API.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if authentication is required. Returns `True` if `path`
        is not in `excluded_paths`, otherwise returns `False`.
        Excluded paths can contain the regex character '*' at the end."""
        if path is None or not excluded_paths:
            return True
        if not path.endswith('/'):
            path += '/'
        # return True if path is not in excluded_paths
        for excl_path in excluded_paths:
            if excl_path.endswith('*'):
                excl_path = excl_path.strip('*')
                if path.startswith(excl_path):
                    return False
            else:
                if excl_path == path:
                    return False
        return True

    def authorization_header(self, request=None) -> Union[str, None]:
        """Returns the `Authorization` header value in `request`."""
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):    # type: ignore
        """Returns the current user."""
        return None

    def session_cookie(self, request=None) -> Union[str, None]:
        """Returns the value of a cookie, named in the environment
        variable `SESSION_NAME`, from `request`."""
        if request is None:
            return None
        return request.cookies.get(getenv('SESSION_NAME'))
