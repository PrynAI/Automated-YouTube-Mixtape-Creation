"""Step 2 page: configure transition and metadata options for generation."""

from __future__ import annotations

import streamlit as st

st.title("Step 2: Configure")

st.session_state.transition_ms = st.number_input(
    "Transition duration (ms)",
    min_value=0,
    max_value=60000,
    value=int(st.session_state.get("transition_ms", 6000)),
    step=500,
)

st.session_state.mixtape_name = st.text_input(
    "Mixtape title",
    value=st.session_state.get("mixtape_name", "Pryn House Mixtape"),
)

st.session_state.genre = st.text_input(
    "Genre",
    value=st.session_state.get("genre", "Pryn House"),
)

st.success("Configuration saved in session.")
