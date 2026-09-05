"""Gradio UI — HTTP client for the ID Document Liveness Detection Flask API.

Local only. Start the API first (``./run.sh``), then ``python3 demo``.
Security / authenticity checks only (no OCR / MRZ / Result / Images tabs).
"""

from __future__ import annotations

import base64
import json
import os
from pathlib import Path

import gradio as gr
import requests

import ui
from security_view import security_view_from_payload

APP_ROOT = Path(__file__).resolve().parent.parent
SAMPLES = APP_ROOT / "assets" / "examples" / "samples"
API = os.environ.get(
    "API_BASE",
    f"http://127.0.0.1:{os.environ.get('PORT', os.environ.get('DOCSDK_PORT', '8086'))}",
).rstrip("/")
DEMO_PORT = int(os.environ.get("DEMO_PORT", "9006"))
_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def _fetch_license_status() -> dict:
    try:
        r = requests.get(f"{API}/api/licenseStatus", timeout=5)
        body = r.json() if r.ok else {}
        data = body.get("data") if isinstance(body, dict) else None
        return data if isinstance(data, dict) else {}
    except Exception:  # noqa: BLE001
        return {}


def _license_banner_md(status: dict | None = None) -> str:
    st = status if status is not None else _fetch_license_status()
    label = str(st.get("label") or "").strip()
    if not label:
        if st.get("licensed"):
            label = str(st.get("levelName") or "Licensed")
        else:
            label = "Not licensed / unavailable"
    return f"**License:** {label}"


def _b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def _list_images() -> list[Path]:
    if not SAMPLES.is_dir():
        return []
    return sorted(
        p for p in SAMPLES.iterdir() if p.is_file() and p.suffix.lower() in _IMAGE_SUFFIXES
    )


def _document_examples() -> list[list[str | None]]:
    files = {p.name: p for p in _list_images()}
    pairs: list[list[str | None]] = []
    used: set[str] = set()
    for path in sorted(files.values()):
        if "_front" not in path.stem:
            continue
        base = path.stem.rsplit("_front", 1)[0]
        back = None
        for suf in _IMAGE_SUFFIXES:
            cand = files.get(f"{base}_back{suf}")
            if cand:
                back = cand
                break
        pairs.append([str(path), str(back) if back else None])
        used.add(path.name)
        if back:
            used.add(back.name)
    for path in _list_images():
        if path.name not in used:
            pairs.append([str(path), None])
    return pairs


def check_liveness(front, back):
    empty: list[list[str]] = []
    lic = _fetch_license_status()
    if not front:
        return ("**Error:** Front image required.", empty, "")

    if lic and not lic.get("authenticity") and not lic.get("licensed"):
        return (
            "**Note:** License unavailable — security checks will not run.\n\n"
            "**Error:** Activate a Liveness-capable license first.",
            empty,
            "",
        )

    images = [{"image": _b64(front), "page_idx": 0}]
    if back:
        images.append({"image": _b64(back), "page_idx": 1})

    try:
        r = requests.post(
            f"{API}/api/documentLiveness",
            json={"images": images},
            timeout=180,
        )
    except Exception as ex:  # noqa: BLE001
        return (f"**Request failed:** {ex}", empty, "")

    try:
        payload = r.json()
    except Exception:  # noqa: BLE001
        return (f"**Invalid JSON** (HTTP {r.status_code})", empty, r.text or "")

    if not isinstance(payload, dict):
        return (
            "**Unexpected response shape.**",
            empty,
            json.dumps(payload, indent=2),
        )

    sec_summary, sec_rows = security_view_from_payload(payload)
    prefix: list[str] = []
    if lic and not lic.get("authenticity"):
        prefix.append(
            "**Note:** Liveness is **not available** on this license — "
            "security checks may be empty / not checked."
        )
    lic_err = str(payload.get("licenseError") or "").strip()
    if lic_err:
        prefix.append(f"**License:** {lic_err}")
    if prefix:
        sec_summary = "\n\n".join(prefix) + "\n\n" + sec_summary
    return (sec_summary, sec_rows, json.dumps(payload, indent=2))


def main() -> None:
    examples = _document_examples()
    with gr.Blocks(title="ID Document Liveness Detection Demo") as demo:
        gr.Markdown(
            "# FacePlugin ID Document Liveness Detection — Demo\n"
            "Upload a document image and click **Check Security**."
        )
        license_md = gr.Markdown(value=_license_banner_md())
        with gr.Row():
            with gr.Column():
                front = gr.Image(type="filepath", label="Front")
                back = gr.Image(type="filepath", label="Back (optional)")
                if examples:
                    gr.Examples(examples, inputs=[front, back], label="Examples")
                btn = gr.Button("Check Security", variant="primary")
            with gr.Column():
                with gr.Tabs():
                    with gr.Tab("Security"):
                        sec_summary = gr.Markdown(
                            value="*Run Check Security to see authenticity checks.*"
                        )
                        sec_table = ui.result_dataframe(
                            headers=["Page", "Check", "Status"],
                            label="Security by page",
                        )
                    with gr.Tab("Raw JSON"):
                        raw = gr.Code(language="json", label="API response")
        btn.click(
            check_liveness,
            inputs=[front, back],
            outputs=[sec_summary, sec_table, raw],
        )
        btn.click(lambda: _license_banner_md(), outputs=[license_md])
        demo.load(lambda: _license_banner_md(), outputs=[license_md])

    print(f"Gradio demo -> http://127.0.0.1:{DEMO_PORT}  (API {API})")
    demo.launch(server_name="0.0.0.0", server_port=DEMO_PORT, css=ui.RESULT_CSS)
