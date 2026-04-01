from app.auth.password import get_password_hash, verify_password
from app.auth.tokens import create_access_token, decode_token


def test_password_hashing_and_verification() -> None:
    password = "super-secret-password"
    hashed = get_password_hash(password)

    assert hashed != password
    assert verify_password(password, hashed) is True


def test_access_token_contains_user_subject() -> None:
    token = create_access_token(subject="42")
    payload = decode_token(token)

    assert payload["sub"] == "42"
