"""
ClawShield integration client.

Provides artifact minting for testing and future remote governance calls.
"""

import os
import uuid
import datetime
from openexec.crypto import canonical_hash, sign_message

CLAWSHIELD_BASE_URL = os.getenv("CLAWSHIELD_BASE_URL", "")
CLAWSHIELD_API_KEY = os.getenv("CLAWSHIELD_API_KEY", "")
CLAWSHIELD_TENANT_ID = os.getenv("CLAWSHIELD_TENANT_ID", "")
CLAWSHIELD_SECRET_KEY = os.getenv("CLAWSHIELD_SECRET_KEY", "")

def mint_approval_artifact(action_request: dict, tenant_id: str = "", secret_key: str = "") -> dict:
    tenant = tenant_id or CLAWSHIELD_TENANT_ID
    secret = secret_key or CLAWSHIELD_SECRET_KEY
    approval_id = str(uuid.uuid4())
    action_hash = canonical_hash(action_request)
    issued_at = datetime.datetime.utcnow().isoformat()

    message = f"{approval_id}:{action_hash}:{tenant}:{issued_at}"
    signature = sign_message(secret, message)

    return {
        "approval_id": approval_id,
        "action_hash": action_hash,
        "signature": signature,
        "issued_by": "clawshield",
        "issued_at": issued_at,
        "tenant_id": tenant
    }
