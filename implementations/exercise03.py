import hashlib
import os

TARGET = int(
    "00000000ffff0000000000000000000000000000000000000000000000000000",
    16,
)

VERSION = "00000002"

PREVIOUS_BLOCK = "00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4a2ee"

MERKLE_ROOT = "d91dd147529e496a82e06cb2f051fb5aaa6ea993e87b269db3bfef8c96a0d093"

# timestamp dentro do range (fixo válido do exercício)
TIMESTAMP = "495fab2a"


def sha256(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()


nonce = 0

print("Mining...")

while True:

    nonce_hex = f"{nonce:016x}"

    header_hex = (
        VERSION +
        PREVIOUS_BLOCK +
        MERKLE_ROOT +
        TIMESTAMP +
        nonce_hex
    )

    header = bytes.fromhex(header_hex)

    h = sha256(header)
    h_int = int.from_bytes(h, "big")

    if nonce % 200_000 == 0:
        print("nonce =", nonce)

    if h_int <= TARGET:
        print("\nFOUND!")
        print("nonce:", nonce)
        print("hash :", h.hex())

        os.makedirs("solutions", exist_ok=True)

        with open("solutions/exercise03.txt", "w") as f:
            f.write(header_hex)

        break

    nonce += 1