---
name: OpenExec
slug: openexec
version: 0.1.0
category: infrastructure/governance/execution
runtime: python
entrypoint: main:app
requires_network: false
modes:
  - demo
  - clawshield
env:
  - OPENEXEC_MODE
  - CLAWSHIELD_PUBLIC_KEY
  - CLAWSHIELD_TENANT_ID
  - CLAWSHIELD_BASE_URL
description: Deterministic execution adapter that runs only with a signed approval artifact (ClawShield mode) and emits verifiable receipts.
---

# OpenExec — Governed Deterministic Execution (Skill)

OpenExec is a **runnable** governed execution service.  
It executes **only** what has already been approved.

It is not an agent.  
It is not a policy engine.  
It does not self-authorize.

---

## Install

```bash
pip install -r requirements.txt
```

## Run (local)

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 5000
```

---

## Endpoints

* `GET /` → must return 200 quickly (deployment health check)
* `GET /health` → health status
* `GET /ready` → readiness checks
* `GET /version` → version metadata
* `POST /execute` → execute an approved action deterministically
* `POST /receipts/verify` → verify receipt hash integrity

---

## Modes

### 1) Demo mode (default, free)

No external governance required. Useful for indie hackers.

```bash
export OPENEXEC_MODE=demo
```

Demo mode still enforces:

* deterministic execution
* replay protection (nonce/action hash)
* receipt generation

### 2) ClawShield mode (production / business)

Requires a **signed approval artifact** issued by ClawShield.
OpenExec verifies the signature offline using the ClawShield public key.

```bash
export OPENEXEC_MODE=clawshield
export CLAWSHIELD_PUBLIC_KEY="-----BEGIN PUBLIC KEY----- ... -----END PUBLIC KEY-----"
export CLAWSHIELD_TENANT_ID="tenant-id"
export CLAWSHIELD_BASE_URL="https://clawshield.forgerun.ai"
```

If signature validation fails → execution is denied.

---

## 90-Second Quickstart (Demo)

1. Start server:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 5000
```

2. Confirm health:

```bash
curl http://localhost:5000/health
```

3. Execute a deterministic demo action:

```bash
curl -X POST http://localhost:5000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "action":"echo",
    "payload":{"msg":"hello"},
    "nonce":"unique-1"
  }'
```

4. Replay attempt (should return same result, not re-execute):

```bash
curl -X POST http://localhost:5000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "action":"echo",
    "payload":{"msg":"hello"},
    "nonce":"unique-1"
  }'
```

---

## Receipts

Every execution attempt produces a receipt hash.
Receipts are **evidence**, not logs.

Verify a receipt hash:

```bash
curl -X POST http://localhost:5000/receipts/verify \
  -H "Content-Type: application/json" \
  -d '{"exec_id":"<id>","result":"<result_json>","receipt":"<hash>"}'
```

---

## What this skill does

* Accepts structured execution requests
* Enforces replay protection
* Executes deterministically (approved parameters only)
* Emits verifiable receipts for every attempt
* In ClawShield mode: verifies **signed approvals** before execution

## What this skill does not do

* Define policy
* Grant permissions
* Reason autonomously
* Override governance decisions
* Self-authorize execution

---

## Architecture context (3-layer separation)

* **OpenExec** — deterministic execution adapter (this skill)
* **ClawShield** — governance + approval minting (SaaS): [https://clawshield.forgerun.ai/](https://clawshield.forgerun.ai/)
* **ClawLedger** — witness ledger (optional integration)

Each layer is replaceable. No single layer can act alone.
