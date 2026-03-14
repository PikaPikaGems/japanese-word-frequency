"""
Slices each *_anchor/consolidated.csv and *_anchor/categorized.csv down to their
top 12,000 rows, writing the results into top12k/anchors/{ANCHOR}_anchor/.

This makes BCCWJ (16,491 unique words) comparable to all other anchors at the same
word-count ceiling.
"""

import csv
import glob
import os

csv.field_size_limit(10_000_000)

TOP_N = 12000
BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "..", "..")  # data/ALL/
ANCHORS_OUT = os.path.join(BASE, "anchors")


for anchor_dir in sorted(glob.glob(os.path.join(DATA_DIR, "*_anchor"))):
    anchor_name = os.path.basename(anchor_dir).removesuffix("_anchor")

    for filename in ("consolidated.csv", "categorized.csv"):
        src = os.path.join(anchor_dir, filename)
        if not os.path.exists(src):
            print(f"Skipping {anchor_name}/{filename} — not found")
            continue

        with open(src, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            header = reader.fieldnames
            rows = []
            for i, row in enumerate(reader):
                if i >= TOP_N:
                    break
                rows.append(row)

        out_dir = os.path.join(ANCHORS_OUT, f"{anchor_name}_anchor")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, filename)

        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=header)
            writer.writeheader()
            writer.writerows(rows)

    print(f"{anchor_name}: wrote top {min(TOP_N, len(rows))} rows")

print("Done.")
