"""
Generates DATA.csv from the HermitDave 2016 OpenSubtitles Japanese word frequency dataset.
Source file: ja_50k.txt (space-separated: word count; pre-sorted desc; top 50k)
Output: top 25,000 words with WORD, FREQUENCY_RANKING columns.
"""

import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), "../../HERMITDAVE/2016JA/ja_50k.txt")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "DATA.csv")
TOP_N = 25000


def main():
    rows = []
    with open(INPUT_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.rsplit(" ", 1)
            if len(parts) != 2:
                continue
            word, count_str = parts
            rows.append((word, int(count_str)))

    rows.sort(key=lambda x: x[1], reverse=True)
    top = rows[:TOP_N]

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        f.write("WORD,FREQUENCY_RANKING\n")
        for rank, (word, _count) in enumerate(top, start=1):
            f.write(f"{word},{rank}\n")

    print(f"Written {len(top)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
