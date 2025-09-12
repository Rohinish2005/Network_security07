import hashlib
from ecdsa import SigningKey, NIST256p, VerifyingKey

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.digest()


signing_key = SigningKey.generate(curve=NIST256p)
verify_key: VerifyingKey = signing_key.get_verifying_key()

print("ECC key pair created (NIST P-256 curve)")

file1 = input("Enter path for first file: ").strip()
file2 = input("Enter path for second file: ").strip()

hash1 = sha256_file(file1)
hash2 = sha256_file(file2)

print(f"SHA-256 of {file1} -> {hash1.hex()}")
print(f"SHA-256 of {file2} -> {hash2.hex()}")


