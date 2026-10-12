"""SHA-256 hashing helpers."""

from __future__ import annotations

from cryptography.hazmat.primitives import hashes


def sha256_digest(data: bytes | str) -> bytes:
    """Return the SHA-256 digest of text or bytes."""

    if isinstance(data, str):
        data = data.encode("utf-8")
    if not isinstance(data, bytes):
        raise TypeError("Data must be text or bytes.")
    digest = hashes.Hash(hashes.SHA256())
    digest.update(data)
    return digest.finalize()


def sha256_hex(data: bytes | str) -> str:
    """Return the SHA-256 digest as lowercase hexadecimal text."""

    return sha256_digest(data).hex()

