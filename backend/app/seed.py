from __future__ import annotations

import datetime as dt
import secrets

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import hash_password
from app.models import BankAccount, Family, Member, MemberRole, User
from app.settings import settings
from app.utils import normalize_cpf


def ensure_seeded(db: Session) -> None:
    cpf_digits = normalize_cpf(settings.seed_patriarch_cpf)

    user = db.scalar(select(User).where(User.cpf == cpf_digits))
    if user is not None:
        return

    family = Family(id=secrets.token_hex(16), name="Default Family")
    user = User(id=secrets.token_hex(16), cpf=cpf_digits, password_hash=hash_password(settings.seed_patriarch_password))
    member = Member(
        id=secrets.token_hex(16),
        family_id=family.id,
        user_id=user.id,
        name="Patriarch",
        cpf=cpf_digits,
        birth_date=dt.date(1970, 1, 1),
        role=MemberRole.patriarch,
    )

    bank_account = BankAccount(
        id=secrets.token_hex(16),
        member_id=member.id,
        bank_id="000",
        bank_name="Seed Bank",
        bank_agency="0001",
        bank_account_num="000000-0",
        bank_type="PF",
    )

    db.add_all([family, user, member, bank_account])
    db.commit()
