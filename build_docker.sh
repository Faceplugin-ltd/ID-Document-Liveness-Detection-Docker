#!/usr/bin/env bash
# Build linux/amd64 image (runs on Linux / Windows / macOS Docker hosts).
set -euo pipefail
cd "$(dirname "$0")"
TAG="${1:-faceplugin/document-liveness:local}"

LIB_DRIVE="https://drive.google.com/drive/folders/1_V05Nvcdc3WfOPuyquFyGIW-4CDj8aAm"

if [[ ! -f lib/cpu/libDocSDK.so ]] \
  || [[ ! -f lib/cpu/libDocumentEngine.so ]] \
  || [[ ! -f lib/cpu/dcr.fpk ]]; then
  echo "ERROR: ./lib/cpu/ is incomplete (need libDocSDK.so, libDocumentEngine.so, and Drive data files)."
  echo "Download all files from Google Drive into ./lib/cpu/:"
  echo "  $LIB_DRIVE"
  exit 1
fi

docker build --platform linux/amd64 -t "$TAG" .
echo "Built $TAG (linux/amd64)"
