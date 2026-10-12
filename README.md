# SecureChat

Secure Message Communication and Cryptography Demonstration System.

## Abstract

SecureChat is a local Streamlit application that demonstrates how modern cryptographic algorithms protect messages. It simulates Alice sending protected data to Bob and shows confidentiality with AES-256-GCM, key transport with RSA-OAEP, integrity comparison with SHA-256, and authenticity with RSA-PSS digital signatures.

This is an educational CNS mini project, not a production secure messenger.

## Problem Statement

Students often learn encryption, hashing, and digital signatures separately. SecureChat brings them into one interactive workflow so users can see what data is secret, what can travel over a network, and how tampering or wrong keys are detected.

## Objectives

- Demonstrate AES-256-GCM encryption, decryption, and tamper detection.
- Demonstrate RSA-OAEP encryption and decryption of an AES session key.
- Demonstrate SHA-256 digest comparison and explain why hashing is not encryption.
- Demonstrate RSA-PSS signing and verification.
- Combine AES and RSA into a hybrid encryption workflow.
- Provide automated tests and beginner-friendly documentation.

## Scope

The application runs locally and uses only session-scoped keys. It does not provide real user accounts, network messaging, certificates, persistent private-key storage, or production-grade secure communication.

## Technologies Used

- Python 3.11 or compatible version
- Streamlit
- cryptography
- pytest

## System Requirements

- Windows, Linux, or macOS
- Python 3.11 or newer recommended
- Internet access for first-time dependency installation
- VS Code or any Python editor

## Installation on Windows and VS Code

Open the project folder in VS Code, then use a terminal:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
pip install -r requirements.txt
```

If `py` is not available, install Python from python.org and select "Add python.exe to PATH" during installation.

## Run the Application

```powershell
streamlit run app.py
```

Open the local URL shown by Streamlit, usually `http://localhost:8501`.

## Run Tests

```powershell
pytest
```

## Project Structure

```text
SecureChat/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── crypto/
│   ├── aes.py
│   ├── rsa.py
│   ├── hashing.py
│   ├── hybrid.py
│   └── signatures.py
├── ui/
│   ├── dashboard.py
│   ├── aes_demo.py
│   ├── rsa_demo.py
│   ├── hybrid_demo.py
│   ├── hashing_demo.py
│   └── signature_demo.py
├── tests/
│   ├── test_aes.py
│   ├── test_rsa.py
│   ├── test_hybrid.py
│   ├── test_hashing.py
│   └── test_signatures.py
└── docs/
    ├── project_report.md
    ├── viva_questions.md
    └── demo_script.md
```

## Algorithm Explanations

AES-256-GCM is a symmetric authenticated encryption algorithm. It uses one secret key and a unique nonce for each encryption. If ciphertext, tag, nonce, or key changes, authentication fails.

RSA-OAEP is an asymmetric encryption method. Alice uses Bob's public key to encrypt a small AES key. Bob uses his private key to recover it.

SHA-256 is a one-way hash function. It creates a 256-bit digest and helps compare message integrity, but it does not hide data and does not prove sender identity by itself.

RSA-PSS is a digital signature scheme. Alice signs with her private key, and Bob verifies with Alice's public key. This supports integrity and authenticity when Bob trusts Alice's public key.

## Application Workflow

1. Open the dashboard and explain confidentiality, integrity, and authenticity.
2. Use AES-256-GCM page to encrypt, decrypt, tamper with ciphertext, and try a wrong key.
3. Use RSA-OAEP page to generate/encrypt an AES key for Bob and show wrong-private-key failure.
4. Use Hybrid Workflow page to create a simulated packet and decrypt it as Bob.
5. Use SHA-256 page to compare message digests.
6. Use RSA-PSS page to sign, verify, modify, and verify with an unrelated public key.

## Test Results

The test suite is included under `tests/`. In this environment, Python was not available on PATH, so tests could not be executed here. After installing Python and dependencies, run:

```powershell
pytest
```

Expected result: all tests should pass.

## Known Limitations

- Educational local simulation only.
- No real network transport.
- No certificate authority or public-key infrastructure.
- No persistent secure private-key storage.
- Streamlit session keys reset when the session is cleared or the app restarts.

