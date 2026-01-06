# Plan: Foundation (Auth, Family, Members & RBAC)

## Architecture overview
- **Frontend:** Node.js web app
- **Backend:** Python API service
- **Database:** PostgreSQL
- **Deployment:** Docker (compose or single image for portability)

## Inputs from the spec (non-negotiable)
- Sign-in identifier: **CPF + password**
- Every **Member is also a login User**
- Member-mode for non-admins is **self-only**
- Initial Family + Patriarch exist via **seed**
- CPF validation is **format-only**: `XXX.XXX.XXX-XX` or `XXXXXXXXXXX`
- Member onboarding requires at least one bank account with:
  - `bank_id`, `bank_name`, `bank_agency`, `bank_account_num`, `bank_type` (PF/PJ)

## Traceability (Spec → Plan)
This section maps plan decisions to the feature spec’s requirements and acceptance criteria.

Spec requirements supported:
- FR1 (Auth gate + CPF sign-in): Auth endpoints + session/token approach + CPF normalization/validation.
- FR2 (Single patriarch per family): DB constraints and seed/bootstrap.
- FR3 (Admin-only onboarding + required fields): Member creation flow + validation rules.
- FR4 (View modes): Mode propagated through UI/API requests.
- FR5 (RBAC visibility + Member-mode self-only): Centralized policy + enforced filtering.

Acceptance criteria supported:
- AC1/AC11: Auth gate + RBAC enforcement happens in the API.
- AC2/AC3: CPF login + seeded Patriarch.
- AC4–AC7: Admin-only member creation, required fields, CPF format validation.
- AC8–AC10: Member-mode self-only and mode-based visibility for transactions/debts.

## Suggested service boundaries
- Web UI (frontend) communicates with Backend API over HTTPS.
- Backend API performs auth, authorization checks, and data access.

## Data model (logical)
Entities:
- Family
- User (login identity)
- Member (profile within a family; 1:1 with User in v1)
- BankAccount (belongs to a Member)

Key relationships/constraints:
- A User belongs to exactly one Family (via its Member).
- A Family has exactly one Patriarch.
- Each Member has >= 1 BankAccount.
- CPF is used for login and must be unambiguous.

## Data storage (high-level)
Tables (indicative):
- families(id, name, created_at)
- users(id, cpf, password_hash, created_at, last_login_at)
- members(id, family_id, user_id, name, cpf, birth_date, role, created_at)
- bank_accounts(id, member_id, bank_id, bank_name, bank_agency, bank_account_num, bank_type, created_at)

Notes:
- Keep CPF formatting normalization consistent (store canonical form) while accepting both formats on input.
- Role is part of the Member (patriarch/admin vs member/user).

## RBAC enforcement
- Backend must compute effective permissions using:
  - the authenticated user’s family_id and role
  - requested "mode" (member or family)
  - selected member_id (for member-mode)
- Every list/detail endpoint must be filtered by these rules (never rely on UI-only hiding).

Member-mode self-only rule:
- If role is Member (non-admin), the effective selected member_id must be forced to the user’s own member_id.

Authorization decision points (recommended):
- A centralized policy function that takes: requester_role, mode, requester_member_id, selected_member_id, resource_kind
- Apply it on every request that returns family-scoped data.

## Key flows
### F1 — Sign-in (CPF + password)
- Input: CPF + password.
- Output: authenticated context that includes: user_id, member_id, role, family_id.
- Enforcement: all family-scoped actions require the authenticated context.

### F2 — Seed/bootstrap
- Seed creates one Family and one Patriarch (User + Member) for initial access.
- Seeded credentials must allow sign-in immediately to complete onboarding.

### F3 — Admin onboards a new Member
- Only Patriarch can create a Member.
- Required fields: name, CPF, birth date, and >= 1 bank account.
- Bank account required fields: `bank_id`, `bank_name`, `bank_agency`, `bank_account_num`, `bank_type`.
- Result: a new Member/User exists and can sign in using CPF + password.

### F4 — Mode switching and visibility
- Family-mode: show all Members’ transactions and all Members’ debts.
- Member-mode:
  - Non-admin: selected member is always self.
  - Visibility limited to selected member’s transactions and debts relevant to selected member.

## Privacy & sensitive fields
- Treat CPF and birth date as sensitive.
- Minimize exposure: only show these fields where required (e.g., Admin-only screens).

## Seed/bootstrap
- Provide seed data to create:
  - One Family
  - One Patriarch User + Member mapped to that Family
- Seeded Patriarch credentials must allow immediate sign-in for initial setup.

## API contracts (high-level)
Auth:
- Login (CPF + password) → authenticated session/token
- Logout → session/token invalidation
- WhoAmI/Me → returns user identity, member_id, role, family_id

Members:
- Create Member (Admin-only): name, CPF, birth date, >=1 bank account (with required fields)
- List Members (family-scoped): sufficient for mode selection; must not allow non-admins to pivot to other Members in Member-mode

Bank accounts:
- Captured during member onboarding; exposure governed by RBAC and “need to know”

## Docker & configuration
- Parameterize secrets/config via environment variables:
  - DB connection string
  - app secret(s)
- Provide local dev compose file (optional) for Postgres + app.

## Validation strategy
The validation approach must be sufficient to demonstrate every acceptance criterion.

Recommended checks:
- Auth gate (AC1): verify all family-scoped endpoints reject unauthenticated access.
- CPF sign-in (AC2): verify CPF + password login works.
- Seeded patriarch (AC3): verify seed creates a usable Patriarch account.
- Admin-only onboarding (AC4/AC7): verify non-admin cannot create/modify/remove Members.
- Required fields (AC5/AC9): verify member onboarding fails when required fields are missing.
- CPF format (AC6): verify only the two accepted CPF formats pass validation.
- Member-mode self-only (AC8): verify non-admin cannot select another Member in Member-mode.
- Mode visibility (AC9/AC10): verify Family-mode vs Member-mode visibility for transactions/debts.
- No bypass (AC11): repeat a subset of the above via direct API calls (not only UI).

## Risks / tradeoffs
- **RBAC correctness risk:** a single missed filter could expose family data → centralize policy and require tests.
- **CPF handling tradeoff:** accepting two input formats implies normalization; inconsistent normalization can cause duplicate-user ambiguity.
- **Sensitive data exposure risk:** CPF/birth date should be minimized in API payloads; ensure only required screens/roles can view.
- **Member-mode self-only constraint:** simplifies privacy but reduces flexibility; must be enforced server-side to prevent “selected member” tampering.

## Sources
- [docs/sources/conversation-summary.md](docs/sources/conversation-summary.md)
- [docs/sources/intake.json](docs/sources/intake.json)

