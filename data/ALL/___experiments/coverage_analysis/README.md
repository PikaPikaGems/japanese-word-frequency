# coverage_analysis

Data quality outputs examining how well each source covers the words in each anchor list.

## Motivation

Not all 35 sources have equal coverage. Some cover only 20% of CEJC words; others cover 90%+. Understanding coverage helps:
- Identify which sources are reliable for a given anchor/word
- Flag words that are absent from most sources (unreliable frequency estimates)
- Find a "high confidence" subset of words present in nearly all sources

These files are generated as a side effect of `make_anchored.py` and `SCRIPT.py`.

---

## Files

### Coverage Reports (Markdown)

#### `coverage_analysis.md`
Per-source missing rate across the ~27,988 CEJC words. Shows what % of CEJC words each source lacks a rank for. Useful for understanding which sources have the weakest coverage of everyday spoken vocabulary.

#### `coverage_analysis_anchor_[ANCHOR].md`
Same analysis but for each non-CEJC anchor (JPDB, YOUTUBE_FREQ_V3, ANIME_JDRAMA, NETFLIX). Shows % of anchor words found in each other source. Anchors differ in how well they are covered — media-specific sources cover anime-anchored words better than Wikipedia-anchored words, for example.

**How to interpret:** A high missing rate (e.g., NIER at 81.6%) means that source is sparse for the anchor's vocabulary domain and should be weighted less or excluded from consensus calculations.

---

### Zero-Missing Words (CSV)

#### `zero_missing.csv`
Words from the CEJC anchor that have a valid rank in **every single source** (no -1 values). These are the highest-confidence words — universally covered across all 35 sources. Use as a gold-standard subset for cross-source comparisons.

#### `zero_missing_anchor_[ANCHOR].csv`
Same concept per non-CEJC anchor. Words from the anchor's top-N that appear in all sources. Larger anchors (YOUTUBE_FREQ_V3 at 30k) will have a smaller zero-missing set since more obscure words are included.

---

### Words with Missing Ranks (CSV)

#### `has_negative_rank.csv` / `has_negative_rank_anchor_[ANCHOR].csv`
All words that have at least one `-1` (missing rank) across sources. A superset of every word with incomplete coverage. Useful for identifying which words have gaps and in which specific sources.

**How to interpret:** A word appearing here is not necessarily a bad learning target — it might just be absent from domain-specific sources. Check which columns are -1 to understand the pattern.

---

### Words Categorized as Rare (CSV)

#### `has_rare_category.csv` / `has_rare_category_anchor_[ANCHOR].csv`
Words where at least one source assigns tier 1 (rare: rank 25,001+ or absent). Flags words with shaky frequency standing in at least one corpus.

**How to interpret:** A word with many tier-1 values across sources is likely domain-specific or genuinely uncommon. A word with only one or two tier-1 values likely just has sparse coverage in those particular sources.

---

## Anchors covered

All files come in five variants:
- `*_CEJC` — anchored on CEJC spoken corpus (~27,988 words)
- `*_JPDB` — anchored on JPDB top 25,000 (games/anime/novels)
- `*_YOUTUBE_FREQ_V3` — anchored on YouTube top 30,000 (conversational)
- `*_ANIME_JDRAMA` — anchored on anime + J-drama subtitles top 25,000
- `*_NETFLIX` — anchored on Netflix subtitles top 25,000
