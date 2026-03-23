# FastAPI Task Manager (FastAPI + Async SQLAlchemy)

Minimal FastAPI skeleton with async SQLAlchemy 2.0, JWT auth, tasks, and rate limiting.

## Stack
- FastAPI
- SQLAlchemy 2.0 (async) + asyncpg
- PostgreSQL
- JWT (PyJWT)
- Pydantic v2
- SlowAPI (rate limiting)
- Docker + Docker Compose

## Requirements
- Docker
- Docker Compose

## Setup

1. Copy environment variables:

```bash
cp .env.example .env
```

2. Build and run the project:

```bash
docker compose up --build
```

## App
- API will be available at: http://localhost:8000
- Docs: http://localhost:8000/docs

## Auth flow (quick check)
1. `POST /signup`
2. `POST /token` (OAuth2 password flow)
3. Use `Authorization: Bearer <token>` for protected routes

## Notes
- PostgreSQL and Redis are started via Docker Compose
- Alembic is configured; run migrations as needed inside the container
- This is a skeleton project; no production hardening beyond basic JWT checks and rate limiting
