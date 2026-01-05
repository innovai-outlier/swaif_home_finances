# Tasks: Security, LGPD Baseline & Data Lifecycle

- [ ] Implement password hashing and secure auth configuration
- [ ] Enforce TLS (deployment configuration)
- [ ] Implement encryption-at-rest strategy for DB volume and backups
- [ ] Implement automated backup job + retention
- [ ] Write and test restore procedure
- [ ] Implement export:
  - [ ] Admin family export
  - [ ] Member self export
- [ ] Implement deletion flows:
  - [ ] member deletion
  - [ ] family deletion (if included)
  - [ ] delete related import artifacts per policy
- [ ] Implement audit logging for security-relevant actions
- [ ] Add tests:
  - [ ] authorization for export/delete
  - [ ] export completeness checks
  - [ ] deletion cascade checks

## Definition of done
- [ ] Encryption at rest + backups are operational
- [ ] Export works with correct RBAC scoping
- [ ] Deletion flows work and are audited

## Sources
- `docs/sources/family-finance/intake.json`
- `docs/sources/family-finance/conversation-summary.md`

