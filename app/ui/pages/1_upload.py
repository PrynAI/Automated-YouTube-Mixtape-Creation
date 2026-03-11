"""Step 1 page: collect audio tracks and optional cover image from users."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# Ensure absolute imports (`from app...`) work when Streamlit executes this page directly.
PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.ui.components.upload_widget import render_upload_widget

st.title("Step 1: Upload")
render_upload_widget()

if st.session_state.get("audio_payloads"):
    st.write("Loaded audio files:")
    for item in st.session_state.audio_payloads:
        st.write(f"- {item['name']}")

if st.session_state.get("image_payload"):
    st.write(f"Loaded image: {st.session_state.image_payload['name']}")
