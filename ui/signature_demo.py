"""RSA-PSS signature demo page."""

from __future__ import annotations

import streamlit as st

from crypto.rsa import generate_rsa_key_pair, public_key_summary
from crypto.signatures import sign_message, verify_signature
from ui.common import b64, ensure_keys, info_panel, viva_expander


def render() -> None:
    ensure_keys()
    st.header("RSA-PSS Digital Signature Demonstration")
    st.markdown("A digital signature proves that a message matches Alice's private key and has not changed.")

    alice = st.session_state.alice_key_pair
    info_panel(
        "Signature sequence",
        [
            "Alice signs the message with her private key.",
            "Bob verifies the signature with Alice's public key.",
            "Changing the message or using the wrong public key makes verification fail.",
            "The signature does not hide the message; encryption is a separate operation.",
        ],
    )

    st.subheader("Alice's Public Key Summary")
    st.json(public_key_summary(alice.public_key))

    message = st.text_area("Message to sign", "I, Alice, approve this SecureChat demo.")
    if st.button("Sign with Alice's private key", type="primary", use_container_width=True):
        if message:
            st.session_state.signature_message = message
            st.session_state.signature_bytes = sign_message(message, alice.private_key)
            st.success("Message signed with RSA-PSS.")
        else:
            st.error("Enter a message before signing.")

    signature = st.session_state.get("signature_bytes")
    if signature:
        signed_message = st.session_state.signature_message
        st.text_area("Signature (Base64)", b64(signature), height=120)
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Verify correct message", use_container_width=True):
                if verify_signature(signed_message, signature, alice.public_key):
                    st.success("Signature is valid for Alice's public key.")
                else:
                    st.error("Signature verification failed.")
        with col2:
            if st.button("Modify message and verify", use_container_width=True):
                modified = signed_message + " Modified."
                if verify_signature(modified, signature, alice.public_key):
                    st.error("Unexpected success.")
                else:
                    st.error("Verification failed because the message changed.")
        with col3:
            if st.button("Verify with unrelated public key", use_container_width=True):
                unrelated = generate_rsa_key_pair()
                if verify_signature(signed_message, signature, unrelated.public_key):
                    st.error("Unexpected success.")
                else:
                    st.error("Verification failed because this is not Alice's public key.")

    st.subheader("What a signature does and does not prove")
    st.markdown(
        "- It proves the message matches a private key corresponding to Alice's public key.\n"
        "- It does not encrypt or hide the message.\n"
        "- Real-world identity depends on trusting the public-key binding through certificates or another trust process."
    )
    viva_expander(
        [
            ("What padding is used for signatures here?", "RSA-PSS with SHA-256."),
            ("Can a signature provide confidentiality?", "No. It provides authenticity and integrity, not secrecy."),
            ("Why must Bob trust Alice's public key?", "Otherwise an attacker could substitute a different public key."),
        ]
    )

