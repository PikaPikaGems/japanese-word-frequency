"""
Generates DATA.csv from Dave Doebrick's Morphman Japanese Novels frequency list.
Source: 'Morphman JapFreqList_5109_Novels.txt' — tab-separated: count, word.
Output: top 25,000 words sorted by occurrence count descending.
"""

import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), "../../DAVE_DOEBRICK_PART2/MORPHMAN/Morphman JapFreqList_5109_Novels.txt")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "DATA.csv")
TOP_N = 25000


def main():
    rows = []
    with open(INPUT_FILE, encoding="utf-8-sig") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            try:
                count = int(parts[0])
                word = parts[1]
                rows.append((word, count))
            except (ValueError, IndexError):
                continue

    # Sort by count descending (highest count = rank 1)
    rows.sort(key=lambda x: x[1], reverse=True)
    top = rows[:TOP_N]

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        f.write("WORD,FREQUENCY_RANKING\n")
        for rank, (word, _count) in enumerate(top, start=1):
            f.write(f"{word},{rank}\n")

    print(f"Written {len(top)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
