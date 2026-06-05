import hashlib

INPUT_FILE = "data/ex02_txid_list.txt"
OUTPUT_FILE = "solutions/exercise02.txt"

TARGET_TXID = (
    "49ff8cccf1ca12179e9ae7a4760f550b5a18401b27e1e057604e27c3e10c08fb"
)


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def load_txids():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def build_merkle_tree(txids):
    level = [bytes.fromhex(txid) for txid in txids]

    levels = [level]

    while len(level) > 1:

        if len(level) % 2 == 1:
            level = level + [level[-1]]

        next_level = []

        for i in range(0, len(level), 2):
            parent = sha256(level[i] + level[i + 1])
            next_level.append(parent)

        levels.append(next_level)
        level = next_level

    return levels


def merkle_proof(levels, target_index):
    proof = []
    index = target_index

    for level in levels[:-1]:

        if len(level) % 2 == 1:
            working_level = level + [level[-1]]
        else:
            working_level = level

        if index % 2 == 0:
            sibling_index = index + 1
        else:
            sibling_index = index - 1

        proof.append(working_level[sibling_index])

        index //= 2

    return proof


def main():
    txids = load_txids()

    try:
        target_index = txids.index(TARGET_TXID)
    except ValueError:
        raise Exception("Target transaction not found.")

    levels = build_merkle_tree(txids)

    merkle_root = levels[-1][0].hex()

    proof = merkle_proof(levels, target_index)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(merkle_root + "\n")

        for sibling in proof:
            f.write(sibling.hex() + "\n")

    print("Merkle Root:", merkle_root)
    print("Proof levels:", len(proof))
    print("Output written to", OUTPUT_FILE)


if __name__ == "__main__":
    main()