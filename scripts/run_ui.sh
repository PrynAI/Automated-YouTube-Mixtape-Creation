#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root and expose it via PYTHONPATH for Streamlit page imports.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Start Streamlit multipage UI.
PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH:-}" streamlit run app/ui/streamlit_app.py --server.port 8501
