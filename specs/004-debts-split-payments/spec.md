# Debts: Split Expenses & Partial Payments

## Goal
Support manual splitting of shared costs that were paid by one member, creating debts among members and enabling partial payments until settled.

## Core requirements
### Create split expense
- User selects (or references) an expense and defines participants and proportions (customizable X).
- System creates debt entries so owing members know how much to transfer to the payer.
- Split is **manual** (explicit action per debt/split).

### Debt visibility rules
- **Family-mode:** members can view all members’ debts.
- **Member-mode:** members can view only debts relevant to the selected member.

### Partial payments
- A debt supports multiple payments (partial).
- Remaining balance is computed from total - sum(payments).
- Debt reaches "Settled" when remaining balance is zero.

## Data model (conceptual)
- Debt(id, family_id, payer_member_id, owing_member_id, total_amount, currency, status, created_at, updated_at, reference_transaction_id?)
- DebtPayment(id, debt_id, paid_by_member_id, amount, paid_at, note?)

## Acceptance criteria
- Creating a split produces correct per-member debt amounts based on proportions.
- Partial payments reduce the outstanding balance correctly.
- Debts appear correctly in Family-mode and Member-mode according to RBAC rules.

## Sources
- `docs/sources/family-finance/intake.json`
- `docs/sources/family-finance/conversation-summary.md`

