"""AES-256-GCM helpers.

The functions in this module use authenticated encryption. Decryption either
returns the original plaintext bytes or raises a clear CryptoError.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


AES_KEY_SIZE = 32
AES_GCM_NONCE_SIZE = 12
AES_GCM_TAG_SIZE = 16


class CryptoError(ValueError):
    """Raised when cryptographic input is invalid or authentication fails."""


@dataclass(frozen=True)
class AESGCMResult:
    """Result of an AES-GCM encryption operation."""

    nonce: bytes
    ciphertext: bytes
    tag: bytes

    @property
    def encrypted_payload(self) -> bytes:
        """Return ciphertext concatenated with the authentication tag."""

        return self.ciphertext + self.tag


def generate_aes_key() -> bytes:
    """Generate a cryptographically secure AES-256 key."""

    return AESGCM.generate_key(bit_length=256)


def generate_nonce() -> bytes:
    """Generate a fresh 96-bit nonce for AES-GCM."""

    return os.urandom(AES_GCM_NONCE_SIZE)


def _validate_key(key: bytes) -> None:
    if not isinstance(key, bytes) or len(key) != AES_KEY_SIZE:
        raise CryptoError("AES-256 requires a 32-byte key.")


def _validate_nonce(nonce: bytes) -> None:
    if not isinstance(nonce, bytes) or len(nonce) != AES_GCM_NONCE_SIZE:
        raise CryptoError("AES-GCM requires a 12-byte nonce in this demo.")


def encrypt_message(plaintext: bytes | str, key: bytes, associated_data: bytes | None = None) -> AESGCMResult:
    """Encrypt plaintext with AES-256-GCM using a fresh nonce."""

    _validate_key(key)
    if isinstance(plaintext, str):
        plaintext = plaintext.encode("utf-8")
    if not isinstance(plaintext, bytes):
        raise CryptoError("Plaintext must be text or bytes.")

    nonce = generate_nonce()
    aesgcm = AESGCM(key)
    encrypted = aesgcm.encrypt(nonce, plaintext, associated_data)
    return AESGCMResult(
        nonce=nonce,
        ciphertext=encrypted[:-AES_GCM_TAG_SIZE],
        tag=encrypted[-AES_GCM_TAG_SIZE:],
    )


def decrypt_message(
    ciphertext: bytes,
    tag: bytes,
    nonce: bytes,
    key: bytes,
    associated_data: bytes | None = None,
) -> bytes:
    """Decrypt and authenticate AES-GCM data."""

    _validate_key(key)
    _validate_nonce(nonce)
    if not isinstance(ciphertext, bytes) or not isinstance(tag, bytes):
        raise CryptoError("Ciphertext and tag must be bytes.")
    if len(tag) != AES_GCM_TAG_SIZE:
        raise CryptoError("AES-GCM authentication tag must be 16 bytes.")

    aesgcm = AESGCM(key)
    try:
        return aesgcm.decrypt(nonce, ciphertext + tag, associated_data)
    except InvalidTag as exc:
        raise CryptoError("Authentication failed: the data, key, nonce, or tag is incorrect.") from exc


def tamper_bytes(data: bytes) -> bytes:
    """Return a copy of bytes with one bit flipped for demonstrations."""

    if not data:
        raise CryptoError("Cannot tamper with empty bytes.")
    changed = bytearray(data)
    changed[0] ^= 0x01
    return bytes(changed)

