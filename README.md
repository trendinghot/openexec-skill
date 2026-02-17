# OpenExec

Deterministic execution engine requiring external governance approval.

## Quick Start (Demo Mode)

```bash
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 5000 --reload

curl http://localhost:5000/health
curl -X POST http://localhost:5000/execute \
  -H "Content-Type: application/json" \
  -d '{"action": "echo", "payload": {"msg": "hello"}, "nonce": "unique-1"}'
```

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info |
| `/health` | GET | Health check with mode and signature status |
| `/version` | GET | Version info |
| `/ready` | GET | Readiness check |
| `/execute` | POST | Execute an action |

## Modes

### Demo (default)
All actions auto-approved. No configuration needed.

### ClawShield -- Signed Approval Enforcement

In ClawShield mode, every execution requires a cryptographically signed approval artifact verified with Ed25519.

**Configuration:**
```bash
OPENEXEC_MODE=clawshield
CLAWSHIELD_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"
CLAWSHIELD_TENANT_ID=your-tenant-id
```

**How it works:**
1. ClawShield mints an approval artifact containing a canonical hash of the action request
2. ClawShield signs the artifact with its Ed25519 private key
3. Client submits the artifact alongside the execution request
4. OpenExec verifies the hash binding, signature, expiry, and tenant match
5. If valid, execution proceeds. If invalid, execution is denied (403).

OpenExec does not evaluate policy. It does not call external services during execution. Authority must originate from ClawShield via a signed artifact. Verification is fully offline.

**Execute with approval artifact:**
```bash
curl -X POST http://localhost:5000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "action": "echo",
    "payload": {"msg": "governed"},
    "nonce": "unique-3",
    "approval_artifact": {
      "approval_id": "...",
      "tenant_id": "...",
      "action_hash": "...",
      "issued_at": "...",
      "expires_at": "...",
      "signature": "base64-ed25519-signature"
    }
  }'
```

## Project Structure

```
openexec-skill/
├── main.py                    # FastAPI application
├── requirements.txt           # Python dependencies
├── SKILL.md                   # Skill metadata (YAML frontmatter)
├── openexec/
│   ├── __init__.py
│   ├── settings.py            # Mode configuration
│   ├── db.py                  # Database setup
│   ├── tables.py              # SQLAlchemy models
│   ├── models.py              # Pydantic schemas
│   ├── registry.py            # Action registry
│   ├── engine.py              # Execution engine
│   ├── crypto.py              # Ed25519 verification + canonical hashing
│   ├── approval_validator.py  # Approval artifact validation
│   ├── clawshield_client.py   # Test artifact minting
│   └── receipts.py            # Receipt verification
├── config/
│   └── openexec.example.json
├── scripts/
│   ├── install.sh
│   └── run.sh
└── tests/
    ├── test_demo_flow.py
    └── test_constitutional.py
```

## Constitutional Enforcement

In ClawShield mode, every execution requires a signed approval artifact. The engine validates:

1. **Hash binding** -- Canonical SHA-256 hash of action request must match the artifact
2. **Expiry enforcement** -- Artifact must not be expired (expires_at > now)
3. **Ed25519 signature verification** -- Signature must be authentic against public key
4. **Tenant isolation** -- Tenant ID must match configuration

Signature is computed over: `approval_id + tenant_id + action_hash + issued_at + expires_at`

## Receipt Verification

Every execution produces a SHA-256 receipt:

```python
from openexec.receipts import verify_receipt
verify_receipt(exec_id, result_json, receipt_hash)
```

## License

Proprietary.
