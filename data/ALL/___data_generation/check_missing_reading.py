"""
Check that every word in every consolidated.csv has both hiragana and katakana readings.

Exits with code 1 if any are missing, 0 if all are present.
"""

import csv
import sys
from pathlib import Path


def check_readings(path: Path) -> list[tuple[str, str, str]]:
    """Return list of (word, missing_field, ...) for rows missing hiragana or katakana."""
    issues = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row.get("word", "")
            hira = row.get("hiragana", "").strip()
            kata = row.get("katakana", "").strip()
            if not hira and not kata:
                issues.append((word, "hiragana+katakana"))
            elif not hira:
                issues.append((word, "hiragana"))
            elif not kata:
                issues.append((word, "katakana"))
    return issues


def main():
    root = Path(__file__).parent.parent.parent
    csv_files = sorted(root.rglob("consolidated.csv"))

    if not csv_files:
        print("No consolidated.csv files found.")
        sys.exit(1)

    found_any = False

    for path in csv_files:
        rel = path.relative_to(root)
        issues = check_readings(path)
        if issues:
            found_any = True
            print(f"MISSING in {rel}:")
            for word, field in issues:
                print(f"  {word!r}  missing {field}")
        else:
            print(f"OK  {rel}")

    if found_any:
        print("\nMissing readings detected.")
        sys.exit(1)
    else:
        print("\nAll words have hiragana and katakana in all files.")


if __name__ == "__main__":
    main()
