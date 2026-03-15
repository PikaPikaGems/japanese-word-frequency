"""
Pairwise reading-aware overlap between all anchor datasets.

For each pair (A, B) at top-N, counts the fraction of A's top-N words that
appear in B's top-N using reading-aware matching:
  A word matches if its surface form OR its hiragana reading equals
  B's surface form or hiragana reading.

Run from repo root:
  python data/ALL/___experiments1/anchor_pairwise_overlap.py
"""

import csv
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ALL_DIR = os.path.abspath(os.path.join(BASE, ".."))

ANCHORS = [
    ("CC100",           "CC100_rank"),
    ("CEJC",            "cejc_combined_rank"),
    ("YOUTUBE_FREQ_V3", "YOUTUBE_FREQ_V3_rank"),
    ("WIKIPEDIA_V2",    "WIKIPEDIA_V2_rank"),
    ("NETFLIX",         "NETFLIX_rank"),
    ("BCCWJ_LUW",       "BCCWJ_LUW_rank"),
    ("BCCWJ_SUW",       "BCCWJ_SUW_rank"),
    ("ANIME_JDRAMA",    "ANIME_JDRAMA_rank"),
    ("RSPEER",          "RSPEER_rank"),
    ("JPDB",            "JPDB_rank"),
]

NS = [5000, 10000, 15000, 25000]


def load_anchor(name, rank_col):
    path = os.path.join(ALL_DIR, f"{name}_anchor", "consolidated.csv")
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                rank = int(row[rank_col])
            except (ValueError, KeyError):
                continue
            if rank < 1:
                continue
            rows.append((rank, row["word"], row.get("hiragana", "-")))
    rows.sort(key=lambda x: x[0])
    return [(w, h) for _, w, h in rows]


def build_lookup(word_hira_list):
    """Build a set of all matchable tokens (surface forms + non-missing readings)."""
    s = set()
    for w, h in word_hira_list:
        s.add(w)
        if h and h != "-":
            s.add(h)
    return s


def overlap_pct(a_list, b_lookup, n):
    top_a = a_list[:n]
    actual_n = len(top_a)
    if actual_n == 0:
        return 0.0
    count = sum(
        1 for w, h in top_a
        if w in b_lookup or (h and h != "-" and h in b_lookup)
    )
    return count / actual_n * 100


# Load all anchors once
print("Loading anchors...")
anchor_data = {}
for name, rank_col in ANCHORS:
    anchor_data[name] = load_anchor(name, rank_col)
    print(f"  {name}: {len(anchor_data[name])} words loaded")

anchor_names = [a[0] for a in ANCHORS]

# Precompute lookups at each N
print()
for n in NS:
    lookups = {name: build_lookup(anchor_data[name][:n]) for name in anchor_names}

    # Header
    col_w = 17
    num_w = 7
    header = f"{'':>{col_w}}" + "".join(f"{name:>{num_w}}" for name in anchor_names)
    sep = "-" * len(header)

    print(f"### Pairwise reading-aware overlap — Top {n:,}")
    print()
    print("Row = source A (denominator). Column = source B.")
    print("Cell = % of A's top-N that appear in B's top-N (reading-aware).")
    print()
    print(header)
    print(sep)

    for a_name in anchor_names:
        row = f"{a_name:>{col_w}}"
        for b_name in anchor_names:
            if a_name == b_name:
                row += f"{'—':>{num_w}}"
            else:
                pct = overlap_pct(anchor_data[a_name], lookups[b_name], n)
                row += f"{pct:>{num_w - 1}.1f}%"
        print(row)

    print()
