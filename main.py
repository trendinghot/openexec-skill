from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from openexec.models import ExecutionRequest
from openexec.engine import execute
from openexec.approval_validator import ApprovalError
from openexec.db import init_db
import os
import datetime

VERSION = "0.2.0"

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
    return {"status": "healthy", "mode": os.getenv("OPENEXEC_MODE", "demo")}

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
