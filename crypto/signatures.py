"""RSA-PSS digital signature helpers."""

from __future__ import annotations

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from crypto.aes import CryptoError


def sign_message(message: bytes | str, private_key: rsa.RSAPrivateKey) -> bytes:
    """Sign a message with RSA-PSS and SHA-256."""

    if isinstance(message, str):
        message = message.encode("utf-8")
    if not isinstance(message, bytes):
        raise CryptoError("Message must be text or bytes.")
    return private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )


def verify_signature(message: bytes | str, signature: bytes, public_key: rsa.RSAPublicKey) -> bool:
    """Return True only when an RSA-PSS signature verifies."""

    if isinstance(message, str):
        message = message.encode("utf-8")
    if not isinstance(message, bytes) or not isinstance(signature, bytes):
        raise CryptoError("Message and signature must be bytes or text as appropriate.")
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
    except InvalidSignature:
        return False
    return True

