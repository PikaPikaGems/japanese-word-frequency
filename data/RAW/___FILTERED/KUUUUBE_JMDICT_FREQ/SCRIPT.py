"""
Generates DATA.csv from the Kuuuube JMdict Freq Yomitan frequency dictionary.
Source: term_meta_bank_1.json — [word, "freq", {"value": rank, "displayValue": rank}]
Output: top 25,000 words by frequency rank with WORD, FREQUENCY_RANKING columns.

Rank-based frequency data derived from JMdict newspaper processing.
"""

import csv
import json
import os

INPUT_FILE = os.path.join(
    os.path.dirname(__file__),
    "../../KUUUUBE/jmdict_freq/term_meta_bank_1.json",
)
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "DATA.csv")
TOP_N = 25000


def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        entries = json.load(f)

    best_rank: dict[str, int] = {}
    for entry in entries:
        word = entry[0]
        freq_data = entry[2]
        if isinstance(freq_data, dict):
            rank = freq_data.get("value", float("inf"))
        elif isinstance(freq_data, (int, float)):
            rank = freq_data
        else:
            continue
        if word not in best_rank or rank < best_rank[word]:
            best_rank[word] = rank

    rows = sorted(best_rank.items(), key=lambda x: x[1])
    top = rows[:TOP_N]

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["WORD", "FREQUENCY_RANKING"])
        for new_rank, (word, _orig_rank) in enumerate(top, start=1):
            writer.writerow([word, new_rank])

    print(f"Written {len(top)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
