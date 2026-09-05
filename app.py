#!/usr/bin/env python3
"""Flask HTTP API — thin server over sdk.py (ID Document Liveness Detection, Linux).

Exposes /api/* for Postman, curl, and the Gradio demo (``python3 demo``). Does not embed Gradio.
Product focus: document authenticity / security (presentation-attack) checks only.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from flask import Flask, Response, request
from werkzeug.exceptions import HTTPException

import license_ux
import sdk

ROOT = Path(__file__).resolve().parent
app = Flask(__name__)
PRODUCT = "DocumentLiveness"
DEFAULT_PORT = 8086


def envelope(success: bool, code: int, message: str, data=None, status: int = 200):
    return Response(
        json.dumps(
            {
                "success": success,
                "code": code,
                "message": message,
                "request_id": None,
                "data": data,
            }
        ),
        status=status,
        mimetype="application/json",
    )


def sdk_json(result):
    raw = result if isinstance(result, (bytes, bytearray)) else str(result).encode()
    return Response(raw, mimetype="application/json")


@app.after_request
def cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


@app.route("/api/<path:_unused>", methods=["OPTIONS"])
def options(_unused):
    return Response(status=204)


@app.get("/api/health")
def health():
    return envelope(True, 0, "OK", {"status": "ok"})


@app.get("/api/machinecode")
def machinecode():
    return envelope(True, 0, "OK", {"machinecode": sdk.get_machine_code()})


@app.get("/api/licenseStatus")
def license_status():
    license_ux.reload_if_changed(ROOT, sdk.activate)
    return envelope(True, 0, "OK", sdk.get_license_status())


@app.get("/api/backend")
def backend():
    name = (os.environ.get("FACEPLUGIN_BACKEND") or "cpu").strip().lower()
    return envelope(
        True,
        0,
        "OK",
        {
            "product": PRODUCT,
            "sdk_version": "1.0.0",
            "backend": name or "cpu",
        },
    )


@app.post("/api/activate")
def activate():
    raw = license_ux.decode_activate_body(request.get_data() or b"")
    if not raw:
        return envelope(False, -1, "Empty license", None)
    path = license_ux.save_license(ROOT, raw)
    res = sdk.activate(str(path))
    license_ux.remember_loaded(ROOT)
    mc = sdk.get_machine_code()
    if res != 0:
        return envelope(
            False, -1, "Invalid license", {"activated": False, "machinecode": mc}
        )
    sdk.init_sdk()
    return envelope(
        True, 0, "Successfully activated", {"activated": True, "machinecode": mc}
    )


@app.post("/api/documentLiveness")
def document_liveness():
    """Document authenticity / security checks (DocSDK Authenticity only)."""
    license_ux.reload_if_changed(ROOT, sdk.activate)
    data = request.get_json(silent=True) or {}
    images = data.get("images")
    if images is None and data.get("image") is not None:
        images = [data["image"]]
    options = data.get("options")
    if options is None and isinstance(data.get("response"), dict):
        options = {"response": data["response"]}
    return sdk_json(
        sdk.document_liveness(images or [], data.get("rfid") or "", options or None)
    )


@app.errorhandler(HTTPException)
def http_error(ex: HTTPException):
    if ex.code == 404:
        return envelope(False, -10, "Not found", None, 404)
    return envelope(False, -19, ex.description or str(ex), None, ex.code or 500)


@app.errorhandler(Exception)
def fail(ex: Exception):
    if isinstance(ex, HTTPException):
        return http_error(ex)
    return envelope(False, -19, str(ex), None, 500)


def main() -> None:
    license_ux.bootstrap(
        ROOT,
        get_machine_code=sdk.get_machine_code,
        activate=sdk.activate,
        init_sdk=sdk.init_sdk,
    )
    port = int(os.environ.get("PORT", os.environ.get("DOCSDK_PORT", str(DEFAULT_PORT))))
    host = os.environ.get("DOCSDK_BIND_HOST", "0.0.0.0")
    print("API listening on http://{0}:{1}".format(host, port))
    app.run(host=host, port=port, threaded=True)


if __name__ == "__main__":
    main()
