# OpenExec

Deterministic execution engine requiring external governance approval.

## Quick Start

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

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info |
| `/health` | GET | Health check |
| `/version` | GET | Version info |
| `/ready` | GET | Readiness check |
| `/execute` | POST | Execute an action |

## Configuration

Set `OPENEXEC_MODE` environment variable:

- `demo` (default) — All actions auto-approved
- `clawshield` — Requires ClawShield governance approval

## Project Structure

```
openexec-skill/
├── main.py                  # FastAPI application
├── requirements.txt         # Python dependencies
├── SKILL.md                 # Skill metadata
├── openexec/
│   ├── __init__.py
│   ├── settings.py          # Mode configuration
│   ├── db.py                # Database setup
│   ├── tables.py            # SQLAlchemy models
│   ├── models.py            # Pydantic schemas
│   ├── registry.py          # Action registry
│   ├── engine.py            # Execution engine
│   ├── clawshield_client.py # ClawShield integration (Phase 7)
│   └── receipts.py          # Receipt verification
├── config/
│   └── openexec.example.json
├── scripts/
│   ├── install.sh
│   └── run.sh
└── tests/
    └── test_demo_flow.py
```

## Receipt Verification

Every execution produces a SHA-256 receipt. Verify with:

```python
from openexec.receipts import verify_receipt
verify_receipt(exec_id, result_json, receipt_hash)
```

## License

Proprietary.
