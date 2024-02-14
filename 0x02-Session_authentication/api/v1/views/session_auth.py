#!/usr/bin/env python3
""" Module of Index views
"""
from flask import request, jsonify
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """ POST /api/v1/auth_session/login
    Return:
      - the session token
    """
    # get user email and password
    email = request.form.get('email')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 404
    password = request.form.get('password')
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 404

    # retrieve user based on email
    try:
        user = User.search({'email': email})[0]
    except (IndexError, KeyError):    # no user for given email
        return jsonify({"error": "no user found for this email"}), 404

    # check if given password matches user's password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    # create session id and set it in responses cookie
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(getenv('SESSION_NAME'), session_id)
    return response
