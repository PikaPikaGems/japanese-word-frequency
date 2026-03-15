"""
Check that no two frequency rank columns in any consolidated.csv are exact duplicates.

Non-rank columns (word, hiragana, katakana) are skipped.
Reports every duplicate pair found, per file.
"""

import csv
import sys
from pathlib import Path

NON_RANK_COLS = {"word", "hiragana", "katakana"}


def find_duplicates(path: Path) -> list[tuple[str, str]]:
    """Return list of (col_a, col_b) pairs that have identical values in this file."""
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rank_cols = [c for c in reader.fieldnames if c not in NON_RANK_COLS]

        # Accumulate each column's values as a tuple
        columns: dict[str, list[str]] = {c: [] for c in rank_cols}
        for row in reader:
            for c in rank_cols:
                columns[c].append(row[c])

    # Convert to tuples for hashing
    col_tuples = {c: tuple(v) for c, v in columns.items()}

    # Group columns by their value tuple
    seen: dict[tuple, list[str]] = {}
    for col, values in col_tuples.items():
        seen.setdefault(values, []).append(col)

    duplicates = []
    for cols in seen.values():
        if len(cols) > 1:
            # Report all pairs within the group
            for i in range(len(cols)):
                for j in range(i + 1, len(cols)):
                    duplicates.append((cols[i], cols[j]))

    return duplicates


def main():
    root = Path(__file__).parent
    csv_files = sorted(root.rglob("consolidated.csv"))

    if not csv_files:
        print("No consolidated.csv files found.")
        sys.exit(1)

    found_any = False

    for path in csv_files:
        rel = path.relative_to(root)
        duplicates = find_duplicates(path)
        if duplicates:
            found_any = True
            print(f"DUPLICATES in {rel}:")
            for col_a, col_b in duplicates:
                print(f"  {col_a}  ==  {col_b}")
        else:
            print(f"OK  {rel}")

    if found_any:
        print("\nDuplicate columns detected.")
        sys.exit(1)
    else:
        print("\nAll columns are unique across all files.")


if __name__ == "__main__":
    main()
