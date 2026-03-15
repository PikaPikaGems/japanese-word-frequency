"""
Generates *_anchor/consolidated.csv and *_anchor/categorized.csv for non-CEJC anchors.
Each file uses one source as the word list backbone, looking up every other source per word.
CEJC is included as a plain source column (cejc_combined_rank only).

Bidirectional kana/kanji lookup via JPDB v2 so that:
  - kanji anchor words find kana-keyed sources
  - kana anchor words find CEJC's kanji lemma entries

Anchors generated:
  JPDB             — anime/games/novels, surface forms, 25k words
  YOUTUBE_FREQ_V3  — spoken/conversational YouTube, surface forms, top 25k
  ANIME_JDRAMA     — anime + j-drama subtitles, 25k words
  NETFLIX          — Netflix subtitles, 25k words
"""

import csv
import glob
import os
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
]


jlookup = JapaneseLookup(JPDB_RAW, CEJC_TSV)


# ── Load CEJC as a plain rank source (cejc_combined_rank only) ────────────────────
cejc_source: dict[str, int] = {}
with open(CEJC_FILE, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        try:
            cejc_source[row["word"]] = int(row["cejc_combined_rank"])
        except (ValueError, KeyError):
            cejc_source[row["word"]] = -1

EXCLUDED_SOURCES = {"KOKUGOJITEN", "MONODICTS", "DD2_MIGAKU_NOVELS", "BCCWJ"}

# ── Load all ___FILTERED sources ─────────────────────────────────────────────
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

# ── Load RSPEER (row position = rank; higher zipf_frequency = more frequent = earlier row) ──
rspeer_ranks: dict[str, int] = {}
with open(RSPEER_FILE, newline="", encoding="utf-8") as f:
    for rank, row in enumerate(csv.DictReader(f), start=1):
        w = row["word"]
        if w not in rspeer_ranks:
            rspeer_ranks[w] = rank
all_sources["RSPEER"] = rspeer_ranks


# ── Categorization (mirrors CATEGORIZED.py) ───────────────────────────────────
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
    out_cols = [
        "word",
        "hiragana",
        "katakana",
        f"{anchor_name}_rank",
        "CEJC_rank",
    ] + other_names

    rows = []
    for word, anchor_rank in anchor_words:
        hira, kata = jlookup.get_reading(word)
        cejc_r = jlookup.lookup(cejc_source, word)
        other_vals = [jlookup.lookup(all_sources[s], word) for s in other_names]
        rows.append([word, hira, kata, anchor_rank, cejc_r] + other_vals)

    consol_path = os.path.join(
        BASE, "..", "..", f"{anchor_name}_anchor", "consolidated.csv"
    )
    categ_path = os.path.join(
        BASE, "..", "..", f"{anchor_name}_anchor", "categorized.csv"
    )

    with open(consol_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(out_cols)
        w.writerows(rows)

    with open(categ_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(out_cols)
        for row in rows:
            # word, hiragana, katakana pass through; remaining cols are rank ints
            w.writerow([row[0], row[1], row[2]] + [categorize(int(v)) for v in row[3:]])

    missing = sum(1 for row in rows if row[1] == "-")
    pct = missing / len(rows) * 100 if rows else 0
    print(
        f"Anchor {anchor_name}: {len(rows)} words written  |  kana missing: {missing} ({pct:.1f}%)"
    )

print("Done.")
