"""SHA-256 demo page."""

from __future__ import annotations

import streamlit as st

from crypto.hashing import sha256_hex
from ui.common import info_panel, viva_expander


def render() -> None:
    st.header("SHA-256 Hashing Demonstration")
    st.markdown("SHA-256 creates a fixed-size digest. It is one-way and is not encryption.")

    info_panel(
        "What to observe",
        [
            "The same input always gives the same digest.",
            "A tiny input change normally creates a very different digest.",
            "A plain hash alone does not prove who created a message.",
        ],
    )

    original = st.text_area("Original message", "The exam starts at 10 AM.")
    modified = st.text_area("Modified message", "The exam starts at 10 PM.")

    original_hash = sha256_hex(original)
    modified_hash = sha256_hex(modified)

    st.subheader("Digest Comparison")
    st.text_input("Original SHA-256 digest", original_hash)
    st.text_input("Modified SHA-256 digest", modified_hash)
    if original_hash == modified_hash:
        st.warning("The digests match because the messages are identical.")
    else:
        st.success("The digests differ. The message content changed.")

    st.subheader("Advantages and Limitations")
    st.markdown(
        "- Hashing is useful for integrity checks and fingerprints.\n"
        "- Hashing is one-way; it does not decrypt back to the original text.\n"
        "- A plain hash is not a digital signature and does not authenticate the sender."
    )
    viva_expander(
        [
            ("Is SHA-256 encryption?", "No. It is a one-way hash function."),
            ("How long is a SHA-256 digest?", "256 bits, usually displayed as 64 hexadecimal characters."),
            ("Does a hash prove Alice sent a message?", "No. Anyone can hash a message; signatures or MACs are needed for authenticity."),
        ]
    )

