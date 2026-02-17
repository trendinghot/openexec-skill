---
name: OpenExec
slug: openexec
version: 0.3.0
category: infrastructure
description: Deterministic execution engine requiring external governance approval with Ed25519 signature enforcement.
runtime: python
entrypoint: main.py
env:
  - OPENEXEC_MODE
  - CLAWSHIELD_PUBLIC_KEY
  - CLAWSHIELD_TENANT_ID
---

# OpenExec Skill

OpenExec is a deterministic execution engine that requires external governance approval before performing any action. In ClawShield mode, execution requires a cryptographically signed (Ed25519) approval artifact. Authority originates from ClawShield. OpenExec only verifies -- it never evaluates policy.

## Modes

### Demo (default)
All actions are auto-approved. Zero friction for adoption and local development.

### ClawShield (Ed25519 signature verified)
Actions require a signed approval artifact issued by ClawShield. The engine validates:
1. Canonical SHA-256 hash of the action request matches the artifact
2. Ed25519 signature is authentic against the configured public key
3. Approval has not expired (expires_at check)
4. Tenant ID matches configuration

No execution without externally minted authority. No live API calls. Fully offline verification.

## Approval Artifact Format

```json
{
  "approval_id": "uuid",
  "tenant_id": "tenant-123",
  "action_hash": "sha256-of-canonical-action-request",
  "issued_at": "ISO-8601",
  "expires_at": "ISO-8601",
  "signature": "base64-ed25519-signature"
}
```

Signature is computed over:
```
approval_id + tenant_id + action_hash + issued_at + expires_at
```

Using Ed25519. OpenExec verifies with `CLAWSHIELD_PUBLIC_KEY`.

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
3. Engine validates approval artifact (hash, expiry, signature, tenant)
4. If valid, handler executes deterministically
5. Result is logged with SHA-256 receipt
6. If invalid, returns 403 with specific rejection reason

## Replay Protection

Every execution requires a unique `nonce`. Duplicate nonces return the original result without re-execution.

## Receipt Verification

Each execution produces a SHA-256 receipt derived from the execution ID and result. Receipts can be verified via `openexec.receipts.verify_receipt()`.

## What OpenExec Does NOT Do

- Does not evaluate policy
- Does not make live API calls during execution
- Does not mint approvals
- Does not manage tenants
- Does not check revocation
- Does not anchor to ledgers

OpenExec is purely: deterministic execution + signature verification.
