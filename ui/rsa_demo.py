"""RSA-OAEP demo page."""

from __future__ import annotations

import streamlit as st

from crypto.aes import CryptoError, generate_aes_key
from crypto.rsa import decrypt_aes_key, encrypt_aes_key, export_public_key_pem, generate_rsa_key_pair, public_key_summary
from ui.common import b64, ensure_keys, info_panel, viva_expander


def render() -> None:
    ensure_keys()
    st.header("RSA-OAEP Public-Key Demonstration")
    st.markdown("RSA lets Alice encrypt a small session key using Bob's public key. Only Bob's private key can unwrap it.")

    bob = st.session_state.bob_key_pair
    alice = st.session_state.alice_key_pair

    info_panel(
        "Important terms",
        [
            "Public key: safe to share; used here to encrypt the AES key.",
            "Private key: must remain secret; used here to decrypt the AES key.",
            "OAEP: modern RSA encryption padding that protects against several classic attacks.",
            "RSA is not used here for long messages because it is slower and has strict size limits.",
        ],
    )

    st.subheader("Bob's Public Key Information")
    st.json(public_key_summary(bob.public_key))
    with st.expander("Export Bob's public key"):
        st.code(export_public_key_pem(bob.public_key), language="text")

    if st.button("Generate AES key and encrypt for Bob", type="primary", use_container_width=True):
        aes_key = generate_aes_key()
        st.session_state.rsa_demo_aes_key = aes_key
        st.session_state.rsa_demo_encrypted_key = encrypt_aes_key(aes_key, bob.public_key)
        st.success("AES key encrypted with Bob's RSA public key.")

    encrypted_key = st.session_state.get("rsa_demo_encrypted_key")
    if encrypted_key:
        st.text_area("Encrypted AES key (Base64)", b64(encrypted_key), height=120)
        show_aes = st.toggle("Show raw AES key for classroom comparison")
        if show_aes:
            st.warning("This is normally secret and is shown only to prove RSA recovered the same key.")
            st.code(st.session_state.rsa_demo_aes_key.hex(), language="text")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Decrypt with Bob's private key", use_container_width=True):
                try:
                    recovered = decrypt_aes_key(encrypted_key, bob.private_key)
                    st.success("Bob recovered the AES session key.")
                    st.code(recovered.hex(), language="text")
                except CryptoError as exc:
                    st.error(str(exc))
        with col2:
            if st.button("Try Alice's private key instead", use_container_width=True):
                try:
                    decrypt_aes_key(encrypted_key, alice.private_key)
                    st.error("Unexpected success.")
                except CryptoError as exc:
                    st.error(str(exc))

    viva_expander(
        [
            ("Why encrypt only the AES key with RSA?", "RSA is slower and can encrypt only small payloads, so it is used to protect a fast symmetric key."),
            ("Which key must Bob keep secret?", "Bob's private key."),
            ("Can everyone know Bob's public key?", "Yes, but they must trust that it really belongs to Bob."),
        ]
    )

