# OpenExec
### Deterministic Execution for AI Systems That Touch the Real World

If your AI can send emails, move money, delete data, or touch production --
you need a hard boundary between **what it thinks** and **what it can execute**.

OpenExec is that boundary.

It sits between your agent and your infrastructure and enforces one rule:

> Nothing executes without explicit approval.

Not "probably allowed."
Not "the model decided."
Not "it looked safe."

Explicit approval. Deterministic execution. Verifiable receipts.

---

## The Problem (You Already Know This)

If you're building with:

- OpenAI function calls
- Tool-using agents
- LangChain / LlamaIndex / custom orchestration
- Autonomous workflows

You are already letting models generate execution payloads.

That means:

- A hallucinated parameter can trigger a real API call.
- A retry loop can duplicate a payment.
- A subtle prompt injection can mutate execution intent.
- A bug can execute twice.
- A race condition can fire in parallel.

You don't need a smarter model.

You need an execution boundary.

---

## What OpenExec Does

OpenExec is a lightweight execution adapter that:

- Accepts structured execution requests
- Enforces replay protection
- Optionally verifies signed approvals (ClawShield mode)
- Executes deterministically
- Emits a receipt for every execution attempt
- Allows receipt verification

It does **not**:

- Define policy
- Make decisions
- Evaluate prompts
- Override governance
- Self-authorize execution

It executes only what has already been approved.

---

## 90-Second Quickstart (Demo Mode)

You can test this right now.

### 1) Install

```bash
pip install -r requirements.txt
```

### 2) Run

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 5000
```

### 3) Confirm health

```bash
curl http://localhost:5000/health
```

### 4) Execute something deterministic

```bash
curl -X POST http://localhost:5000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "action": "echo",
    "payload": { "msg": "hello world" },
    "nonce": "unique-1"
  }'
```

You'll get a receipt.

Now try it again with the same nonce:

```bash
curl -X POST http://localhost:5000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "action": "echo",
    "payload": { "msg": "hello world" },
    "nonce": "unique-1"
  }'
```

Replay denied.

That alone prevents entire classes of production incidents.

---

## Verify a Receipt

Every execution attempt produces a deterministic receipt.

```bash
curl -X POST http://localhost:5000/receipts/verify \
  -H "Content-Type: application/json" \
  -d '{
    "exec_id": "<id>",
    "result": "<result_json>",
    "receipt": "<hash>"
  }'
```

Receipts are evidence, not logs.

Logs can be altered.
Receipts can be verified.

---

## How You'd Use This in Real Systems

Instead of:

```python
send_email(to, subject, body)
```

You route through OpenExec:

```python
requests.post("http://localhost:5000/execute", json={
    "action": "send_email",
    "payload": {...},
    "nonce": uuid4().hex
})
```

In production, you enable strict mode.

---

## Production Mode (ClawShield)

For real systems, you don't want demo auto-approval.

You want signed approvals issued by a governance layer.

Enable:

```bash
export OPENEXEC_MODE=clawshield
export CLAWSHIELD_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----..."
export CLAWSHIELD_TENANT_ID="your-tenant-id"
```

Now:

- Execution requires a signed approval artifact.
- Approval hash must match the request.
- Signature must verify (Ed25519).
- Expired approvals are rejected.
- Tenant must match.

No live API dependency required during execution.

This keeps authority separate from execution.

ClawShield governance layer:
[https://clawshield.forgerun.ai/](https://clawshield.forgerun.ai/)

---

## Architecture (Simple and Intentional)

```
Agent / Client
      |
      v
  OpenExec ---- deterministic execution adapter
      |
      v
  ClawShield -- approval minting + governance (SaaS)
      |
      v
  ClawLedger -- witness layer (optional)
```

Each layer is replaceable.

No single layer can act alone.

That separation is the point.

---

## When You Actually Need This

You don't need OpenExec for chatbots.

You need it when:

- Your AI can trigger payments
- Your AI can modify infrastructure
- Your AI can send production email
- Your AI can call internal tools
- Your AI can delete data

If your agent can act in the real world,
it should not be allowed to execute what it merely imagines.

---

## Why This Is Different

Most AI stacks collapse:

```
Reasoning -> Authorization -> Execution
```

OpenExec forces:

```
Propose -> Approve -> Execute -> Witness
```

That separation prevents silent escalation.

---

## What Happens If You Don't Add This Layer?

Nothing.

Until something goes wrong.

And then:

- Duplicate execution
- Escalated permissions
- Hallucinated parameters
- Audit gaps
- No evidence trail

Execution safety is invisible -- until it isn't.

---

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info |
| `/health` | GET | Health status + mode + signature verification |
| `/ready` | GET | Readiness check |
| `/version` | GET | Version metadata |
| `/execute` | POST | Execute an approved action |
| `/receipts/verify` | POST | Verify receipt hash integrity |

---

## Status

- Demo mode: stable
- Replay protection: enforced
- Deterministic receipts: enforced
- Signed approval validation: implemented (Ed25519)
- No external dependencies required for testing

---

## TL;DR

If your AI touches production,
separate authority from execution.

OpenExec is the minimal adapter that makes that possible.
