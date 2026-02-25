# FastAPI Task Manager (FastAPI + Async SQLAlchemy)

Minimal FastAPI skeleton with async SQLAlchemy 2.0, JWT auth, tasks, and rate limiting.

## Stack
- FastAPI
- SQLAlchemy 2.0 (async) + asyncpg
- PostgreSQL
- JWT (PyJWT)
- Pydantic v2
- SlowAPI (rate limiting)

## Requirements
- Python 3.14+
- PostgreSQL
- Redis (for rate limiting)

## Setup
1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -e .
```

If you use uv:

```bash
uv sync
```

## Environment
Copy `.env.example` to `.env` and adjust values:

```bash
cp .env.example .env
```

## Run
```bash
uvicorn main:app --reload
```

## Auth flow (quick check)
1. `POST /signup`
2. `POST /token` (OAuth2 password flow)
3. Use `Authorization: Bearer <token>` for protected routes

## Notes
- Alembic is configured; run migrations as needed.
- This is a skeleton project; no production hardening beyond basic JWT checks and rate limiting.
