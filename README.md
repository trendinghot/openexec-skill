# OpenExec

Deterministic execution engine requiring external governance approval.

## Quick Start (Demo Mode)

```bash
# Install
pip install -r requirements.txt

# Run
python -m uvicorn main:app --host 0.0.0.0 --port 5000 --reload

# Health check
curl http://localhost:5000/health

# Execute an action
curl -X POST http://localhost:5000/execute \
  -H "Content-Type: application/json" \
  -d '{"action": "echo", "payload": {"msg": "hello"}, "nonce": "unique-1"}'

# Add numbers
curl -X POST http://localhost:5000/execute \
  -H "Content-Type: application/json" \
  -d '{"action": "add", "payload": {"a": 2, "b": 3}, "nonce": "unique-2"}'
```

## Modes

### Demo (default)
All actions auto-approved. No configuration needed.

### ClawShield (signature verified)
Requires signed approval artifacts. Set environment:
```bash
OPENEXEC_MODE=clawshield
CLAWSHIELD_SECRET_KEY=your-shared-secret
CLAWSHIELD_TENANT_ID=your-tenant-id
```

Execute with approval artifact:
```bash
curl -X POST http://localhost:5000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "action": "echo",
    "payload": {"msg": "governed"},
    "nonce": "unique-3",
    "approval_artifact": {
      "approval_id": "...",
      "action_hash": "...",
      "signature": "...",
      "issued_by": "clawshield",
      "issued_at": "...",
      "tenant_id": "..."
    }
  }'
```

Without a valid artifact, execution is rejected with 403.

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info |
| `/health` | GET | Health check |
| `/version` | GET | Version info |
| `/ready` | GET | Readiness check |
| `/execute` | POST | Execute an action |

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
│   ├── crypto.py              # HMAC-SHA256 signing and verification
│   ├── approval_validator.py  # Approval artifact validation
│   ├── clawshield_client.py   # ClawShield artifact minting
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

1. **Hash binding** -- Canonical hash of action request must match the artifact
2. **Signature verification** -- HMAC-SHA256 signature must be authentic
3. **Tenant isolation** -- Tenant ID must match configuration
4. **Issuer verification** -- Must be issued by ClawShield
5. **Expiry enforcement** -- Artifacts expire after 5 minutes

## Receipt Verification

Every execution produces a SHA-256 receipt. Verify with:

```python
from openexec.receipts import verify_receipt
verify_receipt(exec_id, result_json, receipt_hash)
```

## License

Proprietary.
