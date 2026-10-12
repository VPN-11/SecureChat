# Five-Minute SecureChat Demo Script

## 0:00-0:40 Dashboard

1. Run `streamlit run app.py`.
2. Open the dashboard.
3. Say: "SecureChat is an educational simulation of Alice sending protected messages to Bob."
4. Point out the three security goals: confidentiality, integrity, and authenticity.
5. Explain that the app is local and not a production messenger.

## 0:40-1:30 AES-256-GCM

1. Open "AES-256-GCM" from the sidebar.
2. Enter: `Meet me in the lab at 10 AM.`
3. Click "Encrypt message".
4. Point out the nonce, ciphertext, and authentication tag.
5. Click "Decrypt with correct key" and show that the original message returns.
6. Click "Tamper ciphertext" and explain that AES-GCM rejects modified data.
7. Click "Try wrong key" and explain that wrong keys cannot decrypt authenticated ciphertext.

## 1:30-2:15 RSA-OAEP

1. Open "RSA-OAEP".
2. Show Bob's public-key summary and public-key export.
3. Click "Generate AES key and encrypt for Bob".
4. Click "Decrypt with Bob's private key".
5. Click "Try Alice's private key instead".
6. Say: "RSA is used only for the small AES key, not for the full message."

## 2:15-3:15 Hybrid Workflow

1. Open "Hybrid Workflow".
2. Enter: `Hi Bob, the SecureChat demo is ready.`
3. Click "Create secure packet for Bob".
4. Show that the packet has encrypted AES key, nonce, ciphertext, tag, and algorithm names.
5. Say: "The packet does not contain the plaintext, raw AES key, or Bob's private key."
6. Click "Bob decrypts packet".
7. Click "Tamper packet ciphertext" to show authentication failure.

## 3:15-4:00 SHA-256

1. Open "SHA-256 Hashing".
2. Compare `The exam starts at 10 AM.` with `The exam starts at 10 PM.`
3. Point out that the digests are completely different.
4. Say: "Hashing is one-way and not encryption. A plain hash does not prove who sent the message."

## 4:00-5:00 RSA-PSS Signatures

1. Open "RSA-PSS Signatures".
2. Enter: `I, Alice, approve this SecureChat demo.`
3. Click "Sign with Alice's private key".
4. Click "Verify correct message".
5. Click "Modify message and verify".
6. Click "Verify with unrelated public key".
7. Say: "A signature proves the message matches Alice's trusted public key, but real-world identity requires trusted key binding."

