#!/usr/bin/env python3
"""
Route module for the API
"""
from api.v1.views import app_views
from flask import Flask, abort, jsonify, request
from flask_cors import (CORS, cross_origin)
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None     # stores the type of authentication to use
if getenv('AUTH_TYPE') == 'session_db_auth':
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()
elif getenv('AUTH_TYPE') == 'session_exp_auth':
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif getenv('AUTH_TYPE') == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif getenv('AUTH_TYPE') == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif getenv('AUTH_TYPE') == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()


@app.before_request
def authentication_filter():
    """Checks if request path requires authentication."""
    if auth is None:
        return
    # routes that doesn't require authorization
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/',
                      '/api/v1/forbidden/', '/api/v1/auth_session/login/']
    if not auth.require_auth(request.path, excluded_paths):  # path in `exclud`
        return
    if auth.authorization_header(request) is None and\
            auth.session_cookie(request) is None:
        abort(401)
    # get current user (using authorization header or session id)
    current_user = auth.current_user(request)
    if current_user is None:
        abort(403)
    request.current_user = current_user


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error):
    """Unauthorized error handler"""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def not_allowed(error):
    """Authorized but not allowed error handler"""
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
