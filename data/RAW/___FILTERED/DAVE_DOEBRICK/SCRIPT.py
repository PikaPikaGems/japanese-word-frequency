"""
Generates DATA.csv from Dave Doebrick's Netflix Japanese subtitles word frequency report.
Source file: word_freq_report.txt (tab-separated, BOM, cols: count, word, freq_group, freq_rank, ...)
Output: top 25,000 words with WORD, FREQUENCY_RANKING columns.
"""

import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), "../../DAVE_DOEBRICK/word_freq_report.txt")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "DATA.csv")
TOP_N = 25000


def main():
    rows = []
    with open(INPUT_FILE, encoding="utf-8-sig") as f:  # utf-8-sig strips BOM
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 4:
                continue
            try:
                count = int(parts[0])
                word = parts[1]
                freq_rank = int(parts[3])
                rows.append((word, count, freq_rank))
            except (ValueError, IndexError):
                continue

    # Sort by frequency_rank ascending (rank 1 = most frequent)
    rows.sort(key=lambda x: x[2])

    top = rows[:TOP_N]

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        f.write("WORD,FREQUENCY_RANKING\n")
        for rank, (word, _count, _orig_rank) in enumerate(top, start=1):
            f.write(f"{word},{rank}\n")

    print(f"Written {len(top)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
