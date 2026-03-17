"""
Generates DATA.csv from the Jiten NonFiction frequency list CSV.
Source: frequency_list_NonFiction.csv — columns: Word, Form, Rank
Output: top 25,000 words with WORD, FREQUENCY_RANKING columns.
"""

import csv
import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), "../../JITEN/frequency_list_NonFiction.csv")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "DATA.csv")
TOP_N = 25000


def main():
    word_rank = {}
    with open(INPUT_FILE, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row["Word"]
            try:
                rank = float(row["Rank"])
            except (ValueError, KeyError):
                continue
            if word not in word_rank or rank < word_rank[word]:
                word_rank[word] = rank

    rows = sorted(word_rank.items(), key=lambda x: x[1])
    top = rows[:TOP_N]

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        f.write("WORD,FREQUENCY_RANKING\n")
        for new_rank, (word, _orig_rank) in enumerate(top, start=1):
            f.write(f"{word},{new_rank}\n")

    print(f"Written {len(top)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
