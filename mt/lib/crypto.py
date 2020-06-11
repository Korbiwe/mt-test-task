import random

from hashlib import pbkdf2_hmac
from hmac import compare_digest

from mt.lib.errors import MtApiInternalError

# According to official python docs pbkdf2_hmac can be a chokepoint.
# If that happens to be a problem, using OpenSSL's pbkdf2_hmac is recommended as a substitute.


def random_hex_string(length: int = 16):
    return f'{random.randrange(16 ** (length - 1)) : x}'.strip()


def hash_password(password: str):
    if len(password) > 1024:
        raise MtApiInternalError(i18n='tbd', message='Password length is too great!')

    salt = random_hex_string()

    key = pbkdf2_hmac('sha512', password.encode('utf-8'), salt.encode('utf-8'), 10000).hex()

    return f'pbkdf2-sha512|10000|{salt}|{key}'


def verify_password(password: str, password_hash: str):
    (algorithm, iterations, salt, reference_key) = password_hash.split('|')

    try:
        iterations = int(iterations)
    except ValueError:
        raise MtApiInternalError(i18n='tbd', message='The number of iterations must be represented as an integer!')

    if not all((algorithm, iterations, salt, reference_key)):
        raise MtApiInternalError(i18n='tbd', message='Invalid password hash format!')

    if algorithm != 'pbkdf2-sha512' or iterations != 10000:
        raise MtApiInternalError(i18n='tbd', message='Invalid algorithm or iteration count!')

    calculated_key = pbkdf2_hmac('sha512', password.encode('utf-8'), salt.encode('utf-8'), iterations).hex()

    return compare_digest(calculated_key, reference_key)
