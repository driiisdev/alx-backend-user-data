#!/usr/bin/env python3
"""
Reloads the object data from the file storage
"""
try:
    from api.v1.views import *
    User.load_from_file()
except Exception:
    pass