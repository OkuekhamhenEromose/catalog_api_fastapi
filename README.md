# Book Catalog API (PyVol 5 — Project 1)

FastAPI + PostgreSQL 16 + SQLAlchemy 2 + Alembic + pytest. Source reproduced from
*Think Like a Backend Engineer — PyVol 5*. Verified: **71 tests pass** against a real PostgreSQL 16 database.

## Setup
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# PostgreSQL (as the postgres superuser)
CREATE USER course_user WITH PASSWORD 'course_pass' CREATEDB;
CREATE DATABASE catalog_db   OWNER course_user;   -- development
CREATE DATABASE catalog_test OWNER course_user;   -- tests only (truncated every test)

cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload      # http://127.0.0.1:8000/docs
pytest                             # needs catalog_test; builds schema from real migrations
```

## Optional: performance experiment (dev database only)
`psql -U course_user -d catalog_db -f scripts/seed_perf.sql` then `scripts/explain.sql`.

## Layout
`app/` application code · `migrations/` Alembic · `tests/` pytest suite · `scripts/` SQL for load/EXPLAIN.
