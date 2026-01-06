from app.rbac import AuthContext, effective_selected_member_id, member_list_filter


def test_member_mode_self_only_overrides_selected_member() -> None:
    ctx = AuthContext(family_id="f1", role="member", requester_member_id="m_self")
    assert (
        effective_selected_member_id(context=ctx, mode="member", selected_member_id="m_other")
        == "m_self"
    )


def test_family_mode_keeps_selected_member_id() -> None:
    ctx = AuthContext(family_id="f1", role="member", requester_member_id="m_self")
    assert (
        effective_selected_member_id(context=ctx, mode="family", selected_member_id="m_other")
        == "m_other"
    )


def test_member_list_filter_member_mode_self_only() -> None:
    ctx = AuthContext(family_id="f1", role="member", requester_member_id="m_self")
    assert member_list_filter(context=ctx, mode="member") == {"member_id": "m_self"}


def test_member_list_filter_family_mode_all() -> None:
    ctx = AuthContext(family_id="f1", role="member", requester_member_id="m_self")
    assert member_list_filter(context=ctx, mode="family") == {}
