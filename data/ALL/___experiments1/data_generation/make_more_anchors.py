"""
Regenerates all non-CEJC anchor consolidated.csv and categorized.csv files,
now including RSPEER, and generates 4 new anchors: BCCWJ, CC100, RSPEER, WIKIPEDIA_V2.

All anchors generated:
  JPDB             — anime/games/novels, surface forms, 25k words
  YOUTUBE_FREQ_V3  — spoken/conversational YouTube, surface forms, top 25k
  ANIME_JDRAMA     — anime + j-drama subtitles, 25k words
  NETFLIX          — Netflix subtitles, 25k words
  BCCWJ            — balanced written Japanese (NINJAL), 25k words
  CC100            — CommonCrawl web text, 25k words
  RSPEER           — multi-source aggregated (wordfreq), 25k words
  WIKIPEDIA_V2     — Wikipedia (clean), 25k words
"""

import csv
import os
import glob
import sys

csv.field_size_limit(10_000_000)

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, "..", "..", "..", ".."))
sys.path.insert(0, ROOT)

from utils import JapaneseLookup  # noqa: E402

CEJC_FILE = os.path.join(ROOT, "data", "CEJC", "CONSOLIDATED_UNIQUE.csv")
FILTERED_DIR = os.path.join(ROOT, "data", "RAW", "___FILTERED")
JPDB_RAW = os.path.join(ROOT, "data", "JPDBV2", "jpdb_v2.2_freq_list_2024-10-13.csv")
CEJC_TSV = os.path.join(ROOT, "data", "CEJC", "2_cejc_frequencylist_suw_token.tsv")
RSPEER_FILE = os.path.join(ROOT, "data", "RSPEER", "top_25000_japanese.csv")

# (anchor_source_name, max_words_to_include)
ANCHORS = [
    ("JPDB", 25000),
    ("YOUTUBE_FREQ_V3", 25000),
    ("ANIME_JDRAMA", 25000),
    ("NETFLIX", 25000),
    ("BCCWJ", 25000),
    ("CC100", 25000),
    ("RSPEER", 25000),
    ("WIKIPEDIA_V2", 25000),
]


jlookup = JapaneseLookup(JPDB_RAW, CEJC_TSV)


# ── Load all CEJC columns ─────────────────────────────────────────────────────
cejc_cols: list[str] = []
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

# ── Load all ___FILTERED sources ─────────────────────────────────────────────
all_sources: dict[str, dict[str, int]] = {}
for path in sorted(glob.glob(os.path.join(FILTERED_DIR, "*", "DATA.csv"))):
    name = os.path.basename(os.path.dirname(path))
    word_rank: dict[str, int] = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            w, r = row["WORD"], int(row["FREQUENCY_RANKING"])
            if w not in word_rank or r < word_rank[w]:
                word_rank[w] = r
    all_sources[name] = word_rank

# ── Load RSPEER (row position = rank; higher zipf_frequency = more frequent = earlier row) ──
rspeer_ranks: dict[str, int] = {}
with open(RSPEER_FILE, newline="", encoding="utf-8") as f:
    for rank, row in enumerate(csv.DictReader(f), start=1):
        w = row["word"]
        if w not in rspeer_ranks:
            rspeer_ranks[w] = rank
all_sources["RSPEER"] = rspeer_ranks


# ── Categorization ────────────────────────────────────────────────────────────
def categorize(rank: int) -> int:
    if rank == -1 or rank > 25000:
        return 1
    elif rank <= 1000:
        return 5
    elif rank <= 4000:
        return 4
    elif rank <= 10000:
        return 3
    else:
        return 2


# ── Generate each anchor ─────────────────────────────────────────────────────
for anchor_name, top_n in ANCHORS:
    anchor_source = all_sources[anchor_name]
    anchor_words = sorted(anchor_source.items(), key=lambda x: x[1])[:top_n]

    other_names = [s for s in sorted(all_sources) if s != anchor_name]
    out_cols = (
        ["word", "hiragana", "katakana", f"{anchor_name}_rank"]
        + cejc_cols
        + other_names
    )

    rows = []
    for word, anchor_rank in anchor_words:
        hira, kata = jlookup.get_reading(word)
        word_cejc = cejc_source.get(word, {})
        cejc_vals = [word_cejc.get(col, -1) for col in cejc_cols]
        other_vals = [jlookup.lookup(all_sources[s], word) for s in other_names]
        rows.append([word, hira, kata, anchor_rank] + cejc_vals + other_vals)

    anchor_dir = os.path.join(BASE, "..", "..", f"{anchor_name}_anchor")
    os.makedirs(anchor_dir, exist_ok=True)
    consol_path = os.path.join(anchor_dir, "consolidated.csv")
    categ_path = os.path.join(anchor_dir, "categorized.csv")

    with open(consol_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(out_cols)
        w.writerows(rows)

    with open(categ_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(out_cols)
        for row in rows:
            w.writerow([row[0], row[1], row[2]] + [categorize(int(v)) for v in row[3:]])

    missing = sum(1 for row in rows if row[1] == "-")
    pct = missing / len(rows) * 100 if rows else 0
    print(
        f"Anchor {anchor_name}: {len(rows)} words written  |  kana missing: {missing} ({pct:.1f}%)"
    )

print("Done.")
