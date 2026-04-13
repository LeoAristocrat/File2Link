from __future__ import annotations

import base64
import hashlib
import hmac
import time


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def _unb64url(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def sign_token(file_id: int, ttl_seconds: int, secret: str) -> str:
    expires = int(time.time()) + max(ttl_seconds, 1)
    payload = f"{file_id}:{expires}".encode("utf-8")
    signature = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    token_raw = f"{file_id}:{expires}:{signature}".encode("utf-8")
    return _b64url(token_raw)


def verify_token(token: str, expected_file_id: int, secret: str) -> bool:
    try:
        decoded = _unb64url(token).decode("utf-8")
        file_id_str, expires_str, sent_sig = decoded.split(":", 2)
        file_id = int(file_id_str)
        expires = int(expires_str)
    except Exception:
        return False

    if file_id != expected_file_id:
        return False
    if expires < int(time.time()):
        return False

    payload = f"{file_id}:{expires}".encode("utf-8")
    expected_sig = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(sent_sig, expected_sig)
