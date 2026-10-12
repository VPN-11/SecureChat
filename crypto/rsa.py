"""RSA key generation, export, and RSA-OAEP key wrapping helpers."""

from __future__ import annotations

from dataclasses import dataclass

from cryptography.exceptions import InvalidKey
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from crypto.aes import AES_KEY_SIZE, CryptoError


RSA_KEY_SIZE = 2048
PUBLIC_EXPONENT = 65537


@dataclass
class RSAKeyPair:
    """In-memory RSA key pair."""

    private_key: rsa.RSAPrivateKey

    @property
    def public_key(self) -> rsa.RSAPublicKey:
        return self.private_key.public_key()


def generate_rsa_key_pair(key_size: int = RSA_KEY_SIZE) -> RSAKeyPair:
    """Generate an RSA private/public key pair."""

    if key_size < 2048:
        raise CryptoError("RSA keys must be at least 2048 bits for this demo.")
    private_key = rsa.generate_private_key(public_exponent=PUBLIC_EXPONENT, key_size=key_size)
    return RSAKeyPair(private_key=private_key)


def export_public_key_pem(public_key: rsa.RSAPublicKey) -> str:
    """Export an RSA public key as PEM text."""

    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("ascii")


def public_key_fingerprint(public_key: rsa.RSAPublicKey) -> str:
    """Return a short SHA-256 fingerprint for display."""

    der = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    digest = hashes.Hash(hashes.SHA256())
    digest.update(der)
    raw = digest.finalize().hex()
    return ":".join(raw[index : index + 2] for index in range(0, 32, 2))


def public_key_summary(public_key: rsa.RSAPublicKey) -> dict[str, int | str]:
    """Return beginner-friendly public-key metadata."""

    numbers = public_key.public_numbers()
    return {
        "algorithm": "RSA",
        "key_size_bits": public_key.key_size,
        "public_exponent": numbers.e,
        "fingerprint_sha256": public_key_fingerprint(public_key),
    }


def encrypt_aes_key(aes_key: bytes, public_key: rsa.RSAPublicKey) -> bytes:
    """Encrypt a 256-bit AES session key with RSA-OAEP."""

    if not isinstance(aes_key, bytes) or len(aes_key) != AES_KEY_SIZE:
        raise CryptoError("RSA-OAEP demo encrypts exactly one 32-byte AES key.")
    return public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def decrypt_aes_key(encrypted_key: bytes, private_key: rsa.RSAPrivateKey) -> bytes:
    """Decrypt an AES session key with RSA-OAEP."""

    if not isinstance(encrypted_key, bytes) or not encrypted_key:
        raise CryptoError("Encrypted AES key must be non-empty bytes.")
    try:
        aes_key = private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
    except ValueError as exc:
        raise CryptoError("RSA-OAEP decryption failed: wrong private key or corrupted encrypted key.") from exc
    except InvalidKey as exc:
        raise CryptoError("RSA private key is invalid.") from exc

    if len(aes_key) != AES_KEY_SIZE:
        raise CryptoError("Decrypted key is not a valid AES-256 key.")
    return aes_key

