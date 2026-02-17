---
name: OpenExec
slug: openexec
version: 0.2.0
category: infrastructure
description: Deterministic execution engine requiring external governance approval with constitutional signature enforcement.
runtime: python
entrypoint: main.py
env:
  - OPENEXEC_MODE
  - CLAWSHIELD_SECRET_KEY
  - CLAWSHIELD_TENANT_ID
  - CLAWSHIELD_BASE_URL
  - CLAWSHIELD_API_KEY
---

# OpenExec Skill

OpenExec is a deterministic execution engine that requires external governance approval before performing any action.

## Modes

### Demo (default)
All actions are auto-approved. Zero friction for adoption and local development.

### ClawShield (signature verified)
Actions require a signed approval artifact issued by ClawShield. The engine validates:
1. Canonical hash of the action request matches the artifact
2. HMAC-SHA256 signature is authentic
3. Tenant ID matches configuration
4. Issuer is ClawShield
5. Artifact is not expired (5 minute TTL)

No execution without externally minted authority.

## Actions

Actions are registered in the action registry. Demo actions included:

- `echo` -- Returns the payload back
- `add` -- Adds two numbers (`a` and `b`)

## Execution Flow

### Demo Mode
1. Client sends POST `/execute` with `action`, `payload`, and `nonce`
2. Engine checks for replay (duplicate nonce)
3. Action is auto-approved
4. Handler executes deterministically
5. Result is logged with SHA-256 receipt

### ClawShield Mode
1. Client sends POST `/execute` with `action`, `payload`, `nonce`, and `approval_artifact`
2. Engine checks for replay (duplicate nonce)
3. Engine validates approval artifact (hash, signature, tenant, expiry)
4. If valid, handler executes deterministically
5. Result is logged with SHA-256 receipt
6. If invalid, returns 403 with specific rejection reason

## Replay Protection

Every execution requires a unique `nonce`. Duplicate nonces return the original result without re-execution.

## Receipt Verification

Each execution produces a SHA-256 receipt derived from the execution ID and result. Receipts can be verified via `openexec.receipts.verify_receipt()`.

## Approval Artifact Format

```json
{
  "approval_id": "uuid",
  "action_hash": "sha256-of-canonical-action-request",
  "signature": "hmac-sha256-signature",
  "issued_by": "clawshield",
  "issued_at": "iso-timestamp",
  "tenant_id": "tenant-identifier"
}
```
