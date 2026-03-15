"""
Generates DATA.csv from the toasted-nutbread BCCWJ-LUW Yomitan frequency dictionary.
Source: term_meta_bank_*.json files — [word, "freq", {"reading": r, "frequency": rank}]
Output: top 25,000 words by frequency rank with WORD, FREQUENCY_RANKING columns.

LUW = Long Unit Word: compound words and verb+auxiliary sequences are treated as single
units. For example, 食べました is one LUW, whereas SUW splits it into 食べる + ます.
LUW ranks tend to surface more content words and compound expressions.
"""

import csv
import glob
import json
import os

INPUT_DIR = os.path.join(
    os.path.dirname(__file__),
    "../../TOASTED-NUTBREAD/BCCWJ-LUW",
)
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "DATA.csv")
TOP_N = 25000


def main():
    entries = []
    for path in sorted(glob.glob(os.path.join(INPUT_DIR, "term_meta_bank_*.json"))):
        with open(path, encoding="utf-8") as f:
            entries.extend(json.load(f))

    rows = []
    seen = set()
    for entry in entries:
        word = entry[0]
        freq_data = entry[2]
        if isinstance(freq_data, dict):
            rank = freq_data.get("frequency", float("inf"))
        elif isinstance(freq_data, (int, float)):
            rank = freq_data
        else:
            continue
        if word not in seen:
            seen.add(word)
            rows.append((word, rank))

    rows.sort(key=lambda x: x[1])
    top = rows[:TOP_N]

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["WORD", "FREQUENCY_RANKING"])
        for new_rank, (word, _orig_rank) in enumerate(top, start=1):
            writer.writerow([word, new_rank])

    print(f"Written {len(top)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
