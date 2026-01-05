# Plan: Transactions, Categories & Views

## Canonical transaction schema (v1)
Required fields:
- occurred_at (date/time)
- amount (signed or separate direction)
- direction (INCOME | EXPENSE)
- description
- member_id
Optional:
- bank_account_id
- external_id (from bank)
- currency (default BRL)
- category_id
- notes/tags

## DB considerations
- Store amounts as integer minor units (e.g., centavos) to avoid floating point errors.
- Indexes:
  - (family_id, occurred_at)
  - (member_id, occurred_at)
  - (category_id, occurred_at)

## Category model
- Admin-managed list per family.
- Consider seeding default categories on family creation, then allow Admin to adjust.

## API design (indicative)
- GET /transactions?mode=member&member_id=...&from=...&to=...
- GET /transactions?mode=family&from=...&to=...
- GET /categories
- POST /categories (Admin-only)
- PATCH /categories/{id} (Admin-only)

## UI approach
- Primary toggle: Member-mode vs Family-mode.
- Member-mode includes member selector (restricted to members within the family).
- Transaction list with filters and totals; allow drill-down.

## Sources
- `docs/sources/family-finance/intake.json`
- `docs/sources/family-finance/conversation-summary.md`

