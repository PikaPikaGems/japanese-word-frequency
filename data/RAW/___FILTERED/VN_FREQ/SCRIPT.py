"""
Generates DATA.csv from the VN Freq v2 Yomitan frequency dictionary (Shoui collection).
Source: term_meta_bank_1.json — [word, "freq", {"reading": r, "frequency": rank}]
Output: top 25,000 words with WORD, FREQUENCY_RANKING columns.
"""

import json
import os

INPUT_FILE = os.path.join(
    os.path.dirname(__file__),
    "../../SHOUI/[Freq] VN Freq v2/term_meta_bank_1.json",
)
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "DATA.csv")
TOP_N = 25000


def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for entry in data:
        word = entry[0]
        freq_data = entry[2]
        try:
            if isinstance(freq_data, dict):
                rank = float(freq_data.get("frequency", freq_data.get("value", float("inf"))))
            else:
                rank = float(freq_data)
        except (ValueError, TypeError):
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
