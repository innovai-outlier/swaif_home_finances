from __future__ import annotations

import datetime as dt
from typing import Literal

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    cpf: str
    password: str


class LoginResponse(BaseModel):
    token: str


class MeResponse(BaseModel):
    user_id: str
    member_id: str
    family_id: str
    role: Literal["patriarch", "member"]


class BankAccountIn(BaseModel):
    bank_id: str
    bank_name: str
    bank_agency: str
    bank_account_num: str
    bank_type: Literal["PF", "PJ"]


class CreateMemberRequest(BaseModel):
    name: str
    cpf: str
    birth_date: dt.date
    bank_accounts: list[BankAccountIn] = Field(..., min_items=1)


class MemberOut(BaseModel):
    id: str
    family_id: str
    user_id: str
    name: str
    cpf: str
    birth_date: dt.date
    role: Literal["patriarch", "member"]


class CreateMemberResponse(BaseModel):
    member: MemberOut
    initial_password: str
