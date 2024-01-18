#!/usr/bin/env python3

"""
This module provides the class `SessionAuth`
"""

from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """
    A class `SessionAuth` for all
    Session authentication operations
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session id for the current user id
        Parameters:
            user_id: id of current user
        Return:
            session id for user_id
        """
        if user_id is None:
            return
        if not isinstance(user_id, str):
            return
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a user_id based on a given session_id
        Parameters:
            session_id: current session id
        Return:
            user_id of current session
        """
        if session_id is None:
            return
        if not isinstance(session_id, str):
            return
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Creates and returns a User instance based on session_id
        """
        if request is None:
            return
        session = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """ Destroys the current user session in order to log user out """
        session = self.session_cookie(request)
        if session is None:
            return False
        if session == '':
            return False
        if session not in self.user_id_by_session_id.keys():
            return False
        if session in self.user_id_by_session_id.keys():
            del self.user_id_by_session_id[session]
        return True
