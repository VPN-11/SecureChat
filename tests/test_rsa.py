import pytest

from crypto.aes import CryptoError, generate_aes_key
from crypto.rsa import decrypt_aes_key, encrypt_aes_key, export_public_key_pem, generate_rsa_key_pair, public_key_summary


def test_rsa_oaep_encrypts_and_decrypts_aes_key():
    bob = generate_rsa_key_pair()
    aes_key = generate_aes_key()

    encrypted_key = encrypt_aes_key(aes_key, bob.public_key)
    recovered_key = decrypt_aes_key(encrypted_key, bob.private_key)

    assert recovered_key == aes_key
    assert encrypted_key != aes_key


def test_incorrect_private_key_cannot_decrypt_aes_key():
    bob = generate_rsa_key_pair()
    mallory = generate_rsa_key_pair()
    encrypted_key = encrypt_aes_key(generate_aes_key(), bob.public_key)

    with pytest.raises(CryptoError, match="wrong private key"):
        decrypt_aes_key(encrypted_key, mallory.private_key)


def test_public_key_export_and_summary_do_not_include_private_key():
    bob = generate_rsa_key_pair()
    pem = export_public_key_pem(bob.public_key)
    summary = public_key_summary(bob.public_key)

    assert "BEGIN PUBLIC KEY" in pem
    assert "PRIVATE KEY" not in pem
    assert summary["key_size_bits"] >= 2048
    assert summary["public_exponent"] == 65537


def test_rsa_rejects_invalid_aes_key_length():
    bob = generate_rsa_key_pair()

    with pytest.raises(CryptoError, match="32-byte AES key"):
        encrypt_aes_key(b"not-aes-256", bob.public_key)

