from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openexec.models import ExecutionRequest
from openexec.receipts import verify_receipt
from openexec.engine import execute
from openexec.approval_validator import ApprovalError
from openexec.db import init_db
import os
import datetime

VERSION = "0.3.0"

@asynccontextmanager
async def lifespan(application):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"service": "OpenExec", "status": "running", "version": VERSION}

@app.get("/health")
async def health():
    mode = os.getenv("OPENEXEC_MODE", "demo")
    sig_status = "enabled" if mode == "clawshield" else "disabled"
    return {"status": "healthy", "mode": mode, "signature_verification": sig_status}

@app.get("/version")
def version():
    return {
        "version": VERSION,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@app.get("/ready")
def ready():
    return {"ready": True}

@app.post("/execute")
def execute_action(request: ExecutionRequest):
    try:
        result = execute(request)
        return result.model_dump()
    except ApprovalError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

class ReceiptVerifyRequest(BaseModel):
    exec_id: str
    result: str
    receipt: str

@app.post("/receipts/verify")
def verify_receipt_endpoint(req: ReceiptVerifyRequest):
    valid = verify_receipt(req.exec_id, req.result, req.receipt)
    return {"valid": valid}
