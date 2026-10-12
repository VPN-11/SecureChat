"""Hybrid RSA-OAEP + AES-GCM workflow helpers."""

from __future__ import annotations

from dataclasses import dataclass

from cryptography.hazmat.primitives.asymmetric import rsa

from crypto.aes import AESGCMResult, CryptoError, decrypt_message, encrypt_message, generate_aes_key
from crypto.rsa import decrypt_aes_key, encrypt_aes_key


@dataclass(frozen=True)
class HybridPacket:
    """Public network packet for the SecureChat hybrid workflow."""

    algorithm: str
    key_encryption: str
    encrypted_aes_key: bytes
    nonce: bytes
    ciphertext: bytes
    tag: bytes

    def as_display_dict(self) -> dict[str, str]:
        """Return copy-friendly packet fields without secrets."""

        return {
            "algorithm": self.algorithm,
            "key_encryption": self.key_encryption,
            "encrypted_aes_key_hex": self.encrypted_aes_key.hex(),
            "nonce_hex": self.nonce.hex(),
            "ciphertext_hex": self.ciphertext.hex(),
            "authentication_tag_hex": self.tag.hex(),
        }


@dataclass(frozen=True)
class HybridEncryptionResult:
    """Result of hybrid encryption, including the secret key for local tests only."""

    packet: HybridPacket
    aes_key: bytes


def encrypt_for_bob(message: bytes | str, bob_public_key: rsa.RSAPublicKey) -> HybridEncryptionResult:
    """Encrypt a message using AES-GCM and wrap the AES key with Bob's RSA public key."""

    aes_key = generate_aes_key()
    aes_result: AESGCMResult = encrypt_message(message, aes_key)
    encrypted_aes_key = encrypt_aes_key(aes_key, bob_public_key)
    packet = HybridPacket(
        algorithm="AES-256-GCM",
        key_encryption="RSA-OAEP-SHA256",
        encrypted_aes_key=encrypted_aes_key,
        nonce=aes_result.nonce,
        ciphertext=aes_result.ciphertext,
        tag=aes_result.tag,
    )
    return HybridEncryptionResult(packet=packet, aes_key=aes_key)


def decrypt_from_alice(packet: HybridPacket, bob_private_key: rsa.RSAPrivateKey) -> bytes:
    """Recover and authenticate a hybrid encrypted message."""

    if not isinstance(packet, HybridPacket):
        raise CryptoError("Hybrid decrypt expects a HybridPacket.")
    aes_key = decrypt_aes_key(packet.encrypted_aes_key, bob_private_key)
    return decrypt_message(packet.ciphertext, packet.tag, packet.nonce, aes_key)

