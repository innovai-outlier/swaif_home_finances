# Plan: Debts & Payments

## Split calculation (v1)
- Inputs:
  - total expense amount
  - payer_member_id
  - participant list with proportions (percentages or weights)
- Output:
  - For each participant other than payer:
    - debt_amount = participant_share
- Rounding:
  - Use minor units; allocate rounding remainder deterministically (e.g., to largest share).

## Linking to transactions
- Recommended: allow referencing an existing expense transaction as the "source".
- Store reference_transaction_id when available; otherwise allow standalone debt.

## API design (indicative)
- POST /debts (create split)
- GET /debts?mode=member&member_id=...
- GET /debts?mode=family
- POST /debts/{debt_id}/payments
- GET /debts/{debt_id} (details incl. payment history)
- PATCH /debts/{debt_id} (optional: note/status)

## UI approach
- Debt ledger list with:
  - who owes whom
  - outstanding balance
  - status
- Debt detail with payment history and "add payment" action.

## Sources
- `docs/sources/family-finance/intake.json`
- `docs/sources/family-finance/conversation-summary.md`

