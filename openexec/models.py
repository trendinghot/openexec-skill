from pydantic import BaseModel
from typing import Optional

class ApprovalArtifact(BaseModel):
    approval_id: str
    action_hash: str
    signature: str
    issued_by: str = "clawshield"
    issued_at: str
    tenant_id: str

class ExecutionRequest(BaseModel):
    action: str
    payload: Optional[dict] = None
    nonce: str
    approval_artifact: Optional[ApprovalArtifact] = None

class ExecutionResult(BaseModel):
    id: str
    action: str
    result: dict
    approved: bool
    receipt: Optional[str] = None
