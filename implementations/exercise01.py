import csv

MEMPOOL_FILE = "data/mempool.csv"
OUTPUT_FILE = "solutions/exercise01.txt"

REQUIRED_TXID = "4c50e3dad7f98bceb6441f96b23748dea84fbdb7cedd603441e6ea4a574d04a6"
MAX_WEIGHT = 4_000_000
MIN_FEE = 50_000


def load_mempool():
    mempool = {}

    with open(MEMPOOL_FILE, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)

        for row in reader:
            txid = row[0].strip()
            fee = int(row[1])
            weight = int(row[2])

            parents = []
            if len(row) > 3 and row[3].strip():
                parents = [p.strip() for p in row[3].split(";") if p.strip()]

            mempool[txid] = {
                "fee": fee,
                "weight": weight,
                "parents": parents,
            }

    return mempool


def add_with_parents(txid, mempool, selected, selected_set):
    if txid in selected_set:
        return

    for parent in mempool[txid]["parents"]:
        add_with_parents(parent, mempool, selected, selected_set)

    if txid not in selected_set:
        selected.append(txid)
        selected_set.add(txid)


def main():
    mempool = load_mempool()

    selected = []
    selected_set = set()

    add_with_parents(
        REQUIRED_TXID,
        mempool,
        selected,
        selected_set,
    )

    current_fee = sum(mempool[tx]["fee"] for tx in selected)
    current_weight = sum(mempool[tx]["weight"] for tx in selected)

    candidates = sorted(
        mempool.items(),
        key=lambda item: item[1]["fee"],
        reverse=True,
    )

    for txid, data in candidates:

        if txid in selected_set:
            continue

        needed = []

        def collect(tx):
            if tx in selected_set:
                return

            for p in mempool[tx]["parents"]:
                collect(p)

            if tx not in needed:
                needed.append(tx)

        collect(txid)

        extra_weight = sum(mempool[t]["weight"] for t in needed)

        if current_weight + extra_weight > MAX_WEIGHT:
            continue

        for tx in needed:
            if tx not in selected_set:
                selected.append(tx)
                selected_set.add(tx)

                current_fee += mempool[tx]["fee"]
                current_weight += mempool[tx]["weight"]

        if current_fee >= MIN_FEE:
            break

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for txid in selected:
            f.write(txid + "\n")

    print("Fee:", current_fee)
    print("Weight:", current_weight)
    print("Transactions:", len(selected))


if __name__ == "__main__":
    main()