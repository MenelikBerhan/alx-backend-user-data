#!/usr/bin/env python3
"""Basic Flask app
"""
from auth import Auth
from flask import abort, Flask, jsonify, request


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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
