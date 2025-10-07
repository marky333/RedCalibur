#!/usr/bin/env bash
set -euo pipefail

PID_FILE="/tmp/redcalibur_api.pid"

if [ ! -f "$PID_FILE" ]; then
  echo "No PID file at $PID_FILE. Is the API running?" >&2
  exit 0
fi

PID=$(cat "$PID_FILE")
if kill -0 "$PID" 2>/dev/null; then
  kill "$PID" || true
  sleep 1
  if kill -0 "$PID" 2>/dev/null; then
    kill -9 "$PID" || true
  fi
  echo "Stopped API (PID $PID)."
else
  echo "Process $PID not running. Cleaning up PID file."
fi
rm -f "$PID_FILE"
