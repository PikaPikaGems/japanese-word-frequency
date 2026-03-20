"""
Generates DATA.csv from the hlorenzi Jisho-open Wikipedia word rankings.
Source file: word_rankings_wikipedia.txt (one word per line, rank = line number)
Output: top 25,000 words with WORD, FREQUENCY_RANKING columns.
"""

import csv
import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), "../../HLORENZI/word_rankings_wikipedia.txt")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "DATA.csv")
TOP_N = 25000


def main():
    rows = []
    with open(INPUT_FILE, encoding="utf-8") as f:
        for rank, line in enumerate(f, start=1):
            word = line.rstrip("\n")
            if word:
                rows.append((word, rank))
            if rank >= TOP_N:
                break

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["WORD", "FREQUENCY_RANKING"])
        for word, rank in rows:
            writer.writerow([word, rank])

    print(f"Written {len(rows)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
