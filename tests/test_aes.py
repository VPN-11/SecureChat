import pytest

from crypto.aes import CryptoError, decrypt_message, encrypt_message, generate_aes_key, tamper_bytes


def test_aes_encrypt_decrypt_recovers_plaintext():
    key = generate_aes_key()
    result = encrypt_message("Meet at 10:30 AM", key)

    plaintext = decrypt_message(result.ciphertext, result.tag, result.nonce, key)

    assert plaintext == b"Meet at 10:30 AM"


def test_repeated_encryptions_use_fresh_nonces_and_different_ciphertexts():
    key = generate_aes_key()
    first = encrypt_message("same message", key)
    second = encrypt_message("same message", key)

    assert first.nonce != second.nonce
    assert first.encrypted_payload != second.encrypted_payload


def test_tampered_ciphertext_is_rejected():
    key = generate_aes_key()
    result = encrypt_message("do not modify", key)

    with pytest.raises(CryptoError, match="Authentication failed"):
        decrypt_message(tamper_bytes(result.ciphertext), result.tag, result.nonce, key)


def test_incorrect_aes_key_is_rejected():
    key = generate_aes_key()
    wrong_key = generate_aes_key()
    result = encrypt_message("secret", key)

    with pytest.raises(CryptoError, match="Authentication failed"):
        decrypt_message(result.ciphertext, result.tag, result.nonce, wrong_key)


def test_invalid_inputs_raise_understandable_errors():
    with pytest.raises(CryptoError, match="32-byte key"):
        encrypt_message("hello", b"short")

