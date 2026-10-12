import pytest

from crypto.aes import CryptoError, tamper_bytes
from crypto.hybrid import HybridPacket, decrypt_from_alice, encrypt_for_bob
from crypto.rsa import generate_rsa_key_pair


def test_complete_hybrid_workflow_recovers_original_message():
    bob = generate_rsa_key_pair()
    result = encrypt_for_bob("Hello Bob, this is Alice.", bob.public_key)

    recovered = decrypt_from_alice(result.packet, bob.private_key)

    assert recovered == b"Hello Bob, this is Alice."
    display_packet = result.packet.as_display_dict()
    assert "plaintext" not in display_packet
    assert "aes_key" not in display_packet


def test_hybrid_tampered_ciphertext_fails_authentication():
    bob = generate_rsa_key_pair()
    result = encrypt_for_bob("authenticated message", bob.public_key)
    packet = HybridPacket(
        algorithm=result.packet.algorithm,
        key_encryption=result.packet.key_encryption,
        encrypted_aes_key=result.packet.encrypted_aes_key,
        nonce=result.packet.nonce,
        ciphertext=tamper_bytes(result.packet.ciphertext),
        tag=result.packet.tag,
    )

    with pytest.raises(CryptoError, match="Authentication failed"):
        decrypt_from_alice(packet, bob.private_key)


def test_hybrid_wrong_private_key_fails():
    bob = generate_rsa_key_pair()
    mallory = generate_rsa_key_pair()
    result = encrypt_for_bob("for Bob only", bob.public_key)

    with pytest.raises(CryptoError, match="wrong private key"):
        decrypt_from_alice(result.packet, mallory.private_key)

