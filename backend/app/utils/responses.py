from typing import Any
from uuid import uuid4

from flask import jsonify


def success_response(*, data: Any = None, message: str = "OK", status_code: int = 200):
    payload = {
        "success": True,
        "code": "OK",
        "message": message,
        "data": data,
        "request_id": str(uuid4()),
    }
    return jsonify(payload), status_code
