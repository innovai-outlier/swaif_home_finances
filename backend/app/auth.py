from __future__ import annotations

import datetime as dt
import hashlib
import secrets

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Member, SessionToken, User
from app.utils import normalize_cpf

# Use an algorithm that doesn't rely on the external `bcrypt` backend.
# This keeps local dev/test stable (notably on newer Python versions)
# while still providing secure password hashing.
_pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return _pwd.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return _pwd.verify(password, password_hash)


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def login(db: Session, cpf: str, password: str) -> str:
    cpf_digits = normalize_cpf(cpf)

    user = db.scalar(select(User).where(User.cpf == cpf_digits))
    if user is None:
        raise ValueError("invalid_credentials")

    if not verify_password(password, user.password_hash):
        raise ValueError("invalid_credentials")

    token = secrets.token_urlsafe(32)
    st = SessionToken(
        id=secrets.token_hex(16),
        user_id=user.id,
        token_hash=_hash_token(token),
        revoked_at=None,
    )
    user.last_login_at = dt.datetime.now(dt.timezone.utc)
    db.add(st)
    db.commit()
    return token


def revoke(db: Session, token: str) -> None:
    token_hash = _hash_token(token)
    st = db.scalar(select(SessionToken).where(SessionToken.token_hash == token_hash))
    if st is None or st.revoked_at is not None:
        return
    st.revoked_at = dt.datetime.now(dt.timezone.utc)
    db.commit()


def get_me(db: Session, token: str) -> tuple[User, Member]:
    token_hash = _hash_token(token)
    st = db.scalar(select(SessionToken).where(SessionToken.token_hash == token_hash))
    if st is None or st.revoked_at is not None:
        raise PermissionError("unauthorized")

    user = db.get(User, st.user_id)
    if user is None:
        raise PermissionError("unauthorized")

    member = db.scalar(select(Member).where(Member.user_id == user.id))
    if member is None:
        raise PermissionError("unauthorized")

    return user, member
