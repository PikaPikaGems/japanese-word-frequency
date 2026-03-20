"""
Generates data/ALL/RIRIKKU_CONSOLIDATED.csv

Word list: union of all words in the top-25k of any shortlisted source.
RIRIKKU_RANK: minimum rank across all shortlisted sources, requiring
              at least 3 sources to have the word (rank != -1).
              Words with fewer than 3 sources are assigned rank -1.

Output columns:
  word, hiragana, katakana, RIRIKKU_RANK,
  [SHORTLISTED columns — used for rank computation]
  RSPEER, cejc_combined_rank, cejc_small_talk_rank,
  BCCWJ_LUW, BCCWJ_SUW, CC100, MALTESAA_NWJC,
  JITEN_GLOBAL, JITEN_DRAMA, ANIME_JDRAMA,
  YOUTUBE_FREQ_V3, NETFLIX, DD2_MORPHMAN_NETFLIX,
  WIKIPEDIA_V2, ADNO, DD2_MORPHMAN_SOL,
  [EXTRA columns — informational only, not used for rank]
  JITEN_ANIME_V2

Sort order: RIRIKKU_RANK ascending (unranked words last), then word.
"""

import csv
import glob
import os
import sys

csv.field_size_limit(10_000_000)

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
sys.path.insert(0, ROOT)

from utils import JapaneseLookup  # noqa: E402

CEJC_FILE = os.path.join(ROOT, "data", "CEJC", "CONSOLIDATED_UNIQUE.csv")
FILTERED_DIR = os.path.join(ROOT, "data", "RAW", "___FILTERED")
JPDB_RAW = os.path.join(ROOT, "data", "JPDBV2", "jpdb_v2.2_freq_list_2024-10-13.csv")
CEJC_TSV = os.path.join(ROOT, "data", "CEJC", "2_cejc_frequencylist_suw_token.tsv")
RSPEER_FILE = os.path.join(ROOT, "data", "RSPEER", "top_25000_japanese.csv")
OUT_FILE = os.path.join(ROOT, "data", "ALL", "RIRIKKU_CONSOLIDATED.csv")

# Sources used for RIRIKKU_RANK computation and included as output columns.
# Keys match all_sources dict keys (loaded below) or special CEJC keys.
# MALTESAA_CSJ is intentionally excluded (formal academic speech, wrong register).
# JITEN_ANIME_V2 is excluded from rank computation but included as an extra output column.
SHORTLISTED = [
    "RSPEER",
    "cejc_combined_rank",
    "cejc_small_talk_rank",
    "BCCWJ_LUW",
    "BCCWJ_SUW",
    "CC100",
    "MALTESAA_NWJC",
    "JITEN_GLOBAL",
    "JITEN_DRAMA",
    "ANIME_JDRAMA",
    "YOUTUBE_FREQ_V3",
    "NETFLIX",
    "DD2_MORPHMAN_NETFLIX",
    "WIKIPEDIA_V2",
    "ADNO",
    "DD2_MORPHMAN_SOL",
]

# Extra columns included in output for reference but NOT used for RIRIKKU_RANK computation.
EXTRA_COLS = [
    "JITEN_ANIME_V2",
]

CEJC_SHORTLISTED = {"cejc_combined_rank", "cejc_small_talk_rank"}

# ── Load reading lookup ───────────────────────────────────────────────────────
jlookup = JapaneseLookup(JPDB_RAW, CEJC_TSV)

# ── Load CEJC columns ─────────────────────────────────────────────────────────
# cejc_source: word → {col: rank}
cejc_source: dict[str, dict[str, int]] = {}
with open(CEJC_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    cejc_cols = [c for c in reader.fieldnames if c != "word"]
    for row in reader:
        word = row["word"]
        cejc_source[word] = {}
        for col in cejc_cols:
            try:
                cejc_source[word][col] = int(row[col])
            except (ValueError, KeyError):
                cejc_source[word][col] = -1

EXCLUDED_SOURCES = {"KOKUGOJITEN", "MONODICTS", "DD2_MIGAKU_NOVELS", "BCCWJ"}

# ── Load all ___FILTERED sources ──────────────────────────────────────────────
all_sources: dict[str, dict[str, int]] = {}
for path in sorted(glob.glob(os.path.join(FILTERED_DIR, "*", "DATA.csv"))):
    name = os.path.basename(os.path.dirname(path))
    if name in EXCLUDED_SOURCES:
        continue
    word_rank: dict[str, int] = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            w, r = row["WORD"], int(row["FREQUENCY_RANKING"])
            if w not in word_rank or r < word_rank[w]:
                word_rank[w] = r
    all_sources[name] = word_rank

# ── Load RSPEER ───────────────────────────────────────────────────────────────
rspeer_ranks: dict[str, int] = {}
with open(RSPEER_FILE, newline="", encoding="utf-8") as f:
    for rank, row in enumerate(csv.DictReader(f), start=1):
        w = row["word"]
        if w not in rspeer_ranks:
            rspeer_ranks[w] = rank
all_sources["RSPEER"] = rspeer_ranks

# ── Build union word list ─────────────────────────────────────────────────────
# Include every word in the top-25k of any shortlisted source.
union_words: set[str] = set()

for col in SHORTLISTED:
    if col in CEJC_SHORTLISTED:
        for word, ranks in cejc_source.items():
            r = ranks.get(col, -1)
            if r != -1:
                union_words.add(word)
    else:
        source = all_sources.get(col, {})
        union_words.update(source.keys())

print(f"Union word list: {len(union_words):,} words")

# ── Build flat dicts for CEJC shortlisted columns (word → rank) ──────────────
# These are used with jlookup.lookup() for bidirectional kana/kanji resolution.
cejc_flat: dict[str, dict[str, int]] = {}
for col in CEJC_SHORTLISTED:
    cejc_flat[col] = {word: ranks.get(col, -1) for word, ranks in cejc_source.items()}

# ── Compute RIRIKKU_RANK and collect all shortlisted ranks per word ───────────
def get_shortlisted_ranks(word: str) -> dict[str, int]:
    result: dict[str, int] = {}
    for col in SHORTLISTED:
        if col in CEJC_SHORTLISTED:
            result[col] = jlookup.lookup(cejc_flat[col], word)
        else:
            result[col] = jlookup.lookup(all_sources.get(col, {}), word)
    return result


def get_extra_ranks(word: str) -> dict[str, int]:
    return {col: jlookup.lookup(all_sources.get(col, {}), word) for col in EXTRA_COLS}


rows = []
for word in union_words:
    hira, kata = jlookup.get_reading(word)
    ranks = get_shortlisted_ranks(word)
    extra = get_extra_ranks(word)
    valid = [r for r in ranks.values() if r != -1]
    ririkku_rank = min(valid) if len(valid) >= 3 else -1
    rows.append((word, hira, kata, ririkku_rank, ranks, extra))

# Sort: ranked words first (ascending), unranked last, then word alphabetically
rows.sort(key=lambda x: (x[3] == -1, x[3], x[0]))

# ── Write output ──────────────────────────────────────────────────────────────
out_cols = ["word", "hiragana", "katakana", "RIRIKKU_RANK"] + SHORTLISTED + EXTRA_COLS

with open(OUT_FILE, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(out_cols)
    for word, hira, kata, ririkku_rank, ranks, extra in rows:
        w.writerow([word, hira, kata, ririkku_rank] + [ranks[col] for col in SHORTLISTED] + [extra[col] for col in EXTRA_COLS])

ranked_count = sum(1 for _, _, _, r, _, _ in rows if r != -1)
unranked_count = len(rows) - ranked_count
missing_reading = sum(1 for _, h, _, _, _, _ in rows if h == "-")
pct_missing = missing_reading / len(rows) * 100 if rows else 0

print(f"Total words:       {len(rows):,}")
print(f"Ranked (>=3 src):  {ranked_count:,}")
print(f"Unranked (<3 src): {unranked_count:,}")
print(f"Missing reading:   {missing_reading:,} ({pct_missing:.1f}%)")
print(f"Written to:        {OUT_FILE}")
