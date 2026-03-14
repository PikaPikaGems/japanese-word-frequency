"""
Cross-dataset overlap using exact string matching (original methodology).

Methodology (Result A):
  A word in RSPEER is counted as matching JPDB if its surface form is identical
  to the JPDB term string. Same for CEJC: surface form must match the CEJC
  語彙素 key exactly. No reading normalization is applied.

Known limitation:
  This undercounts conceptual overlap because the three sources represent the
  same word differently across scripts. For example:
    - RSPEER: くれる  (hiragana surface)
    - CEJC:   呉れる  (kanji 語彙素 form)
  These are the same word but will not be counted as a match here.

Results (Result A — exact match):
  Comparison     Top 5k  Top 10k  Top 25k
  RSPEER ∩ JPDB  48.2%   48.4%    49.0%
  RSPEER ∩ CEJC  47.9%   46.2%    44.1%
  JPDB ∩ CEJC    42.6%   39.7%    39.4%
  All three       32.2%   31.8%    31.6%
"""

import csv

RSPEER_CSV = "top_25000_japanese.csv"
JPDB_CSV = "../JPDBV2/task1_top25k.csv"
CEJC_CSV = "../CEJC/CONSOLIDATED_UNIQUE.csv"

rspeer_by_rank = []
with open(RSPEER_CSV, encoding="utf-8") as f:
    for i, row in enumerate(csv.DictReader(f), start=1):
        rspeer_by_rank.append(row["word"])

jpdb_by_rank = []
with open(JPDB_CSV, encoding="utf-8") as f:
    for row in csv.DictReader(f):
        jpdb_by_rank.append(row["term"])

cejc_by_rank = []
with open(CEJC_CSV, encoding="utf-8") as f:
    for row in csv.DictReader(f):
        cejc_by_rank.append(row["word"])

def overlap_exact(n):
    rspeer = set(rspeer_by_rank[:n])
    jpdb = set(jpdb_by_rank[:n])
    cejc = set(cejc_by_rank[:n])
    return {
        "rspeer_jpdb": len(rspeer & jpdb) / n * 100,
        "rspeer_cejc": len(rspeer & cejc) / n * 100,
        "jpdb_cejc":   len(jpdb & cejc) / n * 100,
        "all_three":   len(rspeer & jpdb & cejc) / n * 100,
    }

print("=== Result A: Exact string match ===")
print(f"{'Comparison':<18} {'Top 5k':>8} {'Top 10k':>8} {'Top 25k':>8}")
labels = [
    ("rspeer_jpdb", "RSPEER ∩ JPDB"),
    ("rspeer_cejc", "RSPEER ∩ CEJC"),
    ("jpdb_cejc",   "JPDB ∩ CEJC"),
    ("all_three",   "All three"),
]
for key, label in labels:
    vals = [overlap_exact(n)[key] for n in [5000, 10000, 25000]]
    print(f"{label:<18} {vals[0]:>7.1f}% {vals[1]:>7.1f}% {vals[2]:>7.1f}%")
