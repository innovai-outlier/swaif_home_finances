# Security, LGPD Baseline & Data Lifecycle

## Goal
Implement a baseline of security and data lifecycle controls suitable for handling personal and financial data, aligned with LGPD expectations.

## Core requirements
### Encryption at rest
- Persist data in encrypted storage at rest (database storage volume and backups).

### Backups
- Automated backups with defined retention policy (v1: choose a default; configurable later).
- Regular restore testing process documented.

### Data export
- Provide export for a user/family dataset in a common format (e.g., JSON/CSV bundle).

### Data deletion
- Support deletion requests according to policy:
  - user/member deletion (where allowed)
  - family deletion by Admin (if supported)
- Ensure deletion affects:
  - member profile data
  - transactions
  - debts/payments
  - import artifacts (batches/templates) as policy dictates

### Password-only v1
- No 2FA requirement in v1, but password storage must follow best practices.

## Acceptance criteria
- Encryption at rest is enabled for DB storage and backups.
- Backup jobs run automatically and restore procedure is documented.
- Export endpoint produces a complete, consistent snapshot of user/family data within RBAC constraints.
- Deletion flows remove data according to policy and are audited.

## Sources
- `docs/sources/family-finance/intake.json`
- `docs/sources/family-finance/conversation-summary.md`

