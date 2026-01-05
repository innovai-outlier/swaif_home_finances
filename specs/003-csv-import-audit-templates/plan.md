# Plan: CSV Import, Templates & Audit

## Canonical mapping
- Provide a mapping UI that binds:
  - source column → canonical field
  - optional transforms (date parsing, decimal separator, sign handling)
- Store mapping rules in ImportTemplate.mapping_rules (JSON).

## Validation strategy (v1)
- Structural validation:
  - CSV parseable
  - required canonical fields mapped
- Row validation:
  - date parseable
  - amount parseable
  - description non-empty
- Provide per-row error messages and allow the user to fix or delete rows.

## Audit UX
- A table/grid view of imported rows with:
  - inline editing
  - delete row
  - bulk category assignment (optional)
  - filters: invalid only / uncategorized only
- Commit action is disabled until:
  - no required-field errors remain

## Duplicate handling (recommended)
- Flag potential duplicates within the batch and against existing transactions using heuristics:
  - same date (±1 day), same amount, similar description, same member
- Do not auto-delete; user decides during audit.

## API design (indicative)
- POST /imports (upload + parse → returns batch_id)
- GET /imports/{batch_id}
- PATCH /imports/{batch_id}/rows/{row_id} (edit)
- DELETE /imports/{batch_id}/rows/{row_id}
- POST /imports/{batch_id}/commit
- CRUD /import-templates

## Sources
- `docs/sources/family-finance/intake.json`
- `docs/sources/family-finance/conversation-summary.md`

