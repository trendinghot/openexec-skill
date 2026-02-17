# OpenExec Skill

## Overview
OpenExec is a deterministic execution engine requiring external governance approval. It runs as a FastAPI service with SQLite storage, replay protection, receipt verification, and constitutional signature enforcement. Version 0.2.0.

## Recent Changes
- 2026-02-17: Added constitutional layer -- signed approval artifact validation with HMAC-SHA256
- 2026-02-17: Added crypto.py, approval_validator.py, test_constitutional.py
- 2026-02-17: Updated engine.py to enforce signature validation in clawshield mode
- 2026-02-17: Settings and approval_validator read env vars at call time (not import time)
- 2026-02-17: Initial project creation with full runtime surface

## Architecture
- **Runtime**: Python 3.11, FastAPI, SQLAlchemy, Pydantic
- **Database**: SQLite (openexec.db)
- **Entrypoint**: main.py (uvicorn on port 5000)
- **Deployment**: Autoscale on Replit

### Key Files
- `main.py` -- FastAPI app with /health, /ready, /version, /execute endpoints
- `openexec/settings.py` -- Mode configuration (demo vs clawshield), reads env at call time
- `openexec/engine.py` -- Execution engine with replay protection and constitutional enforcement
- `openexec/crypto.py` -- HMAC-SHA256 canonical hashing, signing, verification
- `openexec/approval_validator.py` -- Approval artifact validation (hash, signature, tenant, expiry)
- `openexec/clawshield_client.py` -- Approval artifact minting
- `openexec/registry.py` -- Action registry with demo actions (echo, add)
- `openexec/db.py` -- SQLAlchemy database setup
- `openexec/tables.py` -- ExecutionLog table
- `openexec/models.py` -- Pydantic schemas including ApprovalArtifact
- `openexec/receipts.py` -- SHA-256 receipt verification
- `tests/test_demo_flow.py` -- Demo mode test suite (6 tests)
- `tests/test_constitutional.py` -- Constitutional mode test suite (10 tests)

### Modes
- `demo` (default) -- All actions auto-approved
- `clawshield` -- Requires signed approval artifact with hash binding, signature verification, tenant isolation, and expiry enforcement

## User Preferences
- GitHub as canonical source of truth
- Every commit intentional, no drift
- ClawHub-ready from day one
- Infrastructure-first approach, not spec-only
