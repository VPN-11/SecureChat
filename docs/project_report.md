# SecureChat Project Report

## Title Page

- Project title: SecureChat - Secure Message Communication and Cryptography Demonstration System
- Student name: ____________________
- USN: ____________________
- Department: ____________________
- College: ____________________
- Subject: Cryptography and Network Security
- Academic year: ____________________

## Abstract

SecureChat is a local educational web application that demonstrates major cryptographic concepts through an Alice-to-Bob message communication simulation. It uses AES-256-GCM for symmetric authenticated encryption, RSA-OAEP for protecting an AES session key, SHA-256 for digest comparison, and RSA-PSS for digital signatures. The project helps students understand confidentiality, integrity, authenticity, tamper detection, and the purpose of hybrid encryption.

## Introduction

Cryptography is essential for secure communication. Encryption protects message secrecy, hashing supports integrity checks, and digital signatures support authenticity. SecureChat presents these ideas in an interactive Streamlit interface backed by real cryptographic operations from the Python `cryptography` library.

## Problem Statement

Cryptographic algorithms are often difficult to understand when studied only through theory. The problem is to create a simple, reliable demonstration system that shows how secure message protection works and how attacks such as tampering or wrong-key use are detected.

## Objectives

- Implement AES-256-GCM encryption and decryption.
- Implement RSA-OAEP encryption and decryption of AES keys.
- Implement SHA-256 hashing and digest comparison.
- Implement RSA-PSS signing and verification.
- Build a complete hybrid encryption workflow.
- Provide automated tests and documentation for academic submission.

## Literature and Background Overview

AES is a standard symmetric encryption algorithm used widely for efficient data encryption. GCM mode adds authentication so modified ciphertext is rejected. RSA is a public-key algorithm used here for encrypting small secrets and for signatures. OAEP is used for RSA encryption padding, while PSS is used for RSA signatures. SHA-256 is a one-way hash function that produces a fixed 256-bit digest.

References:

- Python cryptography documentation: https://cryptography.io/
- NIST FIPS 197 Advanced Encryption Standard
- NIST FIPS 180-4 Secure Hash Standard
- RFC 8017 PKCS #1 RSA Cryptography Specifications

## Software and Hardware Requirements

Software:

- Python 3.11 or compatible version
- Streamlit
- cryptography
- pytest
- VS Code or any Python editor

Hardware:

- Standard laptop or desktop computer
- 4 GB RAM or higher recommended

## System Architecture

The project is divided into three layers:

- Crypto layer: reusable functions for AES, RSA, hashing, signatures, and hybrid encryption.
- UI layer: Streamlit pages that present interactive demonstrations.
- Test layer: pytest tests that validate important success and failure cases.

## Module Descriptions

- `crypto/aes.py`: AES-256-GCM key generation, encryption, decryption, and tamper helper.
- `crypto/rsa.py`: RSA key generation, public-key export, public-key summary, RSA-OAEP key encryption.
- `crypto/hashing.py`: SHA-256 digest helpers.
- `crypto/signatures.py`: RSA-PSS signing and verification.
- `crypto/hybrid.py`: complete AES-GCM plus RSA-OAEP packet workflow.
- `ui/*.py`: Streamlit pages for each demonstration.
- `tests/*.py`: automated tests for cryptographic behavior.

## Algorithm Explanations

AES-256-GCM uses a 256-bit symmetric key and a fresh 12-byte nonce to encrypt data. It produces ciphertext and an authentication tag. If data is modified, decryption fails.

RSA-OAEP uses Bob's public key to encrypt a small AES session key. Only Bob's private key can decrypt it.

SHA-256 maps input data to a 256-bit digest. It is useful for comparison but cannot be reversed into the original message.

RSA-PSS signs data with Alice's private key. Bob verifies the signature using Alice's public key.

## Implementation Methodology

1. Create modular cryptographic helper functions.
2. Raise clear errors for expected authentication and key failures.
3. Store demonstration keys in Streamlit session state.
4. Build separate pages for each concept.
5. Write pytest tests for normal and failure behavior.
6. Document setup, demonstration flow, and viva answers.

## Test Cases and Actual Results

Included automated tests:

- AES decrypts original plaintext.
- AES repeated encryption uses fresh nonce and different ciphertext.
- AES rejects tampered ciphertext.
- AES rejects wrong key.
- RSA-OAEP encrypts and decrypts an AES key.
- Wrong RSA private key fails.
- SHA-256 matches the known digest for `abc`.
- Changed messages produce different hashes.
- RSA-PSS verifies correct signatures.
- Modified messages fail signature verification.
- Unrelated public keys fail signature verification.
- Hybrid workflow recovers original message.

Actual local execution note: Python was not available on PATH in the current shell when this project was generated, so pytest could not be executed here. Run `pytest` after installing Python and dependencies.

## Screenshots

Capture genuine screenshots after running the app:

1. Dashboard page.
2. AES page after successful encryption and decryption.
3. AES tamper failure.
4. RSA-OAEP encrypted AES key and successful decrypt.
5. Hybrid packet and Bob decrypt result.
6. SHA-256 digest comparison.
7. RSA-PSS successful and failed verification.

Do not use fabricated screenshots.

## Advantages

- Uses real cryptographic library APIs.
- Demonstrates success and failure cases.
- Clear separation between encryption, hashing, and signatures.
- Easy to run locally.
- Includes automated tests and viva preparation.

## Limitations

- Not production-ready.
- No real messaging network.
- No user authentication system.
- No certificate authority or PKI.
- Private keys are session-scoped and not persisted securely.

## Future Enhancements

- Add authenticated user accounts for a controlled lab setup.
- Add certificate/fingerprint verification demonstration.
- Add optional file encryption demo.
- Add sequence diagrams and downloadable lab worksheet.
- Add Streamlit screenshot guide after running the app.

## Conclusion

SecureChat successfully demonstrates the major cryptographic ideas required for a CNS mini project. It shows how AES-GCM, RSA-OAEP, SHA-256, and RSA-PSS work individually and together in a hybrid communication workflow.

