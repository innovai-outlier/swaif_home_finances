from __future__ import annotations

import secrets

from fastapi import Depends, FastAPI, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import auth, rbac, seed
from app.db import Base, SessionLocal, engine, get_db
from app.models import BankAccount, Member, MemberRole, User
from app.schemas import (
    CreateMemberRequest,
    CreateMemberResponse,
    LoginRequest,
    LoginResponse,
    MeResponse,
    MemberOut,
)
from app.utils import normalize_cpf

app = FastAPI(title="SWAIF Home Finances API")


@app.on_event("startup")
def _startup() -> None:
    # Minimal bootstrap: create tables for local/dev. Alembic should be used for real migrations.
    Base.metadata.create_all(bind=engine)

    # Seed the initial Family + Patriarch (idempotent).
    db = SessionLocal()
    try:
        seed.ensure_seeded(db)
    finally:
        db.close()


def _get_token(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="unauthorized")
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="unauthorized")
    return authorization.split(" ", 1)[1].strip()


def get_auth_context(
    db: Session = Depends(get_db), authorization: str | None = Header(default=None)
) -> tuple[str, rbac.AuthContext]:
    token = _get_token(authorization)
    _user, member = auth.get_me(db, token)
    ctx = rbac.AuthContext(
        family_id=member.family_id,
        role="patriarch" if member.role == MemberRole.patriarch else "member",
        requester_member_id=member.id,
    )
    return token, ctx


@app.post("/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    try:
        token = auth.login(db, payload.cpf, payload.password)
    except ValueError:
        raise HTTPException(status_code=401, detail="invalid_credentials")
    return LoginResponse(token=token)


@app.post("/auth/logout", status_code=204)
def logout(
    db: Session = Depends(get_db), authorization: str | None = Header(default=None)
) -> None:
    token = _get_token(authorization)
    auth.revoke(db, token)


@app.get("/me", response_model=MeResponse)
def me(
    db: Session = Depends(get_db), authorization: str | None = Header(default=None)
) -> MeResponse:
    token = _get_token(authorization)
    _user, member = auth.get_me(db, token)
    return MeResponse(
        user_id=member.user_id,
        member_id=member.id,
        family_id=member.family_id,
        role="patriarch" if member.role == MemberRole.patriarch else "member",
    )


@app.post("/members", response_model=CreateMemberResponse)
def create_member(
    payload: CreateMemberRequest,
    db: Session = Depends(get_db),
    auth_ctx: tuple[str, rbac.AuthContext] = Depends(get_auth_context),
) -> CreateMemberResponse:
    _token, ctx = auth_ctx
    if ctx.role != "patriarch":
        raise HTTPException(status_code=403, detail="forbidden")

    cpf_digits = normalize_cpf(payload.cpf)

    initial_password = secrets.token_urlsafe(12)
    user = User(id=secrets.token_hex(16), cpf=cpf_digits, password_hash=auth.hash_password(initial_password))
    member = Member(
        id=secrets.token_hex(16),
        family_id=ctx.family_id,
        user_id=user.id,
        name=payload.name,
        cpf=cpf_digits,
        birth_date=payload.birth_date,
        role=MemberRole.member,
    )

    accounts = [
        BankAccount(
            id=secrets.token_hex(16),
            member_id=member.id,
            bank_id=a.bank_id,
            bank_name=a.bank_name,
            bank_agency=a.bank_agency,
            bank_account_num=a.bank_account_num,
            bank_type=a.bank_type,
        )
        for a in payload.bank_accounts
    ]

    db.add_all([user, member, *accounts])
    db.commit()

    return CreateMemberResponse(
        member=MemberOut(
            id=member.id,
            family_id=member.family_id,
            user_id=member.user_id,
            name=member.name,
            cpf=member.cpf,
            birth_date=member.birth_date,
            role="member",
        ),
        initial_password=initial_password,
    )


@app.get("/members", response_model=list[MemberOut])
def list_members(
    mode: rbac.Mode = "family",
    db: Session = Depends(get_db),
    auth_ctx: tuple[str, rbac.AuthContext] = Depends(get_auth_context),
) -> list[MemberOut]:
    _token, ctx = auth_ctx
    if not rbac.can_list_members(context=ctx, mode=mode):
        raise HTTPException(status_code=403, detail="forbidden")

    stmt = select(Member).where(Member.family_id == ctx.family_id)
    filters = rbac.member_list_filter(context=ctx, mode=mode)
    if "member_id" in filters:
        stmt = stmt.where(Member.id == filters["member_id"])

    members = db.scalars(stmt).all()
    return [
        MemberOut(
            id=m.id,
            family_id=m.family_id,
            user_id=m.user_id,
            name=m.name,
            cpf=m.cpf,
            birth_date=m.birth_date,
            role="patriarch" if m.role == MemberRole.patriarch else "member",
        )
        for m in members
    ]
