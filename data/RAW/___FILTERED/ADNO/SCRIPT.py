"""
Generates DATA.csv from the ADNO Japanese Wikipedia word frequency dataset.
Source file: jawiki-frequency-20221020.tsv (pre-sorted by count descending)
Output: top 25,000 words with WORD, FREQUENCY_RANKING columns.
"""

import csv
import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), "../../ADNO/jawiki-frequency-20221020.tsv")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "DATA.csv")
TOP_N = 25000


def main():
    rows = []
    with open(INPUT_FILE, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            if row["word"].startswith("["):  # skip metadata rows like [TOTAL]
                continue
            rows.append((row["word"], int(row["count"])))

    # Sort by count descending (already sorted, but ensure correctness)
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
