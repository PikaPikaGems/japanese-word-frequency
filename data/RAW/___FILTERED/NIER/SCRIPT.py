"""
Generates DATA.csv from the Nier Yomitan frequency dictionary (Shoui collection).
Source: term_meta_bank_1.json — [word, "freq", "rank/total"] (fraction string format)
Output: all ~10k words with WORD, FREQUENCY_RANKING columns.
"""

import json
import os

INPUT_FILE = os.path.join(
    os.path.dirname(__file__),
    "../../SHOUI/[Freq] Nier/term_meta_bank_1.json",
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
            elif isinstance(freq_data, str) and "/" in freq_data:
                rank = float(freq_data.split("/")[0])
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
