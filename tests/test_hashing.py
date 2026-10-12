from crypto.hashing import sha256_hex


def test_sha256_known_digest_for_abc():
    assert sha256_hex("abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_changed_message_changes_digest():
    assert sha256_hex("Pay Bob 100") != sha256_hex("Pay Bob 100.")

