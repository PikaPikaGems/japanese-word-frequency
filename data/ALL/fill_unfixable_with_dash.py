"""
For every word still missing a hiragana reading, fill both hiragana
and katakana with "-" and print a summary of what was filled.
"""

import csv
from pathlib import Path

ALL_DIR = Path(__file__).parent

targets = (
    sorted(ALL_DIR.glob("*/categorized.csv")) +
    sorted(ALL_DIR.glob("*/consolidated.csv"))
)

print(f"{'File':<45}  {'Filled':>6}  {'Total':>7}  {'%':>5}")
print("-" * 68)

for csv_path in targets:
    with open(csv_path, encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))

    if not rows:
        continue

    header = rows[0]
    if "hiragana" not in header:
        continue

    hira_idx = header.index("hiragana")
    kata_idx = header.index("katakana")

    filled = 0
    total  = len(rows) - 1
    for row in rows[1:]:
        if not row[hira_idx]:
            row[hira_idx] = "-"
            row[kata_idx] = "-"
            filled += 1

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(rows)

    pct   = filled / total * 100 if total else 0
    label = str(csv_path.relative_to(ALL_DIR))
    print(f"{label:<45}  {filled:>6}  {total:>7}  {pct:>4.1f}%")
