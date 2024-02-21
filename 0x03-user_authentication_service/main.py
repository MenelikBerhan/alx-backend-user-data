#!/usr/bin/env python3
"""Tests for app routes.
"""
import requests


def register_user(email: str, password: str) -> None:
    """Tests user registration."""
    response = requests.post('http://0.0.0.0:5000/users',
                             data={'email': email, 'password': password})
    assert (response.status_code == 200)
    resp_json = response.json()
    assert (resp_json.get('email') == email)
    assert (resp_json.get('message') == 'user created')


def log_in_wrong_password(email: str, password: str) -> None:
    """Tests login with wrong password."""
    response = requests.post('http://0.0.0.0:5000/sessions',
                             data={'email': email, 'password': password})
    assert (response.status_code == 401)


def log_in(email: str, password: str) -> str:
    response = requests.post('http://0.0.0.0:5000/sessions',
                             data={'email': email, 'password': password})
    assert (response.status_code == 200)
    resp_json = response.json()
    assert (resp_json.get('email') == email)
    assert (resp_json.get('message') == 'logged in')
    session_id = response.cookies.get('session_id')
    assert (len(session_id) == 36)   # uuid
    return session_id


def profile_unlogged() -> None:
    """Tests getting profile w/o valid session_id."""
    response = requests.get('http://0.0.0.0:5000/profile')
    assert (response.status_code == 403)


def profile_logged(session_id: str) -> None:
    """Tests getting profile with valid session_id."""
    response = requests.get('http://0.0.0.0:5000/profile',
                            cookies={'session_id': session_id})
    assert (response.status_code == 200)
    assert (response.json().get('email') is not None)


def log_out(session_id: str) -> None:
    """Tests logout."""
    response = requests.delete('http://0.0.0.0:5000/sessions',
                               cookies={'session_id': session_id},
                               allow_redirects=True)
    assert (response.status_code == 200)


def reset_password_token(email: str) -> str:
    """Tests password reset token creation."""
    response = requests.post('http://0.0.0.0:5000/reset_password',
                             data={'email': email})
    assert (response.status_code == 200)
    resp_json = response.json()
    assert (resp_json.get('email') == email)
    new_reset_token = resp_json.get('reset_token')
    assert (len(new_reset_token) == 36)  # uuid
    return new_reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests password updating."""
    response = requests.put('http://0.0.0.0:5000/reset_password',
                            data={'email': email,
                                  'reset_token': reset_token,
                                  'new_password': new_password
                                  }
                            )
    assert (response.status_code == 200)
    resp_json = response.json()
    assert (resp_json.get('email') == email)
    assert (resp_json.get('message') == 'Password updated')


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
