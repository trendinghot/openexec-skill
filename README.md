\# OpenExec — ClawHub Skill



\*\*Governed execution wrapper for deterministic systems.\*\*



This repository is a \*\*ClawHub skill definition\*\*, not a runtime.



OpenExec exposes a governed execution interface that allows agents to:

\- Propose actions

\- Receive approval or denial from governance

\- Execute only approved actions

\- Emit verifiable execution receipts



---



\## What this skill does



\- Accepts structured execution requests

\- Requires explicit governance approval

\- Executes deterministically

\- Emits immutable execution receipts



---



\## What this skill does NOT do



\- It does not decide policy

\- It does not grant permission

\- It does not perform autonomous reasoning



---



\## Architecture context



This skill is part of a three-layer governed execution system:



\- \*\*OpenExec\*\* — deterministic execution engine

\- \*\*ClawShield\*\* — governance and approval gate

\- \*\*ClawLedger\*\* — immutable witness ledger



Each layer is independent and auditable.



---



\## Execution guarantee



Execution only occurs \*\*after\*\* governance approval has been granted.

All executions are logged with:

\- What happened

\- When it happened

\- Under which governance context



---



\## License



To be defined.



