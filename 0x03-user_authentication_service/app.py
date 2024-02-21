#!/usr/bin/env python3
"""Basic Flask app
"""
from auth import Auth
from flask import abort, Flask, jsonify, redirect, request


app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def index():
    """Home page"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Creates and a user using `email` and `password` in request."""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    else:
        return jsonify({"email": email, "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """If a user with given email & password exists creates a session id."""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email=email, password=password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """If a user with given session id exists, deletes its session."""
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """Returns the user's email if one with given session id exists."""
    user = AUTH.get_user_from_session_id(request.cookies.get('session_id'))
    if user is None:
        abort(403)
    return jsonify(email=user.email)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """Generates reset_token for a user of given email in request form."""
    email = request.form.get('email')
    try:
        new_reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": new_reset_token})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """Updates user's password based on "reset_token"."""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
