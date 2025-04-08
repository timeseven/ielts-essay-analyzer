import bcrypt

from app.auth.utils import verify_password


def test_verify_password_success():
    """
    Tests that verify_password returns True for a correct plain text password
    matched against a corresponding hashed password.
    """
    plain_password = "my_password"
    hashed_password = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    assert verify_password(plain_password, hashed_password) is True


def test_verify_password_failure():
    """
    Tests that verify_password returns False for an incorrect plain text
    password matched against a corresponding hashed password.
    """
    plain_password = "my_password"
    wrong_password = "wrong_password"
    hashed_password = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    assert verify_password(wrong_password, hashed_password) is False
