"""
Generates DATA.csv from the Jiten (Anime) Yomitan frequency dictionary (Shoui collection).
Source: term_meta_bank_1.json — mixed format entries:
  - [word, "freq", {"value": rank, "displayValue": "rank㋕"}]
  - [word, "freq", {"reading": r, "frequency": {"value": rank, "displayValue": "rank㋕"}}]
Output: top 25,000 words with WORD, FREQUENCY_RANKING columns.
"""

import json
import os

INPUT_FILE = os.path.join(
    os.path.dirname(__file__),
    "../../SHOUI/[Freq] Jiten (Anime)/term_meta_bank_1.json",
)
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "DATA.csv")
TOP_N = 25000


def extract_rank(freq_data):
    """Extract numeric rank from various freq_data formats."""
    if isinstance(freq_data, (int, float)):
        return float(freq_data)
    if isinstance(freq_data, str):
        try:
            return float(freq_data)
        except ValueError:
            return float("inf")
    if isinstance(freq_data, dict):
        # Nested format: {"reading": r, "frequency": {"value": rank}}
        if "frequency" in freq_data:
            inner = freq_data["frequency"]
            if isinstance(inner, dict):
                return float(inner.get("value", float("inf")))
            return float(inner)
        # Direct format: {"value": rank}
        if "value" in freq_data:
            return float(freq_data["value"])
        if "frequency" in freq_data:
            return float(freq_data["frequency"])
    return float("inf")


def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        data = json.load(f)

    # Collect best (lowest) rank per word
    word_rank = {}
    for entry in data:
        word = entry[0]
        rank = extract_rank(entry[2])
        if rank == float("inf"):
            continue
        if word not in word_rank or rank < word_rank[word]:
            word_rank[word] = rank

    rows = sorted(word_rank.items(), key=lambda x: x[1])
    top = rows[:TOP_N]

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        f.write("WORD,FREQUENCY_RANKING\n")
        for rank, (word, _orig_rank) in enumerate(top, start=1):
            f.write(f"{word},{rank}\n")

    print(f"Written {len(top)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
