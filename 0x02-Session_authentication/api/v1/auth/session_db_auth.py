#!/usr/bin/env python3

"""
This module provides the class `SessionDBAuth`
"""

from api.v1.auth.session_exp_auth import (
    SessionExpAuth,
    datetime,
    timedelta
)
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    A class `SessionDBAuth` that handles saving
    all session credentails to a databsae
    """

    def create_session(self, user_id=None):
        """ Creates a UserSession instance and return the session id """
        if user_id is None:
            return
        session_id = super().create_session(user_id)
        user_session = UserSession(**{
                                    'session_id': session_id,
                                    'user_id': user_id
                                })
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the user_id for the current session
        """
        if session_id is None:
            return
        user_session = UserSession.search({'session_id': session_id})
        created_at = self.user_id_by_session_id\
            .get(session_id).get('created_at')
        session_duration = self.session_duration
        if session_duration <= 0:
            if len(user_session):
                return user_session[0].user_id
            return
        duration = created_at + timedelta(seconds=self.session_duration)
        if 'created_at' not in self.user_id_by_session_id\
                .get(session_id).keys():
            return
        if duration < datetime.now():
            return
        if len(user_session):
            return user_session[0].user_id

    def destroy_session(self, request=None):
        """
        Destroys a UserSession instance from
        the database in order to log out
        """
        session = self.session_cookie(request)
        if session is None:
            return False
        if session == '':
            return False
        user_session = UserSession.search({'session_id': session})
        if not len(user_session):
            return False
        if user_session[0].session_id != session:
            return False
        user_session[0].remove()
        return True
