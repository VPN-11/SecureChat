"""AES-GCM demo page."""

from __future__ import annotations

import streamlit as st

from crypto.aes import CryptoError, decrypt_message, encrypt_message, generate_aes_key, tamper_bytes
from ui.common import b64, info_panel, viva_expander


def render() -> None:
    st.header("AES-256-GCM Demonstration")
    st.markdown("AES-GCM provides fast symmetric encryption and detects tampering before plaintext is released.")

    info_panel(
        "How this page works",
        [
            "A fresh 256-bit AES key is generated for this demo session.",
            "Every encryption uses a new 12-byte nonce.",
            "The authentication tag proves the ciphertext, nonce, and key match.",
            "If the ciphertext or key is wrong, decryption fails safely.",
        ],
    )

    if st.button("Generate new AES key", use_container_width=True) or "aes_demo_key" not in st.session_state:
        st.session_state.aes_demo_key = generate_aes_key()
        st.session_state.pop("aes_result", None)

    show_key = st.toggle("Show AES key for classroom demonstration")
    if show_key:
        st.warning("This key is shown only for learning. Real applications must not expose secret keys.")
        st.code(st.session_state.aes_demo_key.hex(), language="text")

    plaintext = st.text_area("Plaintext message", "Hello Bob, AES-GCM protects this message.")
    if st.button("Encrypt message", type="primary", use_container_width=True):
        if plaintext:
            st.session_state.aes_result = encrypt_message(plaintext, st.session_state.aes_demo_key)
            st.success("Message encrypted with a fresh nonce.")
        else:
            st.error("Enter a non-empty plaintext message.")

    result = st.session_state.get("aes_result")
    if result:
        st.subheader("Encryption Output")
        st.text_input("Nonce (hex)", result.nonce.hex())
        st.text_area("Ciphertext (Base64)", b64(result.ciphertext), height=90)
        st.text_input("Authentication tag (hex)", result.tag.hex())

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Decrypt with correct key", use_container_width=True):
                try:
                    recovered = decrypt_message(result.ciphertext, result.tag, result.nonce, st.session_state.aes_demo_key)
                    st.success("Authentication passed. Plaintext recovered.")
                    st.code(recovered.decode("utf-8"), language="text")
                except CryptoError as exc:
                    st.error(str(exc))
        with col2:
            if st.button("Tamper ciphertext", use_container_width=True):
                try:
                    decrypt_message(tamper_bytes(result.ciphertext), result.tag, result.nonce, st.session_state.aes_demo_key)
                    st.error("Unexpected success.")
                except CryptoError as exc:
                    st.error(str(exc))
        with col3:
            if st.button("Try wrong key", use_container_width=True):
                try:
                    decrypt_message(result.ciphertext, result.tag, result.nonce, generate_aes_key())
                    st.error("Unexpected success.")
                except CryptoError as exc:
                    st.error(str(exc))

    st.subheader("Advantages and Limitations")
    st.markdown(
        "- AES-GCM is efficient and provides confidentiality plus integrity.\n"
        "- The nonce does not need to be secret, but it must be unique for a given key.\n"
        "- AES requires a shared secret key, so key distribution is a separate problem."
    )
    viva_expander(
        [
            ("Why does AES-GCM need a nonce?", "It makes each encryption unique and prevents dangerous key/stream reuse."),
            ("What happens when ciphertext is modified?", "The authentication tag check fails and plaintext is not returned."),
            ("Is AES symmetric or asymmetric?", "Symmetric, because the same secret key is used for encryption and decryption."),
        ]
    )

