"""
ClawShield integration client.

When OPENEXEC_MODE=clawshield, this module handles:
- POST /api/governance/evaluate  — request governance approval
- POST /api/governance/mint      — mint execution receipt
- POST /api/execute              — execute via ClawShield
- GET  /api/receipts/verify      — verify receipt authenticity

Not yet wired. This is a placeholder for Phase 7.
"""

import os

CLAWSHIELD_BASE_URL = os.getenv("CLAWSHIELD_BASE_URL", "")
CLAWSHIELD_API_KEY = os.getenv("CLAWSHIELD_API_KEY", "")
CLAWSHIELD_TENANT_ID = os.getenv("CLAWSHIELD_TENANT_ID", "")
