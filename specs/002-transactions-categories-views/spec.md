# Transactions, Categories & Views

## Goal
Enable recording and viewing of per-member financial transactions (income/expense) with budget categories, supporting Member-mode and Family-mode views under RBAC.

## Non-goals (v1)
- Automated forecasting or budgeting recommendations
- Investment tracking

## Core requirements
### Transactions
- Transactions represent income or expense.
- Each transaction belongs to **exactly one member**.
- Transactions may be created via:
  - CSV import (see CSV feature)
  - Manual creation/editing during audit (and optionally direct manual entry if added later)

### Categories
- Categories are defined by the Patriarch (Admin).
- Members cannot edit category definitions.
- Transactions can be assigned exactly one category (v1).

### Views
- **Member-mode:** show selected member’s transactions and summaries.
- **Family-mode:** show all members’ transactions and summaries.
- Support filtering and sorting by:
  - date range
  - category
  - amount range (optional)
  - free-text search on description (optional)

## Data model (conceptual)
- Transaction(id, member_id, bank_account_id?, occurred_at, amount, direction, description, category_id, source, created_at, updated_at)
- Category(id, family_id, name, parent_id?, active)

## Acceptance criteria
- Admin can define categories and members can assign them to transactions (where permitted by the workflow).
- Transactions appear correctly in Member-mode and Family-mode according to RBAC rules.
- Basic filters (date range + category) produce correct results.

## Sources
- `docs/sources/family-finance/intake.json`
- `docs/sources/family-finance/conversation-summary.md`

