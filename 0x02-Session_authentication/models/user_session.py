#!/usr/bin/env python3

"""
This module provides the class `UserSession`
"""

from models.base import Base


class UserSession(Base):
    """
    A Class `UserSession` that saves all
    session credentials to a database
    """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize instance """
        super().__init__(self, *args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
