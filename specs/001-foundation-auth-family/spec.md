# Foundation: Auth, Family, Members & RBAC

## Goal
Enable a family to be created and managed with two roles (Patriarch/Admin and Member/User), enforcing visibility rules for transactions and debts across Member-mode and Family-mode.

## Non-goals (v1)
- Multi-family membership per user (single-family membership only)
- 2FA requirements (password-only in v1)

## Personas
- **Patriarch (Admin):** creates and manages the family, adds members, defines categories.
- **Member (User):** manages and views finances according to RBAC.

## Core requirements
### Authentication
- Support username/email + password authentication.
- Session management must prevent unauthorized access to family data.

### Authorization (RBAC)
- **Member-mode**
  - A user can view transactions only for the selected member.
  - Debts visibility is limited to those relevant to that member.
- **Family-mode**
  - A user can view all members’ transactions.
  - A user can view all members’ debts.

### Family and member management
- A family has exactly one Patriarch (Admin) in v1.
- Only the Patriarch can add members via UI with:
  - name
  - CPF
  - birth date
  - bank account(s)
- Members cannot add other members.

## Data model (conceptual)
- Family
- User (auth identity)
- Member (profile within a family; linked to a User)
- BankAccount (belongs to a Member)

## Acceptance criteria
- Admin can add a member with the required fields.
- Members cannot add or modify members.
- RBAC rules for Member-mode and Family-mode are enforced consistently across UI and API.

## Sources
- `docs/sources/family-finance/intake.json`
- `docs/sources/family-finance/conversation-summary.md`

