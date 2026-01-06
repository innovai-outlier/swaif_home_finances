"""init

Revision ID: 0001_init
Revises: 
Create Date: 2026-01-06

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "families",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "users",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("cpf", sa.String(length=11), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_users_cpf", "users", ["cpf"], unique=True)

    op.execute("CREATE TYPE member_role AS ENUM ('patriarch', 'member')")

    op.create_table(
        "members",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("family_id", sa.String(), sa.ForeignKey("families.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.String(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("cpf", sa.String(length=11), nullable=False),
        sa.Column("birth_date", sa.Date(), nullable=False),
        sa.Column("role", sa.Enum(name="member_role"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("user_id", name="uq_members_user_id"),
        sa.UniqueConstraint("family_id", "cpf", name="uq_members_family_cpf"),
    )
    op.create_index("ix_members_family_id", "members", ["family_id"], unique=False)
    op.create_index("ix_members_cpf", "members", ["cpf"], unique=False)

    # One Patriarch per family (partial unique index).
    op.execute(
        "CREATE UNIQUE INDEX uq_members_one_patriarch_per_family ON members (family_id) WHERE role = 'patriarch'"
    )

    op.create_table(
        "bank_accounts",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("member_id", sa.String(), sa.ForeignKey("members.id", ondelete="CASCADE"), nullable=False),
        sa.Column("bank_id", sa.String(), nullable=False),
        sa.Column("bank_name", sa.String(), nullable=False),
        sa.Column("bank_agency", sa.String(), nullable=False),
        sa.Column("bank_account_num", sa.String(), nullable=False),
        sa.Column("bank_type", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_bank_accounts_member_id", "bank_accounts", ["member_id"], unique=False)

    # Deferrable constraint trigger: each member must have >= 1 bank account by transaction commit.
    op.execute(
        """
        CREATE OR REPLACE FUNCTION check_member_has_bank_account() RETURNS TRIGGER AS $$
        BEGIN
          IF NOT EXISTS (SELECT 1 FROM bank_accounts WHERE member_id = NEW.id) THEN
            RAISE EXCEPTION 'member_must_have_bank_account';
          END IF;
          RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE CONSTRAINT TRIGGER trg_member_has_bank_account
        AFTER INSERT OR UPDATE ON members
        DEFERRABLE INITIALLY DEFERRED
        FOR EACH ROW
        EXECUTE FUNCTION check_member_has_bank_account();
        """
    )

    op.create_table(
        "session_tokens",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("user_id", sa.String(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("token_hash", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_session_tokens_user_id", "session_tokens", ["user_id"], unique=False)
    op.create_index("ix_session_tokens_token_hash", "session_tokens", ["token_hash"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_session_tokens_token_hash", table_name="session_tokens")
    op.drop_index("ix_session_tokens_user_id", table_name="session_tokens")
    op.drop_table("session_tokens")

    op.execute("DROP TRIGGER IF EXISTS trg_member_has_bank_account ON members")
    op.execute("DROP FUNCTION IF EXISTS check_member_has_bank_account")

    op.drop_index("ix_bank_accounts_member_id", table_name="bank_accounts")
    op.drop_table("bank_accounts")

    op.execute("DROP INDEX IF EXISTS uq_members_one_patriarch_per_family")
    op.drop_index("ix_members_cpf", table_name="members")
    op.drop_index("ix_members_family_id", table_name="members")
    op.drop_table("members")

    op.execute("DROP TYPE IF EXISTS member_role")

    op.drop_index("ix_users_cpf", table_name="users")
    op.drop_table("users")

    op.drop_table("families")
