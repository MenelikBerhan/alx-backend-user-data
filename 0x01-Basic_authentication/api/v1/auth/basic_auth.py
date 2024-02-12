#!/usr/bin/env python3
"""Basic authentication
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import Tuple, TypeVar, Union


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
        format of Base64 decoded value: `<user_email>:<password>`. Password
        could contain the separator `:`, but not the email."""
        if decoded_base64_authorization_header is None or\
            type(decoded_base64_authorization_header) != str or\
                decoded_base64_authorization_header.count(':') == 0:
            return (None, None)
        separator_index = decoded_base64_authorization_header.index(':')
        return (decoded_base64_authorization_header[:separator_index],
                decoded_base64_authorization_header[separator_index + 1:])

    def user_object_from_credentials(
            self, user_email: str,
            user_pwd: str) -> TypeVar('User'):  # type: ignore
        """Returns the User instance based on his email and password."""
        if user_email is None or type(user_email) != str or\
                user_pwd is None or type(user_pwd) != str:
            return None
        try:
            user = User.search({'email': user_email})[0]
        except (IndexError, KeyError):    # no user instance in db
            return None

        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):    # type: ignore
        """Returns the current user."""
        # extract Authorization header value
        aut_header = self.authorization_header(request)
        # get part of Authorization value after word `Base `
        base64_aut_hdr = self.extract_base64_authorization_header(aut_header)
        # decode value from base 64
        decoded_hdr = self.decode_base64_authorization_header(base64_aut_hdr)
        # get email and password values
        email, password = self.extract_user_credentials(decoded_hdr)
        # get user
        user = self.user_object_from_credentials(email, password)
        return user
