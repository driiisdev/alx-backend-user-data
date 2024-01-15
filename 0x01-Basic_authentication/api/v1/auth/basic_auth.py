#!/usr/bin/env python3

"""
This module provides the class BasicAuth
"""

from api.v1.auth.auth import Auth
from base64 import b64decode
from models.base import Base
from models.user import User
import re
from typing import (
    Tuple,
    TypeVar
)


class BasicAuth(Auth):
    """
    A class `BasicAuth` for all Basic
    authentication operations
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        This method extracts the authentication
        credentials from the Authorization header
        """
        if authorization_header is None:
            return
        if not isinstance(authorization_header, str):
            return
        if not bool(re.match(r'^Basic \w*', authorization_header)):
            return
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str)\
            -> str:
        """
        This method returns the decoded value of
        a Base64 string `base64_authorization_header`
        """
        if base64_authorization_header is None:
            return
        if not isinstance(base64_authorization_header, str):
            return
        try:
            credentials = b64decode(base64_authorization_header)
            return credentials.decode('utf-8')
        except Exception:
            return

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str)\
            -> Tuple[str, str]:
        """
        This method  returns the user email and
        password from the Base64 decoded value.
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        credentials = decoded_base64_authorization_header.split(':')
        email = credentials[0]
        credentials.pop(0)
        pwd = ':'.join(credentials)
        return (email, pwd)

    def user_object_from_credentials(self, user_email: str, user_pwd: str)\
            -> TypeVar('User'):
        """
        This method  returns the User instance based on his email and password.
        """
        if user_email is None or user_pwd is None:
            return
        if not isinstance(user_email, str) or not isinstance(user_email, str):
            return
        User.load_from_file()
        if User.count() == 0:
            return
        if len(User.search({'email': user_email})) == 0:
            return
        for user in User.search({'email': user_email}):
            if user.is_valid_password(user_pwd):
                return user
        return

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user object """
        if request is None:
            return
        b64_auth = self.authorization_header(request)
        b64_credentials = self.extract_base64_authorization_header(b64_auth)
        credentials = self.decode_base64_authorization_header(b64_credentials)
        user_email, user_pwd = self.extract_user_credentials(credentials)
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
