"""
Generates DATA.csv from Kuuube's h_freq_list.tsv (adult content word frequency).
Source: h_freq_list.tsv — tab-separated word\tcount, no header, pre-sorted by count desc.
Output: top 25,000 words with WORD, FREQUENCY_RANKING columns.
"""

import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), "../../KUUUUBE/h_freq_list.tsv")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "DATA.csv")
TOP_N = 25000


def main():
    rows = []
    with open(INPUT_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) < 2:
                continue
            word = parts[0]
            try:
                count = int(parts[1])
            except ValueError:
                continue
            rows.append((word, count))

    rows.sort(key=lambda x: x[1], reverse=True)
    top = rows[:TOP_N]

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        f.write("WORD,FREQUENCY_RANKING\n")
        for rank, (word, _count) in enumerate(top, start=1):
            f.write(f"{word},{rank}\n")

    print(f"Written {len(top)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
