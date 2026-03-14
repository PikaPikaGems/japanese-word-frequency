"""
Generates DATA.csv from the Hingston Japanese word frequency list.
Source: 44998-japanese-words.txt — one word per line, ordered by frequency (line 1 = rank 1).
Derived from the University of Leeds Corpus (http://corpus.leeds.ac.uk/frqc/internet-jp.num).
Output: top 25,000 words with WORD, FREQUENCY_RANKING columns.
"""

import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), "../../HINGSTON/44998-japanese-words.txt")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "DATA.csv")
TOP_N = 25000


def main():
    rows = []
    with open(INPUT_FILE, encoding="utf-8") as f:
        for line in f:
            word = line.rstrip("\n")
            if word:
                rows.append(word)
            if len(rows) >= TOP_N:
                break

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        f.write("WORD,FREQUENCY_RANKING\n")
        for rank, word in enumerate(rows, start=1):
            f.write(f"{word},{rank}\n")

    print(f"Written {len(rows)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
