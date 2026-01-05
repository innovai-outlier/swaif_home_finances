# 001 — Foundation: Auth, Family, Members & RBAC

## Summary
Establish the foundational identity and authorization model for the Family Financial Management product: a single family with two roles (Patriarch/Admin and Member/User), Admin-only member onboarding, and strict visibility rules for transactions and debts across **Member-mode** and **Family-mode**.

This feature defines *what* must exist and *how it must behave*; it does not prescribe implementation.

## Goals
- Users can authenticate using **CPF + password**.
- A single Family can be operated with two roles (Patriarch/Admin and Member/User).
- Only the Patriarch can onboard new Members.
- Access to transactions and debts is consistently restricted by **role** and **view mode**.

## Non-goals (v1)
- MFA / 2FA.
- Multi-family membership per user.
- Category management, CSV import, audit workflow, debt creation/payment flows, and LGPD lifecycle/security mechanisms (handled in later features).

## Scope
### In scope (v1)
- Authentication with **password-only** (no MFA requirement).
- A single family context with:
  - Exactly one **Patriarch (Admin)**.
  - One or more **Members (Users)**.
- Admin-only member onboarding via UI form capturing:
  - Name
  - CPF
  - Birth date
  - Bank account(s)
- Role-based permissions and view-mode visibility rules for:
  - Transactions
  - Debts

### Out of scope (v1)
- Multi-family membership per user (a user belongs to only one family).
- MFA / 2FA.
- Category management, CSV import, audit, debts lifecycle logic, security/LGPD lifecycle implementation (defined in later features), except where explicitly referenced as cross-feature constraints.

## Personas & roles
### Patriarch (Admin)
- Can add members.
- Can view all family data.

### Member (User)
- Cannot add members.
- Can view transactions and debts according to view-mode rules.

## Definitions
- **User**: An authenticated identity able to sign in.
- **Member**: A person within a family whose finances are tracked; each transaction belongs to exactly one Member. In v1, every Member is also a login User.
- **Bank account**: An account belonging to a Member; a Member may have multiple bank accounts.
- **Member-mode**: A restricted view centered on one Member.
- **Family-mode**: A combined view across all Members.

## Decisions (resolved)
- Every Member is also a login User.
- In Member-mode, non-admin users can select/view **only themselves**.
- Sign-in identifier is **CPF**.
- The initial Patriarch (Admin) and Family are created via **seed**.
- CPF validation checks **format only**: `XXX.XXX.XXX-XX` or `XXXXXXXXXXX`.
- Bank account required fields at onboarding:
  - `bank_id`
  - `bank_name`
  - `bank_agency`
  - `bank_account_num`
  - `bank_type` (PF or PJ)

## Journeys (v1)
### J1 — Patriarch bootstrap (seed)
1) A Family and its Patriarch User/Member exist from seed.
2) Patriarch can sign in using CPF + password.

### J2 — Patriarch onboards a new Member
1) Patriarch signs in.
2) Patriarch creates a new Member with name, CPF, birth date, and at least one bank account.
3) The new Member can sign in using CPF + password.

### J3 — Member switches between Family-mode and Member-mode
1) Member signs in.
2) In Family-mode, Member can view all family transactions and all family debts.
3) In Member-mode, Member can view only their own transactions and only debts relevant to themselves.

## Functional requirements
### FR1 — Sign-in and authenticated access
- The system must support password-based sign-in.
- The system must prevent unauthenticated access to family data.
- The system must support sign-in using CPF + password.
- After sign-in, the system must associate the user with exactly one family (v1 constraint).
- CPF must uniquely identify a login User (no ambiguity when signing in).

### FR2 — Family and Patriarch
- A family must have exactly one Patriarch (Admin) in v1.
- The Patriarch has permissions to manage the family configuration relevant to this feature (member onboarding).

### FR3 — Member onboarding (Admin-only)
- Only the Patriarch can add a Member.
- Creating a Member must require at minimum:
  - Name
  - CPF
  - Birth date
  - At least one bank account
- CPF must be accepted only in formats `XXX.XXX.XXX-XX` or `XXXXXXXXXXX`.
- Each bank account captured at onboarding must include: `bank_id`, `bank_name`, `bank_agency`, `bank_account_num`, `bank_type` (PF or PJ).
- Members (Users) cannot add, modify, or remove Members.

### FR4 — View modes
- The system must provide two view modes: Member-mode and Family-mode.
- The system must apply authorization rules consistently regardless of how the user navigates (UI or API).

### FR5 — Authorization rules for visibility
#### Transactions visibility
- In **Family-mode**, a Member (User) can view transactions for all Members in the family.
- In **Member-mode**, a Member (User) can view transactions only for the selected Member.

#### Member-mode selection constraint
- For non-admin users, the selected Member in Member-mode must be **the user’s own Member**.

#### Debts visibility
- In **Family-mode**, a Member (User) can view debts for all Members in the family.
- In **Member-mode**, a Member (User) can view only debts relevant to the selected Member.

#### Admin visibility
- The Patriarch (Admin) can view all Members’ transactions and debts.

## Acceptance criteria
- AC1 (Auth gate): When not signed in, the user cannot access any family-scoped data.
- AC2 (CPF sign-in): A user can sign in using CPF + password.
- AC3 (Seeded Patriarch): A seeded Family and Patriarch exist and the Patriarch can sign in.
- AC4 (Admin-only onboarding): Patriarch can create a Member with name, CPF, birth date, and at least one bank account.
- AC5 (Member onboarding constraints): Member creation fails if any required field is missing (name, CPF, birth date, or any required bank account field).
- AC6 (CPF format): CPF input accepts `XXX.XXX.XXX-XX` and `XXXXXXXXXXX` and rejects other formats.
- AC7 (Member cannot onboard): A Member cannot add, modify, or remove Members.
- AC8 (Member-mode self-only): In Member-mode, a non-admin user can only view/select their own Member.
- AC9 (Family-mode visibility): In Family-mode, a Member can view all Members’ transactions and all Members’ debts.
- AC10 (Member-mode visibility): In Member-mode, a Member can view only their own transactions and only debts relevant to themselves.
- AC11 (No bypass): The same RBAC behavior holds regardless of how access is attempted (UI or API).

## Edge cases (v1)
- Invalid CPF format is provided on sign-in or member creation.
- A Member attempts to perform Admin-only actions (e.g., create a Member).
- A non-admin user attempts to select/view another Member in Member-mode.
- A Member creation attempt includes zero bank accounts.
- A Member creation attempt includes a bank account missing any required field.

## Validation
- Manual: Verify sign-in required before accessing any family pages/data.
- Manual: Verify Admin-only access to member onboarding UI and that non-admin attempts are blocked.
- Manual: Verify visibility rules in Member-mode vs Family-mode for both transactions and debts.
- Manual: Verify Member-mode for non-admin cannot select other members.
- Manual: Verify CPF and bank account required fields validation on member onboarding.

## Open questions
- None.

## Sources (evidence)
- [docs/sources/conversation-summary.md](docs/sources/conversation-summary.md)
- [docs/sources/intake.json](docs/sources/intake.json)

