<div align="center">
<img alt="FacePlugin" src="https://raw.githubusercontent.com/Faceplugin-ltd/faceplugin-assets/main/brand/logo.png" width="400"/>
</div>

#### 🌐 Company Site - [Here](https://faceplugin.com)

#### 🤗 Hugging Face - [Here](https://huggingface.co/spaces/FacePlugin-Ltd/Liveness-Detection-SDK)

#### 🛟 Help Center - [Here](https://doc.faceplugin.com)

#### 🐳 Docker Hub - [Here](https://hub.docker.com/r/faceplugin/document-liveness)

# FacePlugin ID Document Liveness Detection SDK — Linux / Docker (Fully On-Premise)

> **Fastest:** `docker pull faceplugin/document-liveness:latest` → run → copy machine code → activate.  
> **Local Linux:** put runtime under `lib/cpu/` → `./run.sh` → activate.  
> **Docker Hub:** no Drive download. **Local:** Google Drive → `lib/cpu/` — see Option B.  
> **Try online:** [Hugging Face Space](https://huggingface.co/spaces/FacePlugin-Ltd/Liveness-Detection-SDK) (Gradio UI → your Linux API).  
> Jump: [Quick start](#quick-start) · [Start the API](#start-the-api) · [SDK License](#sdk-license) · [Company Overview](#company-overview) · [Setup](#setup-on-your-own-app) · [About SDK](#about-sdk) · [Contact](#contact)



## Quick start

- [ ] **Docker (recommended):** `docker pull faceplugin/document-liveness:latest` then `docker run` — [Option A](#option-a--docker-hub-no-drive-download)
- [ ] **Or local:** download CPU runtime into `lib/cpu/` — [Option B](#option-b--local-linux-runsh), then `./run.sh` — API on **8086**
- [ ] **Confirm it is running:** `curl -s http://127.0.0.1:8086/api/health` (no license needed yet)
- [ ] [Contact us](#contact) with your machine code to obtain a license key, then activate with `POST /api/activate` — [SDK License](#sdk-license)
- [ ] **Try it:** Postman, curl, or local Gradio demo on **9006** (`python3 demo`)

Docs: [https://doc.faceplugin.com](https://doc.faceplugin.com)


## Introduction

FacePlugin **ID Document Liveness Detection SDK for Linux / Docker** is a fully on-premise anti-spoofing engine for ID cards, passports, and driver licenses. It detects screen replay, printed copies, digital-source forgeries, portrait substitution, and other presentation attacks — with photo origin analysis, physical document verification, and security pattern checks.

All processing stays on your server. **No** biometric data is sent to FacePlugin cloud — built for KYC, eKYC, and remote identity verification that must stay private.

**Standalone repository** — pull Docker Hub (no Drive) or clone this repo, fill `lib/cpu/` from Google Drive, and run. No other FacePlugin repository is required.

**One repository** for Linux SDK + Docker. Native libraries are **linux/amd64**; the Docker image runs on Linux, Windows, and macOS hosts via Docker (Apple Silicon uses amd64 emulation).

**API server** in Docker — test with Postman, curl, or the local Gradio demo (`python3 demo`) covering Security verdicts and Raw JSON.

### Main Functionalities


| Feature                                         | Supported |
| ----------------------------------------------- | --------- |
| Document authenticity / liveness checks         | ✓         |
| Screen replay and digital-source detection      | ✓         |
| Printed copy and monochrome reproduction checks | ✓         |
| Security pattern and photo origin analysis      | ✓         |
| Front + back (multi-page)                       | ✓         |




### Product List


| Platform           | Repository                                                                                                                           |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| Android            | [ID-Document-Recognition-Android](https://github.com/Faceplugin-ltd/ID-Document-Recognition-Android)                                 |
| iOS                | [ID-Document-Recognition-iOS](https://github.com/Faceplugin-ltd/ID-Document-Recognition-iOS)                                         |
| Windows            | [ID-Document-Recognition-Windows](https://github.com/Faceplugin-ltd/ID-Document-Recognition-Windows)                                 |
| Linux / Docker     | [ID-Document-Recognition-Docker](https://github.com/Faceplugin-ltd/ID-Document-Recognition-Docker)                                   |
| React Native       | [ID-Document-Recognition-React-Native](https://github.com/Faceplugin-ltd/ID-Document-Recognition-React-Native)                       |
| Flutter            | [ID-Document-Recognition-Flutter](https://github.com/Faceplugin-ltd/ID-Document-Recognition-Flutter)                                 |
| Ionic Capacitor    | [ID-Document-Recognition-Ionic-Capacitor](https://github.com/Faceplugin-ltd/ID-Document-Recognition-Ionic-Capacitor)                 |
| Ionic Cordova      | [ID-Document-Recognition-Ionic-Cordova](https://github.com/Faceplugin-ltd/ID-Document-Recognition-Ionic-Cordova)                     |
| **Linux / Docker** | **[ID-Document-Liveness-Detection-Docker](https://github.com/Faceplugin-ltd/ID-Document-Liveness-Detection-Docker)** (**this repo**) |


---



## Before you start


| Step | What you need                                                                                                                                                                                                                      |
| ---- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | A Linux host **or** Docker (Desktop or Engine)                                                                                                                                                                                     |
| 2    | **Docker:** Hub pull only (no Drive). **Local:** Google Drive → `lib/cpu/` — [Option B](#option-b--local-linux-runsh)
| 3    | You do not need a license to start the API the first time. Copy the machine code from the logs or `GET /api/machinecode`. Send it to FacePlugin ([contact](#contact)) to get license key and unlock product endpoints. |


You do **not** need a license to start the API once. Product endpoints unlock after you activate.

### System requirements


| Item | Minimum                | Recommended          |
| ---- | ---------------------- | -------------------- |
| CPU  | 2 cores                | 4 cores              |
| RAM  | 4 GB                   | 8 GB                 |
| Disk | 4 GB                   | 8 GB                 |
| OS   | Ubuntu 20.04+ (x86_64) | Ubuntu 22.04 / 24.04 |
| GPU  | —                      | — (CPU-only product) |


---



## Start the API

You can start **without** a license — the server prints your machine code on startup.

The API starts even if activation fails. Copy the **machine code** from the log and send it to FacePlugin.



### Option A — Docker Hub (no Drive download)

Runtime is already inside the image. No Google Drive step.

```bash
sudo docker pull faceplugin/document-liveness:latest
sudo docker run -d --name faceplugin-document-liveness \
  --shm-size=2gb --privileged \
  -p 8086:8086 \
  -v /etc/machine-id:/etc/machine-id:ro \
  faceplugin/document-liveness:latest
sudo docker logs -f faceplugin-document-liveness
# Look for the machine code line in the logs
```

`--shm-size=2gb` is required (`dcr.fpk` extracts to `/dev/shm`). Keep `--privileged` and the `/etc/machine-id` volume as shown.

On Docker Desktop (macOS/Windows) omit the `/etc/machine-id` volume.

### Run multiple containers

To run multiple containers on one Linux host with a shared machine code / license, see the docs:

[https://doc.faceplugin.com/id-document-liveness-sdk/server-sdk/id-document-liveness-linux-sdk#run-multiple-containers](https://doc.faceplugin.com/id-document-liveness-sdk/server-sdk/id-document-liveness-linux-sdk#run-multiple-containers)

### Option B — Local Linux (`./run.sh`)

Requires the Google Drive runtime under `lib/cpu/`. Needs glibc **2.38+** (for example Ubuntu 24.04).

#### Get the runtime

The `./lib/cpu/` tree is empty on GitHub because native binaries and model files are too large. This product is **CPU-only**.

**[Document Liveness Linux runtime (Google Drive)](https://drive.google.com/drive/folders/1_V05Nvcdc3WfOPuyquFyGIW-4CDj8aAm)**

1. Clone the repo (if you have not already):

```bash
git clone https://github.com/Faceplugin-ltd/ID-Document-Liveness-Detection-Docker.git
cd ID-Document-Liveness-Detection-Docker
```

2. Open the Google Drive folder above.
3. Download **all files** in that folder.
4. Put every file **directly** into `./lib/cpu/` — not inside a nested subfolder.

```text
ID-Document-Liveness-Detection-Docker/
└── lib/
    └── cpu/
        ├── libDocSDK.so
        ├── libDocumentEngine.so
        ├── dcr.fpk
        └── ... (other runtimes from Drive)
```

Wrong layout: `lib/cpu/SomeFolder/libDocSDK.so`.

```bash
ls lib/cpu/libDocSDK.so
ls lib/cpu/libDocumentEngine.so
ls lib/cpu/dcr.fpk
```

#### Run

```bash
pip3 install -r requirements.txt
./run.sh
```

API: **http://127.0.0.1:8086**

Copy the **machine code** from the terminal (or `GET /api/machinecode`), then activate with `POST /api/activate` or paste the license key when prompted.


## SDK License

Licenses are **offline** and bound to your machine code.

1. **Start the server** ([above](#start-the-api)) with Docker Hub or local `./run.sh`. A license is not required for the first start.
2. **Copy the machine code** from the startup log. Copy it from the logs or `GET /api/machinecode`.
3. **Send that machine code** to FacePlugin ([contact](#contact)). We will issue a license key for that code.
4. **Activate** with the license key:

```bash
# Paste the license key into ./license.txt (overwrite the file).

# Detached Docker will not re-read license.txt on its own — POST the key:
curl -s -X POST http://127.0.0.1:8086/api/activate \
  -H 'Content-Type: text/plain' \
  --data-binary @license.txt

```



Use the machine code from the environment you will run in production. **Docker and local host codes are different** — if you run in Docker, send the Docker machine code.

### License capabilities (Liveness)

After activation, `GET /api/licenseStatus` reports what the key unlocks. The Gradio demo shows the same summary as **License: …** at the top of the page.


| Capability                  | Meaning                                                                                                        |
| --------------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Liveness** (authenticity) | Document authenticity: physical document, security patterns, photo origin, digital source, printed-copy checks |


This product is **document liveness / authenticity only**. OCR, MRZ, and barcode recognition are not exposed here. Use a license that includes **Liveness** (authenticity).

Check status anytime:

```bash
curl -s http://127.0.0.1:8086/api/licenseStatus
```

`POST /api/documentLiveness` always requests `"Authenticity": "normal"` (OCR / MRZ / Barcode off).

## Try it



### Health

```bash
curl -s http://127.0.0.1:8086/api/health
```



### Documentation

[https://doc.faceplugin.com](https://doc.faceplugin.com)

### Postman

Import `[postman/DocumentLiveness-API.postman_collection.json](postman/DocumentLiveness-API.postman_collection.json)`.

Default base URL: `http://127.0.0.1:8086`

Canonical protocol: `/api/*`. No version segment in route paths.

### Demo UI (Gradio) — local only

The Docker image is **API/SDK server only** (no Gradio). For a local FacePlugin ID Document Liveness demo in the browser — Security verdicts and Raw JSON — on the host (API must already be running on port 8086):

```bash
pip3 install -r requirements-demo.txt
./run_demo.sh
```

Or:

```bash
pip3 install -r requirements-demo.txt
DEMO_PORT=9006 API_BASE=http://127.0.0.1:8086 python3 demo
```

Open **[http://127.0.0.1:9006](http://127.0.0.1:9006)**. Examples when present: `assets/examples/samples/`. The header shows **License:** from `/api/licenseStatus`.





- **Security** — overall and per-page authenticity: photo origin, physical document, digital source, printed-copy checks (needs a Liveness-capable license)
- **Raw JSON** — full `/api/documentLiveness` response for integration

---



## Setup on your own app

Two paths. You do **not** need the Gradio demo in production.

**HTTP** (any language) — start the API (Option A above), then call:

```bash
curl -s -X POST http://127.0.0.1:8086/api/documentLiveness \
  -H 'Content-Type: application/json' \
  -d '{"images":[{"image":"<BASE64>"}]}'
```

**Python in-process** — keep `lib/cpu/` beside `[sdk.py](sdk.py)`:

```python
import sdk

machine_code = sdk.get_machine_code()  # machine code
sdk.activate("license.txt")
sdk.init_sdk()
result = sdk.document_liveness([{"image": base64_front}])
```

---



## About SDK

Use the Python bindings in `[sdk.py](sdk.py)`. Return code `0` means success.

```python
import sdk

machine_code = sdk.get_machine_code()
print("machineCode:", machine_code)  # machine code

ret = sdk.activate("license.txt")
ret = sdk.init_sdk()

result = sdk.document_liveness([{"image": base64_front}])

# Front + back
result = sdk.document_liveness(
    [
        {"image": base64_front, "page_idx": 0},
        {"image": base64_back, "page_idx": 1},
    ],
)
print(sdk.get_license_status())  # authenticity flag + label
```

HTTP endpoints: `/api/health`, `/api/machinecode`, `/api/licenseStatus`, `/api/backend`, `/api/activate`, `/api/documentLiveness`.

## Company Overview

**FacePlugin** builds **on-premises biometric AI SDKs** for **face recognition**, **face liveness detection** (presentation-attack detection), **deepfake detection**, **ID document recognition** (OCR / MRZ / barcode), **ID document liveness**, and full **eKYC / identity verification** workflows.

Deploy on your own servers, private cloud, or fully on-device. **Biometric data never leaves your infrastructure.** Face matching is **NIST FRVT**-evaluated; liveness targets **iBeta Level 2** class PAD. License once for **unlimited on-prem inference** — **no per-call fees**.

- Website: [faceplugin.com](https://faceplugin.com)
- Docs: [doc.faceplugin.com](https://doc.faceplugin.com)
- Hugging Face demo: [Liveness-Detection-SDK](https://huggingface.co/spaces/FacePlugin-Ltd/Liveness-Detection-SDK)
- Docker Hub: [faceplugin/document-liveness](https://hub.docker.com/r/faceplugin/document-liveness)



## Contact

Request a license, machine-code activation (machine code → license key), or integration help:

   