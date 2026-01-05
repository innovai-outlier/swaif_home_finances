# Tasks: Foundation (Auth, Family, Members & RBAC)

## Milestone: Foundation usable end-to-end

- [ ] DB: define tables and relationships (Family, User, Member, BankAccount) (AC3, AC4, AC5, AC9)
- [ ] DB: add constraints for “one Patriarch per family” and “Member has >=1 bank account” (AC3, AC4, AC5)
- [ ] DB: decide CPF canonical storage format + uniqueness constraint (AC2, AC6)

- [ ] Seed: create initial Family record (AC3)
- [ ] Seed: create initial Patriarch User + Member + bank account(s) (AC3)
- [ ] Seed: document the seeded Patriarch credentials for local/dev validation (AC3)

- [ ] Auth: implement CPF+password login endpoint (AC1, AC2)
- [ ] Auth: implement logout endpoint (AC1)
- [ ] Auth: implement whoami/me endpoint returning user_id, member_id, role, family_id (AC1, AC11)
- [ ] Auth: add CPF input validation (format-only) at auth boundary (AC6)

- [ ] RBAC: implement centralized policy for role × mode × resource decisions (AC9, AC10, AC11)
- [ ] RBAC: enforce Family-mode visibility filtering on relevant endpoints (AC9, AC11)
- [ ] RBAC: enforce Member-mode filtering on relevant endpoints (AC10, AC11)
- [ ] RBAC: enforce Member-mode self-only for non-admins (AC8, AC11)

- [ ] Members API: Admin-only create Member (name, CPF, birth date, >=1 bank account) (AC4, AC5, AC7)
- [ ] Members API: enforce CPF format-only validation on create Member input (AC6)
- [ ] Members API: implement list Members for authenticated family (AC9, AC11)
- [ ] Members API: ensure list/selection does not enable non-admin Member-mode pivot (AC8, AC11)

- [ ] UI: implement CPF sign-in screen + basic failure states (AC2)
- [ ] UI: implement Admin add-member form fields (including bank account required fields) (AC4, AC5)
- [ ] UI: implement CPF format validation feedback on inputs (AC6)
- [ ] UI: implement view mode switch (Family-mode vs Member-mode) (AC9, AC10)
- [ ] UI: enforce Member-mode self-only UX for non-admins (AC8)

- [ ] Tests: auth gate (unauthenticated access denied) (AC1)
- [ ] Tests: seeded Patriarch can sign in (AC2, AC3)
- [ ] Tests: CPF format acceptance/rejection (AC6)
- [ ] Tests: Admin-only member creation (AC4, AC7)
- [ ] Tests: member creation required fields + >=1 bank account (AC5)
- [ ] Tests: RBAC visibility matrix for Family-mode vs Member-mode (AC9, AC10, AC11)
- [ ] Tests: Member-mode self-only constraint (AC8, AC11)

- [ ] Manual validation: run the happy-path journeys J1–J3 from the spec (AC1–AC11)
- [ ] Dev validation: Docker/dev setup runs frontend, backend, and Postgres

## Definition of done
- [ ] A seeded Patriarch can sign in using CPF + password
- [ ] A Patriarch can add Members with required fields (including >=1 bank account)
- [ ] A Member cannot add/modify/remove Members
- [ ] Member-mode is self-only for non-admins
- [ ] Family-mode vs Member-mode visibility matches the spec
- [ ] RBAC is enforced at API level and covered by tests

## Sources
- [docs/sources/conversation-summary.md](docs/sources/conversation-summary.md)
- [docs/sources/intake.json](docs/sources/intake.json)

