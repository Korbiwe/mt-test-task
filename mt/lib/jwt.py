import jwt

from datetime import datetime, timedelta

from mt.config.jwt import (
    SECRET,
    DEFAULT_EXPIRES_IN
)


def create_jwt(payload: dict, expires_in: timedelta = DEFAULT_EXPIRES_IN):
    payload['exp'] = datetime.utcnow() + expires_in
    return jwt.encode(payload, SECRET, algorithm='HS256').decode('utf-8')


def decode_jwt(token: str):
    return jwt.decode(token, SECRET, algorithms='HS256')
