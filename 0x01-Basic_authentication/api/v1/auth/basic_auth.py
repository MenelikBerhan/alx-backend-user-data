#!/usr/bin/env python3
"""Basic authentication
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import Tuple, Union


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> Union[str, None]:
        """Returns the decoded value of the Base64
        string `base64_authorization_header`"""
        if base64_authorization_header is None or\
                type(base64_authorization_header) != str:
            return None
        try:
            return b64decode(base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> Union[Tuple[str, str], None]:
        """Returns the user email and password from the Base64 decoded value.
        format of Base64 decoded value: `<user_email>:<password>`"""
        if decoded_base64_authorization_header is None or\
            type(decoded_base64_authorization_header) != str or\
                decoded_base64_authorization_header.count(':') != 1:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':'))
