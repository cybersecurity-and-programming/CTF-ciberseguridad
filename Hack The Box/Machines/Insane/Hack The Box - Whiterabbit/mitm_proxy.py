#!/usr/bin/python3

import hmac
import hashlib
import json
from mitmproxy import http

SECRET = b"3CWVGMndgMvdVAzOjqBiTicmv7gxc6IS"

def request(flow: http.HTTPFlow) -> None:
    if flow.request.content:
        try:
            data = json.loads(flow.request.content)
            body = json.dumps(data, separators=(',', ':')).encode()
        except json.JSONDecodeError:
            body = flow.request.content

        signature = hmac.new(SECRET, body, hashlib.sha256).hexdigest()
        flow.request.headers["x-gophish-signature"] = f"sha256={signature}"
