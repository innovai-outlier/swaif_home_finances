from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


Mode = Literal["family", "member"]
Role = Literal["patriarch", "member"]
ResourceKind = Literal["members", "transactions", "debts"]


@dataclass(frozen=True)
class AuthContext:
    family_id: str
    role: Role
    requester_member_id: str


def effective_selected_member_id(
    *, context: AuthContext, mode: Mode, selected_member_id: str | None
) -> str | None:
    if mode == "member" and context.role == "member":
        return context.requester_member_id
    return selected_member_id


def can_list_members(*, context: AuthContext, mode: Mode) -> bool:
    # Listing members is needed for Family-mode visibility; in Member-mode self-only is enforced by
    # response filtering.
    return True


def member_list_filter(*, context: AuthContext, mode: Mode) -> dict:
    # Returns SQL filter constraints to apply.
    if mode == "member" and context.role == "member":
        return {"member_id": context.requester_member_id}
    return {}
