from pydantic import BaseModel
from typing import Optional

class ExecutionRequest(BaseModel):
    action: str
    payload: Optional[dict] = None
    nonce: str

class ExecutionResult(BaseModel):
    id: str
    action: str
    result: dict
    approved: bool
    receipt: Optional[str] = None
