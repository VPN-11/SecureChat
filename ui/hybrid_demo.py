"""Hybrid encryption demo page."""

from __future__ import annotations

import streamlit as st

from crypto.aes import CryptoError, tamper_bytes
from crypto.hybrid import HybridPacket, decrypt_from_alice, encrypt_for_bob
from crypto.rsa import generate_rsa_key_pair
from ui.common import ensure_keys, info_panel, viva_expander


def render() -> None:
    ensure_keys()
    st.header("Hybrid Encryption Workflow")
    st.markdown("This is the complete Alice-to-Bob flow: AES-GCM protects the message, RSA-OAEP protects the AES key.")

    info_panel(
        "Public vs secret data",
        [
            "Public in the packet: encrypted AES key, nonce, ciphertext, authentication tag, and algorithm names.",
            "Secret: raw AES key, Bob's private key, and original plaintext before Bob decrypts it.",
            "The packet is safe to display because it does not contain the raw message or private keys.",
        ],
    )

    message = st.text_area("Alice's message", "Hi Bob, the project demo is ready.")
    if st.button("Create secure packet for Bob", type="primary", use_container_width=True):
        if message:
            st.session_state.hybrid_result = encrypt_for_bob(message, st.session_state.bob_key_pair.public_key)
            st.success("Packet created. Plaintext and raw AES key are not included in the packet.")
        else:
            st.error("Enter a message before creating the packet.")

    result = st.session_state.get("hybrid_result")
    if result:
        packet = result.packet
        st.subheader("Simulated Network Packet")
        st.json(packet.as_display_dict())

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Bob decrypts packet", use_container_width=True):
                try:
                    recovered = decrypt_from_alice(packet, st.session_state.bob_key_pair.private_key)
                    st.success("Bob recovered and authenticated the message.")
                    st.code(recovered.decode("utf-8"), language="text")
                except CryptoError as exc:
                    st.error(str(exc))
        with col2:
            if st.button("Tamper packet ciphertext", use_container_width=True):
                tampered = HybridPacket(
                    algorithm=packet.algorithm,
                    key_encryption=packet.key_encryption,
                    encrypted_aes_key=packet.encrypted_aes_key,
                    nonce=packet.nonce,
                    ciphertext=tamper_bytes(packet.ciphertext),
                    tag=packet.tag,
                )
                try:
                    decrypt_from_alice(tampered, st.session_state.bob_key_pair.private_key)
                    st.error("Unexpected success.")
                except CryptoError as exc:
                    st.error(str(exc))
        with col3:
            if st.button("Use wrong private key", use_container_width=True):
                wrong_pair = generate_rsa_key_pair()
                try:
                    decrypt_from_alice(packet, wrong_pair.private_key)
                    st.error("Unexpected success.")
                except CryptoError as exc:
                    st.error(str(exc))

    viva_expander(
        [
            ("Why is hybrid encryption common?", "It combines fast symmetric encryption with public-key key transport."),
            ("Does the packet contain the plaintext?", "No. It contains ciphertext and metadata needed for Bob to decrypt."),
            ("What detects message tampering?", "AES-GCM authentication checks the ciphertext, tag, nonce, and key."),
        ]
    )

