#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
PID_FILE="/tmp/redcalibur_api.pid"
LOG_FILE="/tmp/redcalibur_api.log"
VENV_BIN="$ROOT_DIR/.venv/bin"
PY="$VENV_BIN/python"

if [ ! -x "$PY" ]; then
  echo "Python venv not found at $PY. Create it and install deps first." >&2
  exit 1
fi

if [ -f "$PID_FILE" ] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
  echo "API already running with PID $(cat "$PID_FILE")." >&2
  exit 0
fi

cd "$ROOT_DIR"
# Load .env if present for environment variables
set -a
[ -f .env ] && source .env || true
set +a

nohup "$PY" -m uvicorn api.app:app --host 0.0.0.0 --port 8000 --workers 2 >"$LOG_FILE" 2>&1 & echo $! >"$PID_FILE"
echo "API started. PID $(cat "$PID_FILE"). Logs: $LOG_FILE"
