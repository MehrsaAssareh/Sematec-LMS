import hashlib
import hmac
import os


PASSWORD_ITERATIONS = 210_000


def hash_password(password, salt=None, iterations=PASSWORD_ITERATIONS):
    if password is None:
        raise ValueError('Password is required.')

    if salt is None:
        salt = os.urandom(16)

    if isinstance(salt, memoryview):
        salt = salt.tobytes()

    password_bytes = password.encode('utf-8')
    password_hash = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, iterations)
    return salt, password_hash, iterations


def verify_password(password, salt, password_hash, iterations):
    if not password or not salt or not password_hash or not iterations:
        return False

    if isinstance(salt, memoryview):
        salt = salt.tobytes()

    if isinstance(password_hash, memoryview):
        password_hash = password_hash.tobytes()

    _, attempted_hash, _ = hash_password(password, bytes(salt), int(iterations))
    return hmac.compare_digest(attempted_hash, bytes(password_hash))
