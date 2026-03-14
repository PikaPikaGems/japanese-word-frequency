"""
Cross-dataset overlap using reading-aware matching (corrected methodology).

Methodology (Result B):
  A word in source A is counted as matching source B if its surface form equals
  EITHER the term/key OR the reading in source B (readings normalized to hiragana).

  Specifically:
    RSPEER word W matches JPDB if: W == JPDB.term  OR  W == JPDB.reading
    RSPEER word W matches CEJC if: W == CEJC.key   OR  W == hira(CEJC.reading)
    JPDB entry matches CEJC if:   JPDB.term == CEJC.key  OR  JPDB.reading == hira(CEJC.reading)

  For the three-way count, a JPDB entry is counted if it matches at least one
  CEJC entry (term or reading) AND at least one RSPEER word (term or reading).

  Katakana readings from CEJC JSON are converted to hiragana before comparison.
  JPDB readings are already in hiragana.

Known limitations / potential false positives:
  1. Homophones: the same kana reading can belong to entirely different words.
     E.g. RSPEER's particle "ば" could match JPDB's noun 場 (ば) — these are
     different lexemes. In practice this affects mostly very short function words
     that are already identical in both sources anyway, so the effect is small.
  2. Inflected forms: RSPEER "なく" (surface form of the auxiliary ~なく) could
     match JPDB 泣く/鳴く (reading なく). Without POS tagging there is no way
     to disambiguate purely from the kana string.
  3. RSPEER kanji words without readings: for RSPEER words that contain kanji,
     no reading is available (wordfreq does not expose readings). Matching for
     those words falls back to exact surface-form comparison only. Full reading-
     aware matching for RSPEER kanji forms would require MeCab or similar.
  4. Multiple readings per word: some words have multiple readings (e.g. 一 →
     いち or ひとつ). Only the first/primary reading from CEJC JSON is used.

Results (Result B — reading-aware match):
  Comparison     Top 5k  Top 10k  Top 25k
  RSPEER ∩ JPDB  49.7%   49.9%    50.4%
  RSPEER ∩ CEJC  53.6%   51.1%    48.8%
  JPDB ∩ CEJC    54.6%   52.1%    54.1%
  All three       40.3%   39.9%    40.7%
"""

import csv, json

RSPEER_CSV = "top_25000_japanese.csv"
JPDB_FULL  = "../JPDBV2/JPDB_v2.2_freq_list_2024-10-13.csv"
CEJC_JSON  = "../CEJC/json/CEJC.json"
CEJC_CSV   = "../CEJC/CONSOLIDATED_UNIQUE.csv"

def kata2hira(s):
    return "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ン" else c for c in s)

# Load RSPEER
rspeer_by_rank = []
with open(RSPEER_CSV, encoding="utf-8") as f:
    for row in csv.DictReader(f):
        rspeer_by_rank.append(row["word"])

# Load JPDB: (term, reading_hira) sorted by reading_frequency rank
jpdb_by_rank = []
with open(JPDB_FULL, encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        if not row["frequency"]:
            continue
        jpdb_by_rank.append((row["term"], row["reading"], int(row["frequency"])))
jpdb_by_rank.sort(key=lambda x: x[2])

# Load CEJC JSON for readings
with open(CEJC_JSON, encoding="utf-8") as f:
    cejc_json = json.load(f)

# Load CEJC cejc_combined_rank
cejc_rank_map = {}
with open(CEJC_CSV, encoding="utf-8") as f:
    for row in csv.DictReader(f):
        cejc_rank_map[row["word"]] = int(row["cejc_combined_rank"])

# Build CEJC list: (key, reading_hira, rank) sorted by rank
cejc_by_rank = []
for key, entries in cejc_json.items():
    rank = cejc_rank_map.get(key)
    if rank is None:
        continue
    reading_hira = kata2hira(entries[0]["reading"]) if entries else key
    cejc_by_rank.append((key, reading_hira, rank))
cejc_by_rank.sort(key=lambda x: x[2])

def overlap_reading_aware(n):
    rspeer_words = set(rspeer_by_rank[:n])

    jpdb_top = jpdb_by_rank[:n]
    jpdb_terms   = set(t for t, r, _ in jpdb_top)
    jpdb_readings = set(r for t, r, _ in jpdb_top)

    cejc_top = cejc_by_rank[:n]
    cejc_keys    = set(k for k, r, _ in cejc_top)
    cejc_readings = set(r for k, r, _ in cejc_top)

    # RSPEER ∩ JPDB
    rj = sum(1 for w in rspeer_words if w in jpdb_terms or w in jpdb_readings)

    # RSPEER ∩ CEJC
    rc = sum(1 for w in rspeer_words if w in cejc_keys or w in cejc_readings)

    # JPDB ∩ CEJC
    jc = sum(1 for t, r, _ in jpdb_top if t in cejc_keys or r in cejc_readings)

    # All three: JPDB entry matches CEJC AND matches RSPEER
    a3 = sum(
        1 for t, r, _ in jpdb_top
        if (t in cejc_keys or r in cejc_readings) and (t in rspeer_words or r in rspeer_words)
    )

    return {
        "rspeer_jpdb": rj / n * 100,
        "rspeer_cejc": rc / n * 100,
        "jpdb_cejc":   jc / n * 100,
        "all_three":   a3 / n * 100,
    }

print("=== Result B: Reading-aware match ===")
print(f"{'Comparison':<18} {'Top 5k':>8} {'Top 10k':>8} {'Top 25k':>8}")
labels = [
    ("rspeer_jpdb", "RSPEER ∩ JPDB"),
    ("rspeer_cejc", "RSPEER ∩ CEJC"),
    ("jpdb_cejc",   "JPDB ∩ CEJC"),
    ("all_three",   "All three"),
]
for key, label in labels:
    vals = [overlap_reading_aware(n)[key] for n in [5000, 10000, 25000]]
    print(f"{label:<18} {vals[0]:>7.1f}% {vals[1]:>7.1f}% {vals[2]:>7.1f}%")