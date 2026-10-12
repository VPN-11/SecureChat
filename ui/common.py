"""Shared Streamlit UI helpers."""

from __future__ import annotations

import base64

import streamlit as st

from crypto.rsa import generate_rsa_key_pair


def ensure_keys() -> None:
    """Create session-scoped RSA keys for Alice and Bob."""

    if "alice_key_pair" not in st.session_state:
        st.session_state.alice_key_pair = generate_rsa_key_pair()
    if "bob_key_pair" not in st.session_state:
        st.session_state.bob_key_pair = generate_rsa_key_pair()


def reset_keys_button() -> None:
    """Render a button that refreshes Alice and Bob keys."""

    if st.sidebar.button("Regenerate Alice and Bob RSA keys", use_container_width=True):
        st.session_state.alice_key_pair = generate_rsa_key_pair()
        st.session_state.bob_key_pair = generate_rsa_key_pair()
        st.sidebar.success("New in-memory RSA keys generated.")


def b64(data: bytes) -> str:
    """Base64 encode bytes for display."""

    return base64.b64encode(data).decode("ascii")


def from_hex(value: str, field_name: str) -> bytes | None:
    """Parse hex from Streamlit text inputs and show a friendly error."""

    try:
        return bytes.fromhex(value.strip())
    except ValueError:
        st.error(f"{field_name} must be valid hexadecimal text.")
        return None


def info_panel(title: str, items: list[str]) -> None:
    """Render a compact educational panel."""

    st.markdown(f"#### {title}")
    for item in items:
        st.markdown(f"- {item}")


def viva_expander(questions: list[tuple[str, str]]) -> None:
    """Render a short viva section."""

    with st.expander("Viva questions for this page"):
        for question, answer in questions:
            st.markdown(f"**Q. {question}**")
            st.markdown(f"A. {answer}")

