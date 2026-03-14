> **Use at your own risk.** The code and logic for generating this data have not been fully reviewed. Data quality, coverage, and methodology vary across sources. No guarantees are made about accuracy, completeness, or fitness for any particular purpose.

# Japanese Word Frequency Rankings

A comprehensive collection of Japanese word frequency datasets, analysis scripts, and insights, consolidating 47+ sources into unified formats for language learning, linguistics, and NLP research.

## References

- [notes/consolidated-reference-verbose.md](notes/consolidated-reference-verbose.md) — Detailed descriptions of all frequency sources
- [notes/consolidated-reference-short.md](notes/consolidated-reference-short.md) — Concise reference format

### Main Data Source

- https://github.com/Kuuuube/yomitan-dictionaries
- https://github.com/MarvNC/yomitan-dictionaries
- https://github.com/IlyaSemenov/wikipedia-word-frequency
- https://github.com/adno/wikipedia-word-frequency-clean
- https://github.com/hermitdave/FrequencyWords/
- https://github.com/chriskempson/japanese-subtitles-word-kanji-frequency-lists
- https://github.com/rspeer/wordfreq
- https://github.com/Maltesaa/CSJ_and_NWJC_yomitan_freq_dict
- https://github.com/hingston/japanese
- https://docs.google.com/spreadsheets/d/1xeG-b85EHwo-yUDgwDLuWyYdwtnDgJAzr3VTmteMOaA
- https://drive.google.com/drive/folders/1g1drkFzokc8KNpsPHoRmDJ4OtMTWFuXi
- https://drive.google.com/drive/folders/1xURpMJN7HTtSLuVs9ZtIbE7MDRCdoU29
- https://drive.google.com/file/d/1qHEfYHXjEp83i6PxxMlSxluFyQg2W8Up
- https://docs.google.com/document/d/1IUWkvBxhoazBSTyRbdyRVk7hfKE51yorE86DCRNQVuw/edit

## Data Quality Notes

[`data/ALL/___experiments0/HISTORY.md`](data/ALL/___experiments0/HISTORY.md) documents the bugs, anomalies, and design decisions discovered while consolidating frequency sources. Key findings:

**Pipeline bugs fixed:**

- Quite a few sources had duplicate word entries; the pipeline now keeps the minimum (most frequent) rank.
- CEJC uses UniDic kanji lemma forms (其れ for それ, 為る for する). A kana fallback via JPDB v2 readings was added to bridge form mismatches.
- AOZORA_BUNKO contains zero hiragana words by design (kanji-only source) and must be excluded from coverage checks.

**Structurally incompatible sources:**
Seven sources are excluded from all coverage quality checks because their -1s reflect structural properties, not word rarity:

| Source               | Reason                                                                                                                     |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| AOZORA_BUNKO         | Kanji-only — all hiragana words absent by design                                                                           |
| NIER                 | Single RPG — only ~10,000 unique tokens total                                                                              |
| ILYASEMENOV          | Wikipedia dump with HTML entities (amp, gt, lt) as "words"                                                                 |
| DD2_MIGAKU_NOVELS    | Curated learner deck — only ~16,500 words, not a frequency corpus                                                          |
| HERMITDAVE_2016/2018 | MeCab morpheme-split tokenization — dictionary-form verbs do not exist as tokens (い at rank #1 is a morpheme, not a word) |
| JPDB                 | Anime/game register — misses 36–42% of general vocabulary (e.g. 企業, 男性, 監督)                                          |

After all 7 exclusions, 28 sources remain. Excluding JPDB alone doubled the zero-missing count.

**Tokenization mismatch:** Even top-1,000 common words are missing from HERMITDAVE because morpheme-split tokenization atomizes verbs — `思う` → `思` + `っ` + `て` + `い` + `る`. This is structural and cannot be fixed by lookup.

**Recommended coverage algorithm:** Use a threshold-based filter (`missing_count ≤ N` across the 28 checked sources) rather than requiring zero-missing. N=3 is the practical working threshold, yielding ~6,000–7,800 broadly common words per anchor. Zero-missing is ~15% overall but ~68–70% for the top-500 words.

**Kana reading enrichment:** `hiragana` and `katakana` columns were added using JPDB v2 as primary source and CEJC UniDic readings as fallback. CEJC and JPDB-anchored files reach 100% coverage; media-anchored files (ANIME, NETFLIX, YOUTUBE) have 6–11% gaps, mostly conjugated verb forms and proper nouns not listed as dictionary headwords.

## Repository Structure

```
word-frequency-rankings/
├── data/
│   ├── ALL/          # Consolidated multi-source rankings (27,988 words × 60+ rank columns)
│   ├── CEJC/         # Corpus of Everyday Japanese Conversation (~2.4M words, 577 conversations)
│   ├── JPDBV2/       # JPDB v2.2 entertainment media frequency list (~497k entries)
│   ├── RSPEER/       # rspeer/wordfreq library output (top 25,000 words)
│   └── RAW/
│       └── ___FILTERED/   # 46+ source datasets, each with a standardized DATA.csv
├── notes/            # Reference documentation for all frequency sources
└── utils/            # Shared Python utilities (formatting helpers)
```

## Datasets

### ALL — Consolidated Rankings

`data/ALL/`

The primary output of this repo. Combines CEJC rankings with all 47 filtered sources plus RSPEER into a single file.

Five anchor variants exist (`CEJC_anchor/`, `JPDB_anchor/`, `ANIME_JDRAMA_anchor/`, `NETFLIX_anchor/`, `YOUTUBE_FREQ_V3_anchor/`), each containing:

- **`consolidated.csv`** — words x rank columns for that anchor

Analysis scripts and reports in `___experiments0/`:

- **`data_generation/`** — pipeline scripts for building consolidated.csv from source DATA.csv files (`SCRIPT.py`, `make_anchored.py`)
- **`coverage_analysis/analyze_coverage.py`** — per-source missing rate, zero-missing subsets, rank-band breakdown; outputs `.md` reports and filtered CSVs
- **`coverage_analysis/filter_words.py`** — quick CEJC-anchor filter: words with any `-1` rank or any rare category
- **`threshold_analysis/threshold_analysis.py`** — filters words present in all-but-N sources; outputs threshold CSVs and summary report
- **`duplicate_detection/`** — script and report for identifying duplicate words within source files
- **`source_insights/`** — scripts for cross-source analysis (correlations, coverage, media profiles, spoken vs. written breakdown, variance)

### CEJC — Everyday Spoken Japanese

`data/CEJC/`

Based on 200 hours of recorded spontaneous speech. Rich demographic breakdown by conversation domain, gender, and age group.

- **`CONSOLIDATED.csv`** — 29,534 entries x 36 rank columns (domain + demographic breakdowns)
- **`CONSOLIDATED_UNIQUE.csv`** — 27,988 deduplicated entries
- insight reports in `insights/`
- analysis scripts in `scripts/`

See [data/CEJC/README.md](data/CEJC/README.md) for dataset details.

### JPDBV2 — Entertainment Media

`data/JPDBV2/`

Frequency data from jpdb.io, sourced from light novels, visual novels, anime, J-drama, and web novels.

- **`task1_top25k.csv`** — Top 25,000 words by reading frequency
- **`task2_kana_higher.csv`** — ~765 words where kana frequency exceeds kanji frequency (~3% of top 25k)
- **`process.py`** — Generates both files from the raw source CSV

See [data/JPDBV2/README.md](data/JPDBV2/README.md) for details.

### RSPEER — wordfreq Library

`data/RSPEER/`

Generated from the [rspeer/wordfreq](https://github.com/rspeer/wordfreq) Python library, which aggregates multiple large corpora.

- **`top_25000_japanese.csv`** — 25,000 words with `frequency` and `zipf_frequency` columns
- 6 plotting scripts for distribution analysis (Zipf, coverage curve, script type, word length, cross-dataset comparison)

See [data/RSPEER/INSIGHTS.md](data/RSPEER/INSIGHTS.md) for analysis results.

### RAW/\_\_\_FILTERED — 46+ Source Datasets + RSPEER

`data/RAW/___FILTERED/`

Each subdirectory contains a standardized `DATA.csv` (columns: `WORD`, `FREQUENCY_RANKING`, top 25k entries) and a `README.md` describing the source. `RSPEER` (`data/RSPEER/top_25000_japanese.csv`) is included as an additional source; its rank is derived from row position (row 1 = rank 1, sorted by descending zipf frequency).

| Source                     | Type                                                |
| -------------------------- | --------------------------------------------------- |
| ADNO                       | Wikipedia (cleaned)                                 |
| ANIME_JDRAMA               | Anime & J-drama subtitles                           |
| AOZORA_BUNKO               | Public domain literature                            |
| BCCWJ                      | Balanced written corpus (NINJAL, 100M words)        |
| CC100                      | Web text (Common Crawl)                             |
| CHRISKEMPSON               | Japanese subtitles                                  |
| DAVE_DOEBRICK              | Netflix subtitles (Dave Doebrick, full report)      |
| DD2_MIGAKU_NETFLIX         | Netflix subtitles (Migaku dictionary format)        |
| DD2_MIGAKU_NOVELS          | Novel corpus (Migaku dictionary format)             |
| DD2_MORPHMAN_NETFLIX       | Netflix subtitles (Morphman report, no names)       |
| DD2_MORPHMAN_NOVELS        | Novel corpus (Morphman report)                      |
| DD2_MORPHMAN_SHONEN        | Shonen anime/manga (Morphman report)                |
| DD2_MORPHMAN_SOL           | Slice of Life anime (Morphman report)               |
| DD2_YOMICHAN_NOVELS        | Novel corpus (Yomichan Stars format)                |
| DD2_YOMICHAN_SHONEN        | Shonen anime/manga (Yomichan integer rank format)   |
| DD2_YOMICHAN_SHONEN_STARS  | Shonen anime/manga (Yomichan Stars format)          |
| DD2_YOMICHAN_SOL           | Slice of Life anime (Yomichan integer rank format)  |
| DD2_YOMICHAN_VN            | Visual novels (Yomichan Stars format)               |
| HERMITDAVE_2016            | Subtitle corpus (2016)                              |
| HERMITDAVE_2018            | Subtitle corpus (2018)                              |
| HINGSTON                   | Japanese internet word frequency (Leeds corpus)     |
| H_FREQ                     | Adult content corpus                                |
| ILYASEMENOV                | Wikipedia word frequency                            |
| INNOCENT_RANKED            | Innocent Corpus (novels)                            |
| JITEN_ANIME                | Anime-focused frequency                             |
| JLAB                       | Anime frequency (Japanese Like a Breeze)            |
| JPDB                       | Entertainment media (jpdb.io)                       |
| KOKUGOJITEN                | Japanese dictionary headwords                       |
| MALTESAA_CSJ               | Corpus of Spontaneous Japanese (CSJ), overall       |
| MALTESAA_CSJ_DOKWA_GAKKAI  | CSJ monologue — academic presentations (独話・学会) |
| MALTESAA_CSJ_DOKWA_MOGI    | CSJ monologue — simulated speeches (独話・模擬)     |
| MALTESAA_CSJ_DOKWA_ROUDOKU | CSJ monologue — reading aloud (独話・朗読)          |
| MALTESAA_CSJ_DOKWA_SAIRO   | CSJ monologue — re-reading (独話・再朗読)           |
| MALTESAA_CSJ_DOKWA_SONOTA  | CSJ monologue — other (独話・その他)                |
| MALTESAA_CSJ_TAIKA_JIYU    | CSJ dialogue — free conversation (対話・自由)       |
| MALTESAA_CSJ_TAIKA_KADAI   | CSJ dialogue — task-based (対話・課題)              |
| MALTESAA_CSJ_TAIKA_MOGI    | CSJ dialogue — simulated (対話・模擬)               |
| MALTESAA_NWJC              | NINJAL Web Japanese Corpus (NWJC)                   |
| MONODICTS                  | Monolingual dictionary terms                        |
| NAROU                      | Web novels (Narou)                                  |
| NETFLIX                    | Netflix subtitle frequency                          |
| NIER                       | NieR game script frequency                          |
| NOVELS                     | Novel corpus                                        |
| RSPEER                     | rspeer/wordfreq multi-corpus aggregate              |
| VN_FREQ                    | Visual novel corpus                                 |
| WIKIPEDIA_V2               | Wikipedia (v2)                                      |
| YOUTUBE_FREQ               | YouTube subtitle frequency                          |
| YOUTUBE_FREQ_V3            | YouTube subtitle frequency (v3, ~187k entries)      |

Note: `DD2_*` sources are from Dave Doebrick's Frequency List Compilation (MIGAKU, MORPHMAN, and YOMICHAN dictionary formats). Three were removed as duplicates: `DD2_YOMICHAN_NETFLIX` (= `NETFLIX`), `DD2_MIGAKU_SOL` (= `DD2_YOMICHAN_SOL`), `DD2_MIGAKU_SHONEN` (= `DD2_YOMICHAN_SHONEN_STARS`). `MALTESAA_*` sources are from Maltesaa's CSJ and NWJC yomitan frequency dictionaries.

See [notes/consolidated-reference-verbose.md](notes/consolidated-reference-verbose.md) for detailed descriptions of all sources.

## Setup

### Requirements

- Python 3.8+
- For plotting scripts: `matplotlib`
- For RSPEER generation: `wordfreq`

### Install dependencies

```bash
pip install matplotlib wordfreq
```

### Running scripts

Scripts under `data/ALL/___experiments0/` can be run from the repo root. CEJC, RSPEER, and JPDB scripts must be run from their own directories:

```bash
# Run coverage analysis across all anchors
python data/ALL/___experiments0/coverage_analysis/analyze_coverage.py

# Quick CEJC-anchor word filter (negative ranks / rare categories)
python data/ALL/___experiments0/coverage_analysis/filter_words.py

# Threshold analysis across all anchors
python data/ALL/___experiments0/threshold_analysis/threshold_analysis.py

# Generate CEJC analysis reports
cd data/CEJC/scripts
python vocab_tier_breakdown.py
python domain_profiles.py
python demographic_analysis.py
# ... (see data/CEJC/scripts/ for all scripts)

# Generate RSPEER data and plots
cd data/RSPEER
python generate_top_japanese.py
python plot_coverage_curve.py
python plot_zipf_distribution.py
# ... (see data/RSPEER/ for all 6 plotting scripts)

# Process JPDB data
cd data/JPDBV2
python process.py
```

## Notable Insights

### Coverage is concentrated (RSPEER)

80% of Japanese text is covered by just ~1,700 words; 90% by ~5,000; 95% by ~9,700; 98% by ~16,000. Focusing on the top 5,000 words gives strong practical coverage for everyday reading.

([Full coverage analysis](data/RSPEER/INSIGHTS.md))

### CEJC rankings are heavily tied at the bottom

Only 430 of 29,534 entries have a unique rank. Most entries share ranks due to tied low-frequency counts, creating a 19,985-rank gap. This is a known artifact of standard competition ranking (1224 style).

([Rank distribution analysis](data/CEJC/insights/rank_distribution.md))

### Cross-source agreement is only partial — and datasets index words differently

**Reading-aware match** (surface form OR kana reading, readings normalized to hiragana): a word in source A counts as matching source B if its surface form equals either the term/key or the reading in B. This catches cases like RSPEER `くれる` ↔ CEJC `呉れる` or JPDB `今` (reading `いま`) ↔ RSPEER `いま`.

| Comparison    | Top 5k | Top 10k | Top 25k |
| ------------- | ------ | ------- | ------- |
| RSPEER ∩ JPDB | 49.7%  | 49.9%   | 50.4%   |
| RSPEER ∩ CEJC | 53.6%  | 51.1%   | 48.8%   |
| JPDB ∩ CEJC   | 54.6%  | 52.1%   | 54.1%   |
| All three     | 40.3%  | 39.9%   | 40.7%   |

Caveats: **Homophones** — the same kana reading can belong to unrelated words (e.g. particle `ば` vs noun `場`), so reading-based matching can introduce false positives.

([Cross-dataset comparison](data/RSPEER/INSIGHTS.md))

### Gender differences in CEJC speech: some robust, some confounded (CEJC)

Some findings are well-supported and linguistically established: gendered first-person pronouns (俺/僕 strongly male, 私 strongly female) and gendered sentence-final particles (ぞ/ぜ male, かしら female) show extreme M/F PMW ratios (3–30×). These reflect real speech style differences.

However, the methodology (raw PMW ratio across all speech by gender) does **not** control for conversation domain. Work/meeting vocabulary (会議, 担当, チーム) skewing male, and food/home vocabulary (野菜, 卵, 菓子) skewing female, may reflect which domains male vs. female participants in this corpus happened to participate in — not an intrinsic property of how men and women speak. Core function words show very little gender skew regardless.

([Demographic analysis](data/CEJC/insights/demographic_analysis.md))

## License

MIT License — Copyright 2026 PikaPikaGems. Individual datasets retain their original licenses and attributions as documented in each source's README.
