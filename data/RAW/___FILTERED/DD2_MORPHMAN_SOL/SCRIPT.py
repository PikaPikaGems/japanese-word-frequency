"""
Generates DATA.csv from Dave Doebrick's Morphman Slice of Life frequency report.
Source: 'Morphman SoL instance_freq_report.txt' — tab-separated Morphman report format.
Columns: count, word, reading, kana, POS, sub_POS, rank, rank2, freq%, cumfreq%, matches, number.
Output: top 25,000 words sorted by rank (col index 6) ascending.
"""

import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), "../../DAVE_DOEBRICK_PART2/MORPHMAN/Morphman SoL instance_freq_report.txt")
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
            if len(parts) < 7:
                continue
            try:
                word = parts[1]
                rank = int(parts[6])
                rows.append((word, rank))
            except (ValueError, IndexError):
                continue

    rows.sort(key=lambda x: x[1])
    top = rows[:TOP_N]

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        f.write("WORD,FREQUENCY_RANKING\n")
        for new_rank, (word, _orig_rank) in enumerate(top, start=1):
            f.write(f"{word},{new_rank}\n")

    print(f"Written {len(top)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
