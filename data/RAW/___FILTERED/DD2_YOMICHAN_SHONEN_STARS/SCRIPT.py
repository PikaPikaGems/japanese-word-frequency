"""
Generates DATA.csv from Dave Doebrick's Yomichan Shonen Stars frequency list.
Source: Shonen_freq_list_Stars/term_meta_bank_1.json — [[word, "freq", "★★★★★ (rank)"], ...]
Output: top 25,000 words with WORD, FREQUENCY_RANKING columns.
"""

import json
import os
import re

INPUT_FILE = os.path.join(os.path.dirname(__file__), "../../DAVE_DOEBRICK_PART2/YOMICHAN/Shonen_freq_list_Stars/term_meta_bank_1.json")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "DATA.csv")
TOP_N = 25000


def parse_rank(value):
    if isinstance(value, int):
        return value
    m = re.search(r"\((\d+)\)", str(value))
    return int(m.group(1)) if m else None


def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        entries = json.load(f)

    rows = []
    for entry in entries:
        word = entry[0]
        rank = parse_rank(entry[2])
        if rank is not None:
            rows.append((word, rank))

    rows.sort(key=lambda x: x[1])
    top = rows[:TOP_N]

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        f.write("WORD,FREQUENCY_RANKING\n")
        for new_rank, (word, _orig_rank) in enumerate(top, start=1):
            f.write(f"{word},{new_rank}\n")

    print(f"Written {len(top)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
