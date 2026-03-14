"""
Generates consolidated_anchor_*.csv and categorized_anchor_*.csv for non-CEJC anchors.
Each file uses one source as the word list backbone, looking up every other source per word.
CEJC is included as a plain source column (combined_rank only).

Bidirectional kana/kanji lookup via JPDB v2 so that:
  - kanji anchor words find kana-keyed sources
  - kana anchor words find CEJC's kanji lemma entries

Anchors generated:
  JPDB             — anime/games/novels, surface forms, 25k words
  YOUTUBE_FREQ_V3  — spoken/conversational YouTube, surface forms, top 30k
  ANIME_JDRAMA     — anime + j-drama subtitles, 25k words
  NETFLIX          — Netflix subtitles, 25k words
"""

import csv
import glob
import os

csv.field_size_limit(10_000_000)

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, "..", "..", "..", ".."))
CEJC_FILE = os.path.join(ROOT, "data", "CEJC", "CONSOLIDATED_UNIQUE.csv")
FILTERED_DIR = os.path.join(ROOT, "data", "RAW", "___FILTERED")
JPDB_RAW = os.path.join(ROOT, "data", "JPDBV2", "jpdb_v2.2_freq_list_2024-10-13.csv")

# (anchor_source_name, max_words_to_include)
ANCHORS = [
    ("JPDB", 25000),
    ("YOUTUBE_FREQ_V3", 30000),
    ("ANIME_JDRAMA", 25000),
    ("NETFLIX", 25000),
]

# ── Build bidirectional kana/kanji lookup from JPDB raw data ─────────────────
# kana_fallback:  kanji → kana  (for kanji anchor words looking up kana-keyed sources)
# kana_to_kanji:  kana  → [kanji forms]  (for kana anchor words looking up CEJC kanji lemmas)
kana_fallback = {}
with open(JPDB_RAW, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f, delimiter="\t"):
        term, reading, freq = row["term"], row["reading"], int(row["frequency"])
        if term == reading:
            continue
        if term not in kana_fallback or freq < kana_fallback[term][1]:
            kana_fallback[term] = (reading, freq)
kana_fallback = {t: r for t, (r, _) in kana_fallback.items()}

kana_to_kanji: dict[str, list[str]] = {}
for kanji, kana in kana_fallback.items():
    kana_to_kanji.setdefault(kana, []).append(kanji)


def lookup(source: dict, word: str) -> int:
    if word in source:
        return source[word]
    # kanji word → try its kana reading in source
    kana = kana_fallback.get(word)
    if kana and kana in source:
        return source[kana]
    # kana word → try any kanji form that reads as this kana in source
    for kanji in kana_to_kanji.get(word, []):
        if kanji in source:
            return source[kanji]
    return -1


# ── Load CEJC as a plain rank source (combined_rank only) ────────────────────
cejc_source: dict[str, int] = {}
with open(CEJC_FILE, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        try:
            cejc_source[row["word"]] = int(row["combined_rank"])
        except (ValueError, KeyError):
            cejc_source[row["word"]] = -1

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
    out_cols = ["word", f"{anchor_name}_rank", "CEJC_rank"] + other_names

    rows = []
    for word, anchor_rank in anchor_words:
        cejc_r = lookup(cejc_source, word)
        other_vals = [lookup(all_sources[s], word) for s in other_names]
        rows.append([word, anchor_rank, cejc_r] + other_vals)

    consol_path = os.path.join(BASE, "..", "..", f"{anchor_name}_anchor", "consolidated.csv")
    categ_path = os.path.join(BASE, "..", "..", f"{anchor_name}_anchor", "categorized.csv")

    with open(consol_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(out_cols)
        w.writerows(rows)

    with open(categ_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(out_cols)
        for row in rows:
            w.writerow([row[0]] + [categorize(int(v)) for v in row[1:]])

    print(f"Anchor {anchor_name}: {len(rows)} words written")

print("Done.")
