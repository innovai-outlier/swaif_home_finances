# Tasks: CSV Import, Templates & Audit

- [ ] Implement CSV upload and parsing
- [ ] Implement mapping UI (de-para)
- [ ] Persist ImportTemplate (create/select/update)
- [ ] Create ImportBatch and ImportRow storage
- [ ] Implement validation and per-row error reporting
- [ ] Build audit UI
  - [ ] inline edit
  - [ ] delete row
  - [ ] category assignment
  - [ ] invalid/uncategorized filters
- [ ] Implement commit flow (batch status transition)
- [ ] Add duplicate-flagging (heuristic) during audit (optional but recommended)
- [ ] Add tests
  - [ ] mapping + validation tests
  - [ ] commit gating tests

## Definition of done
- [ ] A user can import a new CSV format, map columns, save a template, and reuse it
- [ ] Audit supports edit/delete/categorize and only committed data appears in transaction views
- [ ] Validation errors are actionable and block commit until resolved

## Sources
- `docs/sources/family-finance/intake.json`
- `docs/sources/family-finance/conversation-summary.md`

