# Backend (FastAPI)

## Setup
- Install: `python -m pip install -r requirements.txt`
- Run: `uvicorn app.main:app --reload`

Note: This repo is currently easiest to run via Docker (Python 3.11), since some local Python versions may not have wheels for required deps.

## Environment variables
- `DATABASE_URL` (required)
  - Example (docker compose): `postgresql+psycopg://swaif:swaif@localhost:5432/swaif`
- `SEED_PATRIARCH_CPF` (optional, default: `00000000000`)
- `SEED_PATRIARCH_PASSWORD` (optional, default: `admin123`)

## Seed
Seed is run automatically on app startup (idempotent) to ensure the initial Family + Patriarch exist.

Default seeded credentials (dev only):
- CPF: `00000000000`
- Password: `admin123`
