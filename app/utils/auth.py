import string
import random
import bcrypt
import hashlib
from utils import consts


class Password:

    def __init__(self, salt, hashed_password):
        self.salt = salt
        self.hashed_password = hashed_password


def create_token(length: int = consts.Consts.TOKEN_LENGTH):
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])


def generate_random_password(n=12):
    return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(n))


def hash_password(password: str):
    salt = bcrypt.gensalt()  # salt is unique
    # bcrypt the password using the salt and concat a secret key not present in database (hardcoded on backend only)
    encrpyted_password = bcrypt.hashpw((f"{password}+{consts.Consts.SECRET_KEY}").encode('utf8'), salt.encode('utf-8'))
    hashed_password = hashlib.sha512(encrpyted_password).hexdigest()
    return Password(salt, hashed_password)


def does_password_match(salt, hashed_password_in_db, password_to_check):
    encoded_string_password = f"{password_to_check}+{consts.Consts.SECRET_KEY}"
    encrpyted_password = bcrypt.hashpw(encoded_string_password.encode('utf8'), salt.encode('utf8'))
    hashed_password_to_check = hashlib.sha512(encrpyted_password).hexdigest()
    if hashed_password_in_db == hashed_password_to_check:
        return True
    return False
