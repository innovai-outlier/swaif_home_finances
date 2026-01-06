import pytest

from app.auth import hash_password, verify_password


def test_password_hash_roundtrip() -> None:
    hashed = hash_password("secret")
    assert verify_password("secret", hashed)
    assert not verify_password("wrong", hashed)


@pytest.mark.parametrize("pwd", ["", "a", "longer_password_123!"])
def test_hash_accepts_various_passwords(pwd: str) -> None:
    hashed = hash_password(pwd)
    assert verify_password(pwd, hashed)
