"""
Generates DATA.csv from the HermitDave 2018 OpenSubtitles Japanese word frequency dataset.
Combines ja_ignored.txt (high-freq words) and ja_full.txt, sorts by count descending.
Output: top 25,000 words with WORD, FREQUENCY_RANKING columns.
"""

import csv
import os

BASE_DIR = os.path.join(os.path.dirname(__file__), "../../HERMITDAVE/2018JA")
INPUT_FILES = [
    os.path.join(BASE_DIR, "ja_ignored.txt"),
    os.path.join(BASE_DIR, "ja_full.txt"),
]
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "DATA.csv")
TOP_N = 25000


def parse_file(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.rsplit(" ", 1)
            if len(parts) != 2:
                continue
            word, count_str = parts
            try:
                rows.append((word, int(count_str)))
            except ValueError:
                continue
    return rows


def main():
    rows = []
    for path in INPUT_FILES:
        rows.extend(parse_file(path))

    # Sort by count descending
    rows.sort(key=lambda x: x[1], reverse=True)

    top = rows[:TOP_N]

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["WORD", "FREQUENCY_RANKING"])
        for rank, (word, _count) in enumerate(top, start=1):
            writer.writerow([word, rank])

    print(f"Written {len(top)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
