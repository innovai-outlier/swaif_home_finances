# Tasks: Foundation (Auth, Family, Members & RBAC)

## Milestone: Foundation usable end-to-end

- [ ] Define DB schema for families, users, members, bank accounts
- [ ] Implement authentication (password hashing, session/JWT, logout)
- [ ] Implement RBAC policy module (Member-mode vs Family-mode)
- [ ] Build Admin UI: add member (name, CPF, birth date, bank accounts)
- [ ] Build Member UI: select mode (Member/Family) and selected member (when in Member-mode)
- [ ] API endpoints:
  - [ ] POST /auth/login, POST /auth/logout
  - [ ] GET /me (current user + role + family_id)
  - [ ] POST /families/{family_id}/members (Admin-only)
  - [ ] GET /families/{family_id}/members (RBAC-aware)
  - [ ] CRUD bank accounts (Admin-only create/update; view per RBAC)
- [ ] Add automated tests:
  - [ ] RBAC matrix tests (mode × role × resource)
  - [ ] Sensitive field exposure tests (CPF/birth date)
- [ ] Dockerize services (frontend, backend, postgres for dev)

## Definition of done
- [ ] A Patriarch can add members and see them listed
- [ ] A Member cannot add members
- [ ] Mode switching affects accessible data as specified
- [ ] RBAC is enforced at API level and covered by tests

## Sources
- `docs/sources/family-finance/intake.json`
- `docs/sources/family-finance/conversation-summary.md`

