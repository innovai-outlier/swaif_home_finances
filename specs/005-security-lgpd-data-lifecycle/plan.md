# Plan: Security, LGPD Baseline & Data Lifecycle

## Security controls (v1)
- Password hashing using a modern adaptive algorithm (e.g., argon2/bcrypt).
- TLS termination for all traffic.
- Principle of least privilege for DB credentials.
- Secrets managed via environment variables (no secrets in repo).

## Encryption at rest
- Prefer platform/disk-level encryption for:
  - Postgres data volume
  - backup storage
- Consider field-level encryption for CPF if required by policy.

## Backups
- Automated daily backups (suggested default) with retention (suggested default 30 days).
- Document restore steps and perform periodic restore drills.

## Export
- Export bundle contents:
  - members (with sensitive fields handled per policy)
  - transactions
  - categories
  - debts and payments
  - import templates (optional)
- Export scope:
  - Admin can export family dataset
  - Member can export their own dataset

## Deletion policy (v1 proposal)
- Admin can delete a member (soft-delete first; hard-delete per policy).
- Admin can delete the family (optional; if supported, must cascade appropriately).
- Maintain minimal audit trail that does not retain personal data beyond policy.

## Audit logging
- Log security-relevant events:
  - login attempts
  - exports
  - deletions
  - privilege changes (member additions)

## Sources
- `docs/sources/family-finance/intake.json`
- `docs/sources/family-finance/conversation-summary.md`

