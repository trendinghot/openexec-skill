---
name: OpenExec
slug: openexec
version: 0.1.0
category: infrastructure
description: Deterministic execution engine requiring external governance approval.
runtime: python
entrypoint: main.py
env:
  - OPENEXEC_MODE
  - CLAWSHIELD_BASE_URL
  - CLAWSHIELD_API_KEY
  - CLAWSHIELD_TENANT_ID
---

# OpenExec Skill

OpenExec is a deterministic execution engine that requires external governance approval before performing any action.

## Modes

- **demo** (default): All actions are auto-approved. For local development and testing.
- **clawshield**: Actions require governance approval from ClawShield before execution.

## Actions

Actions are registered in the action registry. Demo actions included:

- `echo` — Returns the payload back
- `add` — Adds two numbers (`a` and `b`)

## Execution Flow

1. Client sends POST `/execute` with `action`, `payload`, and `nonce`
2. Engine checks for replay (duplicate nonce)
3. In demo mode, action is auto-approved
4. Action handler executes deterministically
5. Result is logged with SHA-256 receipt
6. Receipt can be independently verified

## Replay Protection

Every execution requires a unique `nonce`. Duplicate nonces return the original result without re-execution.

## Receipt Verification

Each execution produces a SHA-256 receipt derived from the execution ID and result. Receipts can be verified via `openexec.receipts.verify_receipt()`.
