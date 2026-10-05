<div align="center">
<img alt="FacePlugin" src="https://raw.githubusercontent.com/Faceplugin-ltd/faceplugin-assets/main/brand/logo.png" width="400"/>
</div>

#### 🌐 Company Site - [Here](https://faceplugin.com)

#### 🤗 Hugging Face - [Here](https://huggingface.co/spaces/FacePlugin-Ltd/Liveness-Detection-SDK)

#### 📚 Help Center - [Here](https://doc.faceplugin.com)

#### 🐳 Docker Hub - [Here](https://hub.docker.com/r/faceplugin/document-liveness)

# FacePlugin ID Document Liveness Detection SDK — Linux / Docker (Fully On-Premise)

## Quick start

- **Docker (recommended):** `docker pull faceplugin/document-liveness:latest` then `docker run` — [Option A](#option-a--docker-hub)
- **Or local:** download CPU runtime into `lib/cpu/` — [Option B](#option-b-local-linux-runsh), then `./run.sh` — API on **8086**
- **Confirm it is running:** `curl -s http://127.0.0.1:8086/api/health` (no license needed yet)
- [Contact us](#contact) with your machine code to obtain a license key, then activate with `POST /api/activate` — [Activate your license](#activate-your-license)
- **Try it:** Postman, curl, or local Gradio demo on **9006** (`python3 demo`)

Docs: [doc.faceplugin.com](https://doc.faceplugin.com)\
Try online: [Hugging Face Space](https://huggingface.co/spaces/FacePlugin-Ltd/Liveness-Detection-SDK)


## Introduction

**FacePlugin ID Document Liveness Detection SDK** is an on-premise document anti-spoofing engine for Linux and Docker. It verifies that an ID card, passport, or driver's license is a real physical document and detects presentation attacks such as screen replays, printed copies, digitally generated forgeries, and portrait substitution.

The SDK combines photo origin analysis, physical document verification, and security pattern checks to support **KYC, eKYC, and remote identity verification** workflows. All processing runs on your own server, and **no images or biometric data are ever sent to FacePlugin**.

The SDK runs as a REST API server on Linux (x86_64), or through Docker on Linux, Windows, and macOS. This repository is self-contained, with no other FacePlugin repository required.

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

## Start the API

You do **not** need a license to start the API. The server prints your machine code on startup, which you'll need to [activate your license](#activate-your-license). Product endpoints unlock after you activate.

### Option A — Docker Hub

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

### Option B: Local Linux (`./run.sh`)

This option runs the server directly on your machine. It requires glibc **2.38 or newer** (for example, Ubuntu 24.04). Check your version with `ldd --version`. No GPU is needed; this product runs on CPU only.

#### 1. Clone the repository

```bash
git clone https://github.com/Faceplugin-ltd/ID-Document-Liveness-Detection-Docker.git
cd ID-Document-Liveness-Detection-Docker
```

#### 2. Download the runtime

The `lib/cpu/` folder is empty on GitHub because the native libraries and model files are too large to host there.

1. Open the [Document Liveness Linux runtime folder on Google Drive](https://drive.google.com/drive/folders/1_V05Nvcdc3WfOPuyquFyGIW-4CDj8aAm).
2. Download every file in the folder.
3. Place the files **directly** in `lib/cpu/`, not in a subfolder.

Your project should look like this:

```text
ID-Document-Liveness-Detection-Docker/
└── lib/
    └── cpu/
        ├── libDocSDK.so
        ├── libDocumentEngine.so
        ├── dcr.fpk
        └── ... (remaining files from Google Drive)
```

> ⚠️ If Google Drive gives you a zip, extract it and move the files up so you don't end up with `lib/cpu/SomeFolder/libDocSDK.so`.

#### 3. Install dependencies and run

```bash
pip3 install -r requirements.txt
./run.sh
```

The API starts at **http://127.0.0.1:8086**, and the machine code is printed in the terminal. Continue with [Activate your license](#activate-your-license).

## Activate your license

Licenses work **offline** and are tied to the machine code of the environment where the server runs.

> ⚠️ **Docker and local installs have different machine codes.** Get the machine code from the same environment you'll use in production. If you'll run in Docker, send the code from the Docker container, not from the host.

1. **Start the server** using Docker Hub or `./run.sh` (see [Start the API](#start-the-api)). You don't need a license for the first start.
2. **Get your machine code.** It's printed in the startup log, or you can fetch it with `GET /api/machinecode`.
3. **Send the machine code to FacePlugin** ([contact us](#contact)). We'll reply with a license key for that machine code.
4. **Activate the license.** Save the license key to `license.txt` in the project root, replacing anything already in the file. Then send it to the running server:

   ```bash
   curl -s -X POST http://127.0.0.1:8086/api/activate \
     -H 'Content-Type: text/plain' \
     --data-binary @license.txt
   ```

   If you run in Docker, this command is required, because detached containers don't re-read `license.txt` after they start. The same command also works with `./run.sh`.

## Try it

### Health

```bash
curl -s http://127.0.0.1:8086/api/health
```

### Postman

Import [`postman/DocumentLiveness-API.postman_collection.json`](postman/DocumentLiveness-API.postman_collection.json).

Default base URL: `http://127.0.0.1:8086`


### Demo UI (Gradio) — local only

The Docker image includes only the API server, not the demo UI. To view results in your browser, run the Gradio demo on your own machine. Make sure the API is already running on port 8086 first.

```bash
pip3 install -r requirements-demo.txt
./run_demo.sh
```

Or:

```bash
pip3 install -r requirements-demo.txt
DEMO_PORT=9006 API_BASE=http://127.0.0.1:8086 python3 demo
```

Open **[http://127.0.0.1:9006](http://127.0.0.1:9006)** in your browser. Sample images, if included, are in `assets/examples/samples/`. The page header shows your current license status, taken from `/api/licenseStatus`.

- **Security** — overall and per-page authenticity: photo origin, physical document, digital source, printed-copy checks (needs a Liveness-capable license)
- **Raw JSON** — full `/api/documentLiveness` response for integration

---

## Setup on your own app

Two paths. You do **not** need the Gradio demo in production.

**HTTP** (any language) — start the API (see [Start the API](#start-the-api)), then call:

```bash
curl -s -X POST http://127.0.0.1:8086/api/documentLiveness \
  -H 'Content-Type: application/json' \
  -d '{"images":[{"image":"<BASE64>"}]}'
```

**Python in-process** — keep `lib/cpu/` beside [`sdk.py`](sdk.py) and call the SDK directly. See [About SDK](#about-sdk).

---

## About SDK

Use the Python bindings in [`sdk.py`](sdk.py). Return code `0` means success.

```python
import sdk

machine_code = sdk.get_machine_code()
print("machineCode:", machine_code)

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


## Contact

Request a license, machine-code activation (machine code → license key), or integration help:

<div align="left">
<a target="_blank" href="mailto:info@faceplugin.com"><img src="https://img.shields.io/badge/email-info@faceplugin.com-blue.svg?logo=gmail" alt="faceplugin.com"></a>&emsp;
<a target="_blank" href="https://t.me/FacePluginSupport"><img src="https://img.shields.io/badge/telegram-@FacePluginSupport-blue.svg?logo=telegram" alt="Telegram @FacePluginSupport"></a>&emsp;
<a target="_blank" href="https://wa.me/+14692784822"><img src="https://img.shields.io/badge/whatsapp-faceplugin-blue.svg?logo=whatsapp" alt="faceplugin.com"></a>
</div>
