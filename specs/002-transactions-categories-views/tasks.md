# Tasks: Transactions, Categories & Views

- [ ] Implement category management (Admin-only)
  - [ ] Create/list/update/disable categories per family
  - [ ] Seed default categories for new families (optional)
- [ ] Implement transaction storage + retrieval
  - [ ] Canonical transaction model
  - [ ] List endpoints with filtering (date range, category)
- [ ] Implement UI screens
  - [ ] Categories management (Admin)
  - [ ] Transactions list + filters (Member-mode and Family-mode)
  - [ ] Transaction detail view (read-only in this feature; edits handled in audit feature)
- [ ] Add RBAC enforcement for transaction and category endpoints
- [ ] Add tests
  - [ ] Filtering correctness tests
  - [ ] Mode-based visibility tests

## Definition of done
- [ ] Categories are Admin-defined and used in transaction display and summaries
- [ ] Member-mode and Family-mode lists match RBAC requirements
- [ ] Filters work and are tested

## Sources
- `docs/sources/family-finance/intake.json`
- `docs/sources/family-finance/conversation-summary.md`

