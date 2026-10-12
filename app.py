"""SecureChat Streamlit application."""

from __future__ import annotations

import streamlit as st

from ui import aes_demo, dashboard, hashing_demo, hybrid_demo, rsa_demo, signature_demo
from ui.common import ensure_keys, reset_keys_button


st.set_page_config(
    page_title="SecureChat",
    page_icon=":lock:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root {
        --secure-bg: #07111f;
        --secure-panel: #0f1c2e;
        --secure-panel-2: #132840;
        --secure-cyan: #48cae4;
        --secure-blue: #4ea8de;
        --secure-text: #eaf4ff;
        --secure-muted: #a9bfd6;
        --secure-border: rgba(120, 190, 220, 0.25);
    }
    .stApp {
        background: radial-gradient(circle at top left, rgba(72,202,228,0.13), transparent 28rem),
                    linear-gradient(180deg, #07111f 0%, #091526 100%);
        color: var(--secure-text);
    }
    h1, h2, h3 {
        color: var(--secure-text);
        letter-spacing: 0;
    }
    .secure-card {
        background: linear-gradient(180deg, rgba(19,40,64,0.92), rgba(15,28,46,0.92));
        border: 1px solid var(--secure-border);
        border-radius: 8px;
        padding: 1rem;
        min-height: 9rem;
    }
    .secure-card h3 {
        margin-top: 0;
        color: var(--secure-cyan);
        font-size: 1.1rem;
    }
    .workflow-step {
        background: rgba(15, 28, 46, 0.85);
        border-left: 4px solid var(--secure-cyan);
        padding: 0.85rem 1rem;
        border-radius: 6px;
        margin-bottom: 0.6rem;
    }
    code, pre {
        white-space: pre-wrap !important;
        overflow-wrap: anywhere !important;
    }
    [data-testid="stSidebar"] {
        background: #081321;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


PAGES = {
    "Dashboard": dashboard.render,
    "AES-256-GCM": aes_demo.render,
    "RSA-OAEP": rsa_demo.render,
    "Hybrid Workflow": hybrid_demo.render,
    "SHA-256 Hashing": hashing_demo.render,
    "RSA-PSS Signatures": signature_demo.render,
}


def main() -> None:
    ensure_keys()
    st.sidebar.title("SecureChat")
    page_name = st.sidebar.radio("Navigate", list(PAGES.keys()))
    st.sidebar.caption("Educational CNS demo. Keys are held only in Streamlit session memory.")
    reset_keys_button()
    PAGES[page_name]()


if __name__ == "__main__":
    main()

