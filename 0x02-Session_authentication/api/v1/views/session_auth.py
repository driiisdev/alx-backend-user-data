#!/usr/bin/env python3

""" Module for login feature
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from os import getenv
from models.user import User


@app_views.route('/auth_session/login',
                 methods=['POST'], strict_slashes=False)
def login():
    """
    Logs-in a user based on a session created for such user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or not len(email):
        return jsonify({'error': 'email missing'}), 400
    if password is None or not len(password):
        return jsonify({'error': 'password missing'}), 400
    users = User.search({'email': email})
    if users is None or not len(users):
        return jsonify({'error': 'no user found for this email'}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response = jsonify(user.to_json())
            response.set_cookie(getenv('SESSION_NAME', '_my_session_id'),
                                session_id)
            return response
    return jsonify({'error': 'wrong password'}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    """
    Logs-out a user based on a session created for such user
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/auth_session/signup',
                 methods=['POST'], strict_slashes=False)
def signup():
    """
    Creates a user account for authentication
    """
    email = request.form.get('email')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    if email is None or not len(email):
        return jsonify({'error': 'email missing'}), 400
    if password is None or not len(password):
        return jsonify({'error': 'password missing'}), 400
    if first_name is None or not len(first_name):
        return jsonify({'error': 'first_name missing'}), 400
    if last_name is None or not len(last_name):
        return jsonify({'error': 'last_name missing'}), 400
    user_info = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name
    }
    newUser = User(**user_info)
    newUser.password = password
    newUser.save()
    return jsonify(newUser.to_json()), 201
