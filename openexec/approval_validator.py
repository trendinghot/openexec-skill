import os
import datetime
from openexec.crypto import canonical_hash, verify_signature

class ApprovalError(Exception):
    pass

def validate_approval(action_request: dict, artifact: dict) -> bool:
    request_hash = canonical_hash(action_request)

    if artifact.get("action_hash") != request_hash:
        raise ApprovalError("Action hash mismatch: approval does not match this request")

    signature = artifact.get("signature", "")
    message = f"{artifact['approval_id']}:{artifact['action_hash']}:{artifact['tenant_id']}:{artifact['issued_at']}"
    secret = os.getenv("CLAWSHIELD_SECRET_KEY", "")

    if not secret:
        raise ApprovalError("CLAWSHIELD_SECRET_KEY not configured")

    if not verify_signature(secret, message, signature):
        raise ApprovalError("Invalid signature: approval artifact is not authentic")

    expected_tenant = os.getenv("CLAWSHIELD_TENANT_ID", "")
    if expected_tenant and artifact.get("tenant_id") != expected_tenant:
        raise ApprovalError(f"Tenant mismatch: expected {expected_tenant}, got {artifact.get('tenant_id')}")

    if artifact.get("issued_by") != "clawshield":
        raise ApprovalError(f"Unknown issuer: {artifact.get('issued_by')}")

    issued_at = artifact.get("issued_at", "")
    if issued_at:
        try:
            issued_time = datetime.datetime.fromisoformat(issued_at)
            age = datetime.datetime.utcnow() - issued_time
            if age.total_seconds() > 300:
                raise ApprovalError("Approval artifact expired (older than 5 minutes)")
        except ValueError:
            raise ApprovalError("Invalid issued_at timestamp")

    return True
