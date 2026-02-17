# OpenExec Skill

## Overview
OpenExec is a deterministic execution engine requiring external governance approval. It runs as a FastAPI service with SQLite storage, replay protection, and receipt verification. Currently in demo mode (v0.1.0).

## Recent Changes
- 2026-02-17: Initial project creation with full runtime surface

## Architecture
- **Runtime**: Python 3.11, FastAPI, SQLAlchemy, Pydantic
- **Database**: SQLite (openexec.db)
- **Entrypoint**: main.py (uvicorn on port 5000)

### Key Files
- `main.py` — FastAPI app with /health, /ready, /version, /execute endpoints
- `openexec/settings.py` — Mode configuration (demo vs clawshield)
- `openexec/engine.py` — Execution engine with replay protection
- `openexec/registry.py` — Action registry with demo actions (echo, add)
- `openexec/db.py` — SQLAlchemy database setup
- `openexec/tables.py` — ExecutionLog table
- `openexec/models.py` — Pydantic request/response schemas
- `openexec/receipts.py` — SHA-256 receipt verification
- `openexec/clawshield_client.py` — ClawShield integration placeholder
- `tests/test_demo_flow.py` — Full test suite

### Modes
- `demo` (default) — All actions auto-approved
- `clawshield` — Requires external governance (not yet wired)

## User Preferences
- GitHub as canonical source of truth
- Every commit intentional, no drift
- ClawHub-ready from day one
- Infrastructure-first approach, not spec-only
