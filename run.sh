#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

# Runtime libs are not on GitHub — download into ./lib/cpu/ from:
LIB_DRIVE="https://drive.google.com/drive/folders/1_V05Nvcdc3WfOPuyquFyGIW-4CDj8aAm"

need_lib() {
  [[ -f lib/cpu/libDocSDK.so ]] || return 0
  [[ -f lib/cpu/libDocumentEngine.so ]] || return 0
  [[ -f lib/cpu/dcr.fpk ]] || return 0
  return 1
}

if need_lib; then
  echo "ERROR: ./lib/cpu/ is empty."
  echo "Download all files from Google Drive into ./lib/cpu/:"
  echo "  $LIB_DRIVE"
  exit 1
fi

export LICENSE="${LICENSE:-$(pwd)/license.txt}"
# Default API port 8086 (Docker and native use the same PORT).
export PORT="${PORT:-${DOCSDK_PORT:-8086}}"
exec python3 app.py
