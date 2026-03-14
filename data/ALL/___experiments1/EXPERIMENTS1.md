# Experiments 1 — Plan and Findings

## Context

The original §13 experiments in `___experiments0/HISTORY.md` were run with ~30 sources across 5 anchors (CEJC, JPDB, ANIME_JDRAMA, NETFLIX, YOUTUBE_FREQ_V3). Since then:

- The dataset has grown to **49 external source columns** (up from ~35)
- **RSPEER** was added to CEJC_anchor but the other 4 non-CEJC anchors were never regenerated with it
- The recommended EXCLUDE additions from §12 (H_FREQ, NAROU, VN_FREQ) were never applied

This experiment set addresses all three gaps.

---

## New Anchors

Four new anchors are added, chosen for broad coverage and surface-form tokenization:

| Anchor | Source | Type | Words |
| --- | --- | --- | --- |
| BCCWJ | NINJAL Balanced Corpus of Contemporary Written Japanese | Books, magazines, newspapers, blogs, forums (balanced) | 25,000 |
| CC100 | CommonCrawl 100 (Seikou/arujisho) | Web text (broad) | 25,000 |
| RSPEER | rspeer/wordfreq | Multi-source aggregated (Wikipedia + subtitles + news + web + Twitter/Reddit) | 25,000 |
| WIKIPEDIA_V2 | Shoui Wikipedia v2 | Wikipedia (clean) | 25,000 |

All four use surface-form tokenization (top entries: の, に, は, て, が — not UniDic lemmas like 其れ or 為る).

**Rejected candidates:**
- JLAB — anime-subtitle-specific, too domain-narrow for anchor use
- NOVELS — punctuation (、。) at ranks 1 and 3, would distort coverage analysis
- MALTESAA_NWJC — parentheses （） at ranks 1 and 3
- INNOCENT_RANKED — unusual ordering (要る at rank 1)

Together with the 5 existing anchors, this gives **9 total anchors** representing:
- Spoken: CEJC, YOUTUBE_FREQ_V3
- Subtitle: ANIME_JDRAMA, NETFLIX, JPDB
- Web: CC100, WIKIPEDIA_V2, RSPEER
- Balanced written: BCCWJ

---

## Updated EXCLUDE Set

Per the recommendation in §12, H_FREQ, NAROU, and VN_FREQ are added:

```
EXCLUDE = {
    "AOZORA_BUNKO",       # kanji-only source — zero hiragana words by design
    "NIER",               # single game, ~10k words total
    "ILYASEMENOV",        # Wikipedia dump with HTML entities, wrong domain
    "DD2_MIGAKU_NOVELS",  # curated learner deck, ~16k words
    "HERMITDAVE_2016",    # MeCab morpheme-split — dictionary-form verbs absent
    "HERMITDAVE_2018",    # same tokenization as HERMITDAVE_2016
    "JPDB",               # anime/game corpus — misses general vocabulary
    "H_FREQ",             # adult content corpus — basic particles absent
    "NAROU",              # UniDic kanji lemma forms — particles absent
    "VN_FREQ",            # UniDic kanji lemma forms — particles absent
}
```

This leaves **~39 checked sources** (up from 28 in the old experiments).

---

## Scripts

### `data_generation/make_more_anchors.py`

Regenerates all 4 existing non-CEJC anchors (now including RSPEER column) and generates the 4 new ones:

```
ANCHORS = [
    ("JPDB", 25000),
    ("YOUTUBE_FREQ_V3", 30000),
    ("ANIME_JDRAMA", 25000),
    ("NETFLIX", 25000),
    ("BCCWJ", 25000),
    ("CC100", 25000),
    ("RSPEER", 25000),
    ("WIKIPEDIA_V2", 25000),
]
```

Output directories: `data/ALL/{ANCHOR}_anchor/consolidated.csv` and `categorized.csv`.

### `coverage_analysis/analyze_coverage.py`

Same logic as `___experiments0/coverage_analysis/analyze_coverage.py` but:
- Uses updated 10-source EXCLUDE set
- Outputs to `___experiments1/coverage_analysis/`
- Runs on all 9 `*_anchor/` directories

### `coverage_analysis/threshold_analysis.py`

Same logic as `___experiments0/threshold_analysis/threshold_analysis.py` but:
- Uses updated 10-source EXCLUDE set
- Outputs to `___experiments1/coverage_analysis/`
- Runs on all 9 `*_anchor/` directories

---

## Findings

See `HISTORY.md` for full findings. Summary:

- BCCWJ only yields 16,491 unique words (UniDic POS duplication) — not usable as a comparable anchor
- CC100 has the strongest top-500 coverage at **85.6%** zero-missing
- ANIME_JDRAMA and NETFLIX have the best high-frequency density: **29.4%** of 25k words pass N≤3
- JPDB remains the outlier: only **11.8%** at N≤3, confirms exclusion from quality checks
- CEJC checks 51 sources (vs 38 for others) due to sub-corpus columns — not directly comparable
- Removing H_FREQ/NAROU/VN_FREQ from checks and adding new sources nets a ~+0.3pp improvement in zero-missing for YOUTUBE
