import hmac
import hashlib
import json
from typing import Union

def canonical_hash(data: Union[dict, str]) -> str:
    if isinstance(data, dict):
        data = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode()).hexdigest()

def sign_message(secret_key: str, message: str) -> str:
    return hmac.new(
        secret_key.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

def verify_signature(secret_key: str, message: str, signature: str) -> bool:
    expected = hmac.new(
        secret_key.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
