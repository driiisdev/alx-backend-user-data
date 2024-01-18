#!/usr/bin/env python3

"""
This module provides the class Auth
"""

from flask import request
from os import getenv
import re
from typing import (
        List,
        TypeVar
    )


class Auth:
    """ Auth class for authentication operations """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if a resource defined by
        `path` needs authentication
        """
        if path is None or excluded_paths is None:
            return True
        if path[len(path) - 1] != '/' and path[len(path) - 1] != '*':
            path += '/'
        for excluded_path in excluded_paths:
            if path[len(path) - 1] == '*':
                if bool(re.match(fr'^{excluded_path}\w*', path)):
                    return False
            if path in excluded_paths:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Gets and returns the authorization header of the request
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Gets and returns the current user object"""
        return None

    def session_cookie(self, request=None):
        """ Gets the current session's id """
        if request is None:
            return None
        self._my_session_id = getenv('SESSION_NAME')
        return request.cookies.get(self._my_session_id)
