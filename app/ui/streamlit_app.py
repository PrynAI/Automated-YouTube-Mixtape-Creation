"""Streamlit entrypoint that initializes global session state for the UI."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# Ensure absolute imports (`from app...`) work when Streamlit executes pages as scripts.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

st.set_page_config(
    page_title="Automated YouTube Mixtape Creator",
    page_icon="🎛️",
    layout="wide",
)

# Shared session keys used across multipage UI flow.
if "audio_payloads" not in st.session_state:
    st.session_state.audio_payloads = []
if "image_payload" not in st.session_state:
    st.session_state.image_payload = None
if "job_id" not in st.session_state:
    st.session_state.job_id = None
if "job_status" not in st.session_state:
    st.session_state.job_status = None
if "transition_ms" not in st.session_state:
    st.session_state.transition_ms = 6000
if "mixtape_name" not in st.session_state:
    st.session_state.mixtape_name = "Pryn House Mixtape"
if "genre" not in st.session_state:
    st.session_state.genre = "Pryn House"

st.title("Automated YouTube Mixtape Creator")
st.write("Use the pages in the left sidebar: Upload → Configure → Generate → Results.")
st.info("Run FastAPI first, then use this UI to submit jobs and fetch outputs.")
