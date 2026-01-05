# Tasks: Debts, Split Expenses & Partial Payments

- [ ] Implement debt and debt payment DB tables
- [ ] Implement split-expense creation logic with custom proportions
- [ ] Build API endpoints for:
  - [ ] create debt(s) from split
  - [ ] list debts (mode-aware)
  - [ ] debt detail
  - [ ] add payment (partial)
- [ ] Implement RBAC enforcement for debt visibility rules
- [ ] Build UI screens:
  - [ ] create split expense (from a transaction or standalone)
  - [ ] debt list (Family-mode and Member-mode)
  - [ ] debt detail + payment history + add payment
- [ ] Add tests:
  - [ ] split math + rounding tests
  - [ ] partial payment balance tests
  - [ ] mode-based visibility tests

## Definition of done
- [ ] Manual split creates correct debts
- [ ] Partial payments work and settle debts accurately
- [ ] Debts respect Family-mode vs Member-mode visibility

## Sources
- `docs/sources/family-finance/intake.json`
- `docs/sources/family-finance/conversation-summary.md`

