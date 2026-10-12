"""Dashboard page."""

from __future__ import annotations

import streamlit as st


def render() -> None:
    st.title("SecureChat")
    st.caption("Secure Message Communication and Cryptography Demonstration System")
    st.markdown(
        "SecureChat is a local educational simulation of Alice sending protected messages to Bob. "
        "It demonstrates confidentiality, integrity, authenticity, and the practical reason modern systems use hybrid encryption."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            '<div class="secure-card"><h3>Confidentiality</h3><p>AES-GCM hides the message content. '
            'RSA-OAEP protects the temporary AES key while it travels to Bob.</p></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div class="secure-card"><h3>Integrity</h3><p>AES-GCM authentication and SHA-256 comparisons '
            'help show whether data changed after it was created.</p></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            '<div class="secure-card"><h3>Authenticity</h3><p>RSA-PSS signatures let Bob verify that a message '
            'was signed by the holder of Alice\'s private key.</p></div>',
            unsafe_allow_html=True,
        )

    st.subheader("Algorithms Used")
    st.table(
        [
            {"Algorithm": "AES-256-GCM", "Purpose": "Fast symmetric encryption with built-in authentication"},
            {"Algorithm": "RSA-OAEP", "Purpose": "Encrypt a small AES session key using Bob's public key"},
            {"Algorithm": "SHA-256", "Purpose": "Create a fixed-size message digest for comparison"},
            {"Algorithm": "RSA-PSS", "Purpose": "Create and verify digital signatures"},
        ]
    )

    st.subheader("Symmetric vs Asymmetric Encryption")
    left, right = st.columns(2)
    with left:
        st.markdown(
            "#### Symmetric\n"
            "One shared secret key encrypts and decrypts data. It is fast and suitable for message content, "
            "but Alice and Bob must protect the same key."
        )
    with right:
        st.markdown(
            "#### Asymmetric\n"
            "A public key can be shared, while the private key stays secret. It is useful for key exchange "
            "and signatures, but slower and limited to small payloads."
        )

    st.subheader("Sender-to-Receiver Workflow")
    steps = [
        "Alice writes a message.",
        "The app generates a fresh AES-256 key and nonce.",
        "AES-GCM encrypts and authenticates the message.",
        "RSA-OAEP encrypts the AES key with Bob's public key.",
        "The simulated packet contains only public/safe transport fields.",
        "Bob uses his private key to recover the AES key.",
        "Bob decrypts the message; tampering causes authentication failure.",
    ]
    for index, step in enumerate(steps, start=1):
        st.markdown(f'<div class="workflow-step"><strong>{index}.</strong> {step}</div>', unsafe_allow_html=True)

    st.info("Use the sidebar to open each demonstration page. No messages are sent to external servers.")

