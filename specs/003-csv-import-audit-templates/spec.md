# CSV Import, Mapping Templates & Audit

## Goal
Allow importing transactions from CSV exports (primarily banks), validating the schema, mapping fields to a canonical format, and auditing imported records before committing them to the ledger.

## Core requirements
### Import flow
1. User uploads CSV
2. System detects known template (if available) or starts "from zero"
3. User maps source columns to canonical fields (de-para)
4. System validates:
   - required fields are present/mapped
   - data types and formats
   - basic personal-data checks as required
5. System creates an **import batch** in "Needs Audit" state
6. User audits imported transactions:
   - edit fields as needed
   - delete incorrect rows
   - assign categories
7. User commits the batch, making transactions visible in standard views

### Template learning
- If importing from zero, user can save mappings as a reusable **bank template**.
- Templates are scoped to a family.

### Audit requirements
- Audit must support edit/delete and category assignment before commit.
- The audit step is the gate to data consistency.

## Data model (conceptual)
- ImportTemplate(id, family_id, name, mapping_rules, created_at)
- ImportBatch(id, family_id, created_by_member_id, template_id?, status, created_at, committed_at?)
- ImportRow(id, import_batch_id, raw_data, parsed_data, status, validation_errors?)

## Acceptance criteria
- CSV import rejects files without required mapped fields.
- A user can save a mapping template and reuse it for a later import.
- Audit UI supports edit/delete/categorize and only committed batches affect standard transaction views.

## Sources
- `docs/sources/family-finance/intake.json`
- `docs/sources/family-finance/conversation-summary.md`

