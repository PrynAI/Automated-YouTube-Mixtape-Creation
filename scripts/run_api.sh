#!/usr/bin/env bash
set -euo pipefail

# Start FastAPI with auto-reload for local development.
uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
