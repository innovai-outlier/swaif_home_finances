# Source: Conversation Summary (Family Finance Management)

This file summarizes user-provided requirements for the "Family Financial Management" project, captured during intake.

## Product summary
A system for **family financial management** that:
- Tracks all **financial transactions** (income/expenses) per family member
- Allows switching views between **Member-mode** (single member) and **Family-mode** (all members)
- Supports **budget categories** defined by the family Admin (Patriarch)
- Imports bank/export data via **CSV** with schema validation and a mapping ("de-para") step
- Provides an **audit** step after import to validate/clean data and assign categories
- Manages **shared expenses** and **debts between members**, including **partial payments**
- Meets a baseline of **LGPD-aligned** security and data lifecycle controls

## Roles & permissions (RBAC)
- **Patriarch (Admin)**
  - The only role that can add members
  - Defines budget categories (members cannot edit categories)
  - Can view all data
- **Member (User)**
  - **Family-mode:** can view all members' transactions and all members' debts
  - **Member-mode:** can view only the selected member's transactions, and only debts relevant to that member

## Member onboarding (Admin-only)
Admin adds a member via UI form with:
- name
- CPF
- birth date
- bank account(s)

## Data rules
- Each transaction belongs to **exactly one member**
- Each member may have **multiple bank accounts**

## CSV import & templates
- System validates required columns on import and supports mapping source columns to a canonical schema
- When importing a new bank/export format ("from zero"), the mapping can be saved as a reusable **bank template** for future imports

## Audit workflow
- Imported transactions can be edited/deleted during audit
- Audit is used to validate imported columns, validate personal data, and assign categories before committing transactions

## Debts
- Shared expense splitting is **manual** (explicit user action per debt/split)
- Split proportions are customizable
- Debts support **partial payments** and settlement

## Security / LGPD baseline
Required in v1:
- encryption at rest
- backups
- data export
- data deletion

## Tech constraints
- Postgres database
- Node.js frontend
- Python backend
- Docker container deployment

