"""
Generates DATA.csv from the InnocentRanked Yomitan frequency dictionary (MarvNC collection).
Source: 28 term_meta_bank_N.json files — each entry: [word, "freq", rank]
Output: top 25,000 words with WORD, FREQUENCY_RANKING columns.
"""

import json
import os
import glob

INPUT_DIR = os.path.join(
    os.path.dirname(__file__),
    "../../MARVNC/[JA Freq] InnocentRanked",
)
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "DATA.csv")
TOP_N = 25000


def main():
    # Use glob.escape to handle brackets in directory name
    bank_files = sorted(glob.glob(os.path.join(glob.escape(INPUT_DIR), "term_meta_bank_*.json")))
    print(f"Found {len(bank_files)} bank files")

    rows = []
    for bank_file in bank_files:
        with open(bank_file, encoding="utf-8") as f:
            data = json.load(f)
        for entry in data:
            word = entry[0]
            freq_data = entry[2]
            if isinstance(freq_data, dict):
                rank = freq_data.get("frequency", float("inf"))
            elif isinstance(freq_data, (int, float)):
                rank = freq_data
            else:
                continue
            rows.append((word, rank))

    rows.sort(key=lambda x: x[1])
    top = rows[:TOP_N]

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        f.write("WORD,FREQUENCY_RANKING\n")
        for rank, (word, _orig_rank) in enumerate(top, start=1):
            f.write(f"{word},{rank}\n")

    print(f"Written {len(top)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
