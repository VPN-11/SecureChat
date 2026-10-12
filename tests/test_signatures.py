from crypto.rsa import generate_rsa_key_pair
from crypto.signatures import sign_message, verify_signature


def test_rsa_pss_signature_verifies_for_correct_message_and_key():
    alice = generate_rsa_key_pair()
    message = "Approved by Alice"

    signature = sign_message(message, alice.private_key)

    assert verify_signature(message, signature, alice.public_key)


def test_modified_message_fails_signature_verification():
    alice = generate_rsa_key_pair()
    signature = sign_message("Transfer 100", alice.private_key)

    assert not verify_signature("Transfer 1000", signature, alice.public_key)


def test_unrelated_public_key_fails_signature_verification():
    alice = generate_rsa_key_pair()
    mallory = generate_rsa_key_pair()
    signature = sign_message("Signed by Alice", alice.private_key)

    assert not verify_signature("Signed by Alice", signature, mallory.public_key)

