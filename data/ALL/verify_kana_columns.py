"""
Quick sanity check — prints the first 6 rows (header + 5 data rows)
of each patched categorized.csv, showing only the first 6 columns.
"""

import csv
from pathlib import Path

ALL_DIR = Path(__file__).parent

for csv_path in sorted(ALL_DIR.glob("*/categorized.csv")):
    print(f"\n=== {csv_path.relative_to(ALL_DIR)} ===")
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            print(row[:6])
            if i >= 5:
                break
