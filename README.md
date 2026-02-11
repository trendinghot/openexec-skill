# OpenExec — ClawHub Skill

**Governed execution for agents that must act in the real world.**

This repository defines a **ClawHub skill** that exposes OpenExec as a governed execution interface.
It is intentionally **not** a runtime, agent, or decision-maker.

OpenExec exists to solve a hard problem in modern AI systems:

> How do you let agents *do real things* without letting them decide *whether they should*?

---

## Why OpenExec exists

Most agent systems collapse three responsibilities into one layer:

1. Reasoning (what should be done)
2. Authorization (is it allowed)
3. Execution (do it)

That design does not scale.
It fails under audit, regulation, failure, and adversarial pressure.

**OpenExec separates these concerns by design.**

It executes work **only after** governance approval has been granted elsewhere.

---

## Why this model matters

Most agent systems fail silently:
they act, but cannot later explain *why*.

This architecture makes execution:
- Explicit instead of implicit
- Governed instead of assumed
- Auditable instead of opaque

It allows AI systems to operate in environments where
trust, accountability, and review are required — not optional.


## What this skill enables

When installed via ClawHub, OpenExec allows agents to:

- Propose **explicit, structured actions**
- Submit those actions for **external governance review**
- Execute **only** actions that have been approved
- Produce **verifiable execution receipts** for every action taken

This makes agent behavior:
- Reviewable
- Reproducible
- Auditable
- Defensible outside the system itself

---

## What this skill does

- Accepts structured execution requests
- Requires explicit governance approval
- Executes deterministically (no hidden reasoning)
- Emits immutable execution receipts

---

## What this skill explicitly does NOT do

- It does **not** decide policy
- It does **not** grant permission
- It does **not** reason autonomously
- It does **not** modify governance rules
- It does **not** self-authorize actions

These are not limitations.
They are **safety boundaries**.

---

## Architecture context

This skill is one layer of a three-layer governed execution system:

- **OpenExec** — deterministic execution engine  
  https://github.com/trendinghot/openclaw

- **ClawShield** — governance and approval gate  
  https://github.com/trendinghot/clawshield

- **ClawLedger** — immutable witness ledger  
  https://github.com/trendinghot/clawledger

Each layer is:
- Independent
- Replaceable
- Auditable

No single layer can act alone.

---

## Execution flow (at a glance)

A typical governed execution using this skill looks like:

1. An agent proposes a structured action  
   (e.g. “send email”, “run job”, “update record”)

2. The proposal is evaluated by governance  
   via **ClawShield** (policy, rules, approvals)

3. If approved, an execution token is issued

4. OpenExec executes the action deterministically  
   using the approved parameters only

5. A receipt is written to **ClawLedger**  
   capturing what happened and why it was allowed

At no point can the executing system self-authorize.


## Execution guarantee

OpenExec enforces a hard invariant:

> **Execution only occurs after governance approval has been granted.**

Every execution produces a receipt containing:

- What happened
- When it happened
- Under which governance context
- Which approval allowed it

Receipts are evidence, not logs.

---

## Who this is for

This skill is designed for teams building:

- Agent systems that touch real infrastructure
- Regulated or audited environments
- Multi-agent workflows with shared responsibility
- AI systems that must be explainable *after the fact*
- Platforms where trust matters more than speed

---

## License

To be defined.
