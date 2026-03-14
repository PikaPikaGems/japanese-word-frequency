"""
Report how many words are missing hiragana/katakana readings
across all patched categorized.csv and consolidated.csv files.
"""

import csv
from pathlib import Path

ALL_DIR = Path(__file__).parent

for csv_path in sorted(ALL_DIR.glob("*/categorized.csv")) + sorted(ALL_DIR.glob("*/consolidated.csv")):
    total = 0
    missing = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "hiragana" not in (reader.fieldnames or []):
            print(f"{csv_path.relative_to(ALL_DIR)}: no hiragana column")
            continue
        for row in reader:
            total += 1
            if not row["hiragana"]:
                missing.append(row["word"])

    pct = len(missing) / total * 100 if total else 0
    print(f"{csv_path.relative_to(ALL_DIR)}: {len(missing)}/{total} missing ({pct:.1f}%)")
    if missing:
        for w in missing[:10]:
            print(f"  {w!r}")
        if len(missing) > 10:
            print(f"  ... and {len(missing) - 10} more")
