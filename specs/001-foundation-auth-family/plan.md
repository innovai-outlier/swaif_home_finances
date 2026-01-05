# Plan: Foundation (Auth, Family, Members & RBAC)

## Architecture overview
- **Frontend:** Node.js web app
- **Backend:** Python API service
- **Database:** PostgreSQL
- **Deployment:** Docker (compose or single image for portability)

## Suggested service boundaries
- Web UI (frontend) communicates with Backend API over HTTPS.
- Backend API performs auth, authorization checks, and data access.

## Data storage (high-level)
Tables (indicative):
- families(id, name, created_at)
- users(id, email_or_username, password_hash, created_at, last_login_at)
- family_members(id, family_id, user_id, name, cpf, birth_date, role, created_at)
- bank_accounts(id, member_id, label, bank_name, account_identifier_last4, created_at)

## RBAC enforcement
- Backend must compute effective permissions using:
  - the authenticated user’s family_id and role
  - requested "mode" (member or family)
  - selected member_id (for member-mode)
- Every list/detail endpoint must be filtered by these rules (never rely on UI-only hiding).

## Privacy & sensitive fields
- Treat CPF and birth date as sensitive.
- Minimize exposure: only show these fields where required (e.g., Admin-only screens).

## Docker & configuration
- Parameterize secrets/config via environment variables:
  - DB connection string
  - app secret(s)
- Provide local dev compose file (optional) for Postgres + app.

## Risks / mitigations
- Incorrect RBAC filtering could expose data → implement authorization tests per endpoint.
- Member identity linking (User ↔ Member) must be consistent → enforce constraints at DB level.

## Sources
- `docs/sources/family-finance/intake.json`
- `docs/sources/family-finance/conversation-summary.md`

