"""
Generates DATA.csv from the Japanese Like a Breeze anime frequency list.
Source file: JLAB.tsv (tab-separated, first 2 lines are metadata, line 3 is header)
Columns: Expression, Occurences, Reading, Roumaji
Output: top 25,000 words with WORD, FREQUENCY_RANKING columns.
"""

import csv
import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), "../../JLAB/JLAB.tsv")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "DATA.csv")
TOP_N = 25000


def main():
    rows = []
    with open(INPUT_FILE, encoding="utf-8") as f:
        # Skip first 2 metadata lines before the actual header
        next(f)
        next(f)
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            word = row["Expression"]
            try:
                count = int(row["Occurences"])
            except (ValueError, KeyError):
                continue
            rows.append((word, count))

    # Sort by occurrence count descending (already sorted, but ensure correctness)
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
