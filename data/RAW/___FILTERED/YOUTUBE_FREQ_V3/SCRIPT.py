"""
Generates DATA.csv from the YoutubeFreqV3 Yomitan frequency dictionary (MarvNC collection).
Source: term_meta_bank_1.json — [word, "freq", rank_as_string]
Output: all ~187k words with WORD, FREQUENCY_RANKING columns.
"""

import json
import os

INPUT_FILE = os.path.join(
    os.path.dirname(__file__),
    "../../MARVNC/[JA Freq] YoutubeFreqV3/term_meta_bank_1.json",
)
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "DATA.csv")


def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for entry in data:
        word = entry[0]
        freq_data = entry[2]
        try:
            if isinstance(freq_data, dict):
                rank = float(freq_data.get("value", freq_data.get("frequency", float("inf"))))
            else:
                rank = float(freq_data)
        except (ValueError, TypeError):
            continue
        rows.append((word, rank))

    rows.sort(key=lambda x: x[1])

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        f.write("WORD,FREQUENCY_RANKING\n")
        for rank, (word, _orig_rank) in enumerate(rows, start=1):
            f.write(f"{word},{rank}\n")

    print(f"Written {len(rows)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
