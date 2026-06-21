import bcrypt
from models.user_model import create_user

def hash_password(password):

    password_bytes = password.encode("utf-8")

    hashed = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")


def verify_password(
    plain_password,
    hashed_password
):

    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )

def register_user(
    name,
    email,
    password
):

    hashed_password = hash_password(
        password
    )

    create_user(
        name,
        email,
        hashed_password
    )

    return True
