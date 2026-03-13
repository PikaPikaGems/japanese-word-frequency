#!/usr/bin/env python3
"""
Generate CONSOLIDATED_UNIQUE.csv from CONSOLIDATED.csv.

Deduplicates words that appear multiple times (due to different POS entries
in the source TSV), keeping only the row with the best (lowest) combined_rank
for each unique word spelling.

Usage:
    python3 scripts/make_consolidated_unique.py

Input:  CONSOLIDATED.csv  (at CEJC root)
Output: CONSOLIDATED_UNIQUE.csv  (at CEJC root)
"""

import csv
from pathlib import Path

ROOT = Path(__file__).parents[1]
IN_PATH  = ROOT / "CONSOLIDATED.csv"
OUT_PATH = ROOT / "CONSOLIDATED_UNIQUE.csv"


def run():
    best: dict[str, dict] = {}

    with IN_PATH.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            word = row["word"]
            rank = int(row["combined_rank"])
            if word not in best or rank < int(best[word]["combined_rank"]):
                best[word] = row

    # Sort by combined_rank ascending
    rows = sorted(best.values(), key=lambda r: int(r["combined_rank"]))

    with OUT_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Input rows : {sum(1 for _ in open(IN_PATH, encoding='utf-8')) - 1:,}")
    print(f"Output rows: {len(rows):,}  (duplicates removed: {29534 - len(rows):,})")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    run()
