from fastapi import FastAPI
import os
import datetime

app = FastAPI()

VERSION = "0.1.0"

@app.get("/")
def root():
    return {"name": "OpenExec", "version": VERSION}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "mode": os.getenv("OPENEXEC_MODE", "demo")
    }

@app.get("/version")
def version():
    return {
        "version": VERSION,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@app.get("/ready")
def ready():
    return {"ready": True}
