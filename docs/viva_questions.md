# SecureChat Viva Questions

1. What is symmetric encryption?
   - It uses the same secret key for encryption and decryption.

2. What is AES?
   - AES is a widely used symmetric block cipher.

3. What does AES-256 mean?
   - It means AES is used with a 256-bit key.

4. What is GCM?
   - Galois/Counter Mode, an authenticated encryption mode for AES.

5. Why is AES-GCM useful?
   - It provides confidentiality and detects unauthorized modification.

6. What is a nonce?
   - A number used once; AES-GCM needs a unique nonce for each encryption under a key.

7. Does the nonce need to be secret?
   - No, but it must not repeat with the same key.

8. What is an authentication tag?
   - A value used during decryption to verify that encrypted data has not been modified.

9. What happens if AES-GCM ciphertext is changed?
   - Authentication fails and plaintext is not returned.

10. What is asymmetric encryption?
    - It uses a public key and private key pair.

11. What is RSA used for in this project?
    - RSA-OAEP encrypts the AES session key, and RSA-PSS creates digital signatures.

12. Why not encrypt the whole message directly with RSA?
    - RSA is slower and limited to small payloads.

13. What is OAEP?
    - A secure padding scheme used with RSA encryption.

14. Which key encrypts the AES key for Bob?
    - Bob's public key.

15. Which key decrypts the AES key?
    - Bob's private key.

16. What is SHA-256?
    - A cryptographic hash function that produces a 256-bit digest.

17. Is hashing encryption?
    - No. Hashing is one-way and cannot be decrypted.

18. What is the length of a SHA-256 hex digest?
    - 64 hexadecimal characters.

19. Does a plain SHA-256 hash prove sender identity?
    - No. Anyone can compute a hash.

20. What is a digital signature?
    - A cryptographic value created with a private key and verified with a public key.

21. What signature scheme is used here?
    - RSA-PSS with SHA-256.

22. What does a valid signature prove?
    - The message matches the private key corresponding to the trusted public key.

23. Does a signature hide the message?
    - No. It authenticates the message but does not encrypt it.

24. What is hybrid encryption?
    - A combination of symmetric encryption for data and asymmetric encryption for the symmetric key.

25. What are confidentiality, integrity, and authenticity?
    - Confidentiality hides data, integrity detects changes, and authenticity verifies the claimed source.

26. What is non-repudiation?
    - The idea that a signer cannot easily deny a valid signature made with their private key.

27. What is a man-in-the-middle attack?
    - An attacker intercepts or changes communication between two parties.

28. How can public-key substitution be prevented?
    - By verifying public keys through certificates, fingerprints, or trusted channels.

29. Why is key management important?
    - Strong algorithms fail if keys are leaked, reused incorrectly, or replaced by an attacker.

30. What are this project's limitations?
    - It is local, educational, has no real networking, no PKI, and no persistent secure key storage.

