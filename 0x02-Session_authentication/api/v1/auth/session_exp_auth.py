#!/us/bin/env python3

"""
This module provides the class `SessionExpAuth`
"""


from api.v1.auth.session_auth import SessionAuth
from datetime import (
    datetime,
    timedelta
)
from os import getenv


class SessionExpAuth(SessionAuth):
    """
    A class `SessionExpAuth` for all
    Session authentication operations
    with expiring sessions
    """

    def __init__(self):
        """ Initialize instance """
        self.session_duration = 0
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except Exception:
            pass

    def create_session(self, user_id=None):
        """
        Creates a session id for the current user id
        Parameters:
            user_id: id of current user
        Return:
            session id for user_id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return
        self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns a user_id based on a given session_id
        Parameters:
            session_id: current session id
        Return:
            user_id of current session
        """
        if session_id is None:
            return
        if session_id not in self.user_id_by_session_id.keys():
            return
        created_at = self.user_id_by_session_id\
            .get(session_id).get('created_at')
        session_duration = self.session_duration
        if session_duration <= 0:
            return self.user_id_by_session_id\
                .get(session_id).get('user_id')
        duration = created_at + timedelta(seconds=self.session_duration)
        if 'created_at' not in self.user_id_by_session_id\
                .get(session_id).keys():
            return
        if duration < datetime.now():
            return
        return self.user_id_by_session_id.get(session_id).get('user_id')
