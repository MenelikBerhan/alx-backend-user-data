#!/usr/bin/env python3
"""Basic authentication
"""
from api.v1.auth.auth import Auth
from typing import Union


class BasicAuth(Auth):
    """Implements a basic authentication."""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> Union[str, None]:
        """Returns the `Base64` part of the `Authorization` header for a
        `Basic Authentication`. (values after `Basic `)"""
        if authorization_header is None or type(authorization_header) != str:
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header.split(' ')[1]
