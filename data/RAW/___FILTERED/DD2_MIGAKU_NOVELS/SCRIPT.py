"""
Generates DATA.csv from Dave Doebrick's Migaku Novel 5k frequency list.
Source: Novel_5k.json — [[word, reading], ...] ordered by frequency rank.
Output: all entries with WORD, FREQUENCY_RANKING columns (~16,469 entries, under 25k cap).
"""

import codecs
import json
import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), "../../DAVE_DOEBRICK_PART2/MIGAKU/Novel_5k.json")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "DATA.csv")
TOP_N = 25000


def main():
    with codecs.open(INPUT_FILE, "r", "utf-8-sig") as f:
        entries = json.load(f)

    rows = [(entry[0], i + 1) for i, entry in enumerate(entries)]
    top = rows[:TOP_N]

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        f.write("WORD,FREQUENCY_RANKING\n")
        for word, rank in top:
            f.write(f"{word},{rank}\n")

    print(f"Written {len(top)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
