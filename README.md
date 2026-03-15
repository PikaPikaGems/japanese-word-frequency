> **Use at your own risk.** The code and logic for generating this data have not been fully reviewed. Data quality, coverage, and methodology vary across sources. No guarantees are made about accuracy, completeness, or fitness for any particular purpose.

# Japanese Word Frequency Rankings

A comprehensive collection of Japanese word frequency datasets, analysis scripts, and insights, consolidating 47+ datasets into unified formats for language learning, linguistics, and NLP research.

## References

- [CONSOLIDATED_CSV_REFERENCEV1.md](CONSOLIDATED_CSV_REFERENCEV1.md) — How to read `consolidated.csv`: column layout, what `-1` means, practical interpretation guide, and per-source caveats

- [notes/consolidated-reference-verbose.md](notes/consolidated-reference-verbose.md) — Detailed descriptions of all frequency sources
- [notes/consolidated-reference-short.md](notes/consolidated-reference-short.md) — Concise reference format

- [notes/cleaned-datasets-reference-v1.md](notes/cleaned-datasets-reference-v1.md) — Detailed descriptions of every frequency rank dataset included in the database, with source notes on corpus size, register, and tokenization

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

## Repository Structure

```
word-frequency-rankings/
├── data/
│   ├── ALL/          # Consolidated multi-source rankings (27,988 words × 60+ rank columns)
│   ├── CEJC/         # Corpus of Everyday Japanese Conversation (~2.4M words, 577 conversations)
│   ├── JPDBV2/       # JPDB v2.2 entertainment media frequency list (~497k entries)
│   ├── RSPEER/       # rspeer/wordfreq library output (top 25,000 words)
│   └── RAW/
│       └── ___FILTERED/   # 46+ datasets, each with a standardized DATA.csv
├── notes/            # Reference documentation for all frequency sources
└── utils/            # Shared Python utilities (formatting, kana conversion, JP word lookup)
```

## Datasets

### ALL — Consolidated Rankings

`data/ALL/`

The primary output of this repo. Each `consolidated.csv` is a matrix of **words × rank columns**, one column per frequency source. The **anchor** is the source whose word list defines the rows — every word in the anchor appears as a row, and each column shows that word's rank in the other sources (`-1` if absent). Different anchors produce different matrices because each source has different vocabulary coverage and tokenization. Nine anchor variants exist: CEJC, BCCWJ, CC100, RSPEER, WIKIPEDIA_V2, ANIME_JDRAMA, NETFLIX, YOUTUBE_FREQ_V3, and JPDB. Analysis scripts and reports in `___experiments0/` and `___experiments1/`:
Please see: [CONSOLIDATED_CSV_REFERENCEV1.md](CONSOLIDATED_CSV_REFERENCEV1.md) for more details.

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
| YOUTUBE_FREQ_V3            | YouTube subtitle frequency (v3, top 25k)            |

Note: `DD2_*` sources are from Dave Doebrick's Frequency List Compilation (MIGAKU, MORPHMAN, and YOMICHAN dictionary formats). Three were removed as duplicates: `DD2_YOMICHAN_NETFLIX` (= `NETFLIX`), `DD2_MIGAKU_SOL` (= `DD2_YOMICHAN_SOL`), `DD2_MIGAKU_SHONEN` (= `DD2_YOMICHAN_SHONEN_STARS`). `MALTESAA_*` sources are from Maltesaa's CSJ and NWJC yomitan frequency dictionaries.

See [notes/consolidated-reference-verbose.md](notes/consolidated-reference-verbose.md) for detailed descriptions of all sources.

## Data Quality Notes

### Inspecting the JPDB dataset

- **Surface forms, not lemmas.** JPDB records exactly what was written in the source texts. Inflected and compound forms appear as separate top-ranked entries: `だった` (rank 24), `には` (rank 26), `だろう` (rank 37), `けど` (rank 38), `だから` (rank 43), `ではない` (rank 89), `ことになる` (rank 167). Every other source (CEJC, RSPEER, BCCWJ, etc.) lemmatizes these to their base forms (`だ`, `けれど`, etc.), so the same underlying word occupies a completely different slot in JPDB's list.

- **Entertainment media-specific vocabulary.** Fantasy and RPG terms (`ギルド`, `ダンジョン`, `スケルトン`, `リザードマン`) and light novel tropes (`ハーレム`, `クラスメイト`) appear in JPDB's top 5k but are absent from general-language corpora.

- **Onomatopoeia and expressive words.** Words like `ぺこり`, `にこり`, `ゆらり`, `ぐるりと`, `ちょこん` are extremely common in fiction narration (describing character movements and expressions) but are rare in general or spoken Japanese.

- **Multi-morpheme phrases as single entries.** Expressions like `ことによって`, `よりによって`, `それゆえに` are stored as single vocabulary items rather than being decomposed into constituent morphemes.

## Experiments 0

[`data/ALL/___experiments0/HISTORY.md`](data/ALL/___experiments0/HISTORY.md) documents the bugs, anomalies, and design decisions discovered while consolidating frequency sources.

**Pipeline bugs fixed:**

- Quite a few sources had duplicate word entries; the pipeline now keeps the minimum (most frequent) rank.
- CEJC uses UniDic kanji lemma forms (其れ for それ, 為る for する). A bidirectional kana/kanji fallback via JPDB v2 readings was added to bridge form mismatches: kanji anchor words look up their kana reading in other sources, and kana anchor words look up any kanji form that shares the same reading.
- AOZORA_BUNKO contains zero hiragana words by design (kanji-only source) and must be excluded from coverage checks.

**Structurally incompatible sources:**
Seven sources are excluded from all coverage quality checks because their -1s reflect structural properties, not word rarity:

| Source               | Reason                                                                                                                                                                  |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AOZORA_BUNKO         | Kanji-only — all hiragana words absent by design                                                                                                                        |
| NIER                 | Single RPG — only ~10,000 unique tokens total                                                                                                                           |
| ILYASEMENOV          | Wikipedia dump with HTML entities (amp, gt, lt) as "words"                                                                                                              |
| DD2_MIGAKU_NOVELS    | Curated learner deck — only ~16,500 words, not a frequency corpus                                                                                                       |
| HERMITDAVE_2016/2018 | MeCab morpheme-split tokenization — dictionary-form verbs do not exist as tokens (い at rank #1 is a morpheme, not a word)                                              |
| JPDB                 | Anime/game register — Surface forms, not lemmas. JPDB records exactly what was written in the source texts. misses 36–42% of general vocabulary (e.g. 企業, 男性, 監督) |

**Tokenization mismatch:** Even top-1,000 common words are missing from HERMITDAVE because morpheme-split tokenization atomizes verbs — `思う` → `思` + `っ` + `て` + `い` + `る`. This is structural and cannot be fixed by lookup.

**Kana reading enrichment:** `hiragana` and `katakana` columns for each word are included per row media-anchored files (ANIME, NETFLIX, YOUTUBE) have 6–11% gaps, mostly conjugated verb forms and proper nouns not listed as dictionary headwords.

## Experiments 1

[`data/ALL/___experiments1/HISTORY.md`](data/ALL/___experiments1/HISTORY.md) documents findings from re-running coverage experiments after the dataset grew from ~35 to 49 external sources and 4 new anchors were added.

**New anchors added (9 total):**

| Anchor       | Type                               | Words                                    |
| ------------ | ---------------------------------- | ---------------------------------------- |
| BCCWJ        | Balanced written Japanese (NINJAL) | 16,491 unique (UniDic POS deduplication) |
| CC100        | CommonCrawl web text               | 24,605                                   |
| RSPEER       | Multi-source aggregated (wordfreq) | 25,000                                   |
| WIKIPEDIA_V2 | Wikipedia (clean)                  | 25,000                                   |

**Updated EXCLUDE set (10 sources):** H_FREQ, NAROU, and VN_FREQ added to the original 7 — all use UniDic kanji lemma forms or domain-skewed tokenization that causes basic particles to score as absent.

**How to read these tables:**

- **Top-N %** (zero-missing): of the first N words in the anchor's frequency list, the percentage that appear in _every_ checked source (no `-1` rank). A high Top-500 means the most common words are universally found everywhere. The percentage naturally falls as N grows because rarer words start appearing in fewer domain-specific corpora.
- **N≤3**: words missing from _at most 3_ of the ~38 checked sources — the "broadly common" core vocabulary present in nearly all corpora.

**Zero-missing by rank band** ([`top12k/`](data/ALL/___experiments1/top12k/HISTORY.md)):

| Anchor          | Top-500 | Top-1k | Top-3k | Top-5k | Top-12k |
| --------------- | ------- | ------ | ------ | ------ | ------- |
| CC100           | 83.2%   | 76.5%  | 61.7%  | 51.1%  | 28.9%   |
| CEJC            | 78.2%   | 72.1%  | 56.0%  | 45.0%  | 26.3%   |
| BCCWJ           | 75.0%   | 74.0%  | 63.6%  | 52.3%  | 29.3%   |
| WIKIPEDIA_V2    | 73.4%   | 69.8%  | 53.4%  | 44.4%  | 26.7%   |
| NETFLIX         | 65.4%   | 61.0%  | 50.9%  | 42.9%  | 27.2%   |
| YOUTUBE_FREQ_V3 | 63.4%   | 62.4%  | 54.8%  | 47.0%  | 27.9%   |
| RSPEER          | 57.6%   | 57.3%  | 52.1%  | 45.2%  | 27.9%   |
| ANIME_JDRAMA    | 55.8%   | 55.2%  | 47.0%  | 39.4%  | 25.6%   |
| JPDB            | 18.0%   | 11.2%  | 4.9%   | 3.3%   | 1.5%    |

**N≤3 missing sources by rank band** (top-12k slices, [`n_leq3_by_rank_band.py`](data/ALL/___experiments1/top12k/n_leq3_by_rank_band.py)):

| Anchor          | Top-500 | Top-1k | Top-3k | Top-5k | Top-12k | N≤3 @25k              |
| --------------- | ------- | ------ | ------ | ------ | ------- | --------------------- |
| CC100           | 92.4%   | 88.0%  | 77.0%  | 67.6%  | 44.4%   | 5,935 (24.1%)         |
| CEJC            | 92.6%   | 90.2%  | 76.6%  | 63.4%  | 39.8%   | 6,075 (21.7%)         |
| BCCWJ           | 83.0%   | 82.9%  | 76.8%  | 68.3%  | 45.0%   | —                     |
| WIKIPEDIA_V2    | 83.2%   | 79.5%  | 65.6%  | 56.5%  | 37.3%   | 5,568 (22.3%)         |
| YOUTUBE_FREQ_V3 | 70.6%   | 73.1%  | 68.3%  | 61.6%  | 41.4%   | 5,786 (23.1%)         |
| NETFLIX         | 71.0%   | 69.4%  | 63.5%  | 56.9%  | 39.8%   | 5,728 (22.9%)         |
| RSPEER          | 63.6%   | 65.8%  | 63.7%  | 58.0%  | 39.7%   | 5,666 (22.7%)         |
| ANIME_JDRAMA    | 62.6%   | 63.4%  | 59.5%  | 53.0%  | 37.5%   | 5,669 (22.7%)         |
| JPDB            | 25.2%   | 22.1%  | 14.7%  | 10.2%  | 4.6%    | 564 (2.3%) — excluded |

## Setup

### Requirements

- Python 3.10+
- For plotting scripts: `matplotlib`, `numpy`
- For RSPEER generation: `wordfreq`

### Install dependencies

```bash
pip install matplotlib numpy wordfreq
```

### Running scripts

Scripts under `data/ALL/___experiments0/` and `data/ALL/___experiments1/` can be run from the repo root. CEJC, RSPEER, and JPDB scripts must be run from their own directories.

The full pipeline has the following dependency order: RAW/\_\_\_FILTERED → CEJC + RSPEER preprocessing → data/ALL consolidation → analysis.

#### Step 1 — Generate standardized DATA.csv for each RAW source

Each source under `data/RAW/___FILTERED/` has a `SCRIPT.py` that reads the raw upstream file and outputs a normalized `DATA.csv` (columns: `WORD`, `FREQUENCY_RANKING`, top 25k entries). Run each from the repo root:

```bash
python data/RAW/___FILTERED/ADNO/SCRIPT.py
python data/RAW/___FILTERED/ANIME_JDRAMA/SCRIPT.py
python data/RAW/___FILTERED/AOZORA_BUNKO/SCRIPT.py
# ... repeat for all subdirectories under data/RAW/___FILTERED/
```

#### Step 2 — Preprocess CEJC, RSPEER, and JPDBV2

These outputs are consumed by the data/ALL consolidation scripts.

```bash
# CEJC: generate JSON and CSV breakdowns from the source TSV, then deduplicate
cd data/CEJC
python3 scripts/tsv_to_json.py 2_cejc_frequencylist_suw_token.tsv json 25000
python3 scripts/tsv_to_csv.py 2_cejc_frequencylist_suw_token.tsv csv 25000
python3 scripts/make_consolidated_unique.py   # reads CONSOLIDATED.csv → writes CONSOLIDATED_UNIQUE.csv

# RSPEER: generate top_25000_japanese.csv via the wordfreq library
cd data/RSPEER
python generate_top_japanese.py

# JPDBV2: generate task1_top25k.csv and task2_kana_higher.csv
cd data/JPDBV2
python process.py
```

#### Step 3 — Generate consolidated.csv and categorized.csv (experiments0)

Run from the repo root. Reads CEJC CONSOLIDATED_UNIQUE.csv, all DATA.csv files from RAW/\_\_\_FILTERED, and RSPEER top_25000_japanese.csv.

```bash
# Generate CEJC_anchor/consolidated.csv (CEJC as the anchor word list)
python data/ALL/___experiments0/data_generation/SCRIPT.py

# Generate CEJC_anchor/categorized.csv (vocab tier categories from consolidated.csv)
python data/ALL/___experiments0/data_generation/CATEGORIZED.py

# Generate consolidated.csv + categorized.csv for JPDB, YOUTUBE_FREQ_V3, ANIME_JDRAMA, NETFLIX anchors
python data/ALL/___experiments0/data_generation/make_anchored.py
```

#### Step 4 — Coverage and threshold analysis (experiments0)

```bash
# Run coverage analysis across all anchors
python data/ALL/___experiments0/coverage_analysis/analyze_coverage.py

# Quick CEJC-anchor word filter (negative ranks / rare categories)
python data/ALL/___experiments0/coverage_analysis/filter_words.py

# Threshold analysis across all anchors
python data/ALL/___experiments0/threshold_analysis/threshold_analysis.py
```

#### Step 5 — Add new anchors and re-run analysis (experiments1)

> Note: `make_more_anchors.py` must be run before the analysis scripts, and `generate_12k.py` must be run before the top12k analysis scripts.

```bash
# Regenerate all non-CEJC anchor consolidated.csv files (adds BCCWJ, CC100, RSPEER, WIKIPEDIA_V2)
python data/ALL/___experiments1/data_generation/make_more_anchors.py

# Coverage analysis across all anchors (updated EXCLUDE set: 10 sources)
python data/ALL/___experiments1/coverage_analysis/analyze_coverage.py

# Threshold analysis across all anchors
python data/ALL/___experiments1/coverage_analysis/threshold_analysis.py

# Slice all anchors to top 12k rows for equal-footing comparison
python data/ALL/___experiments1/top12k/generate_12k.py

# Coverage analysis on top-12k slices
python data/ALL/___experiments1/top12k/analyze_coverage.py

# Threshold analysis on top-12k slices
python data/ALL/___experiments1/top12k/threshold_analysis.py

# N≤3 missing sources by rank band summary table (prints markdown)
python data/ALL/___experiments1/top12k/n_leq3_by_rank_band.py

# Pairwise reading-aware overlap between all anchor datasets (top 5k/10k/15k/25k)
python data/ALL/___experiments1/anchor_pairwise_overlap.py
```

#### CEJC analysis reports

```bash
cd data/CEJC/scripts
python vocab_tier_breakdown.py ../json
python domain_profiles.py ../json
python demographic_analysis.py ../json
# ... (see data/CEJC/scripts/ for all scripts — all take ../json as the first argument)
```

#### RSPEER plots

```bash
cd data/RSPEER
python plot_coverage_curve.py
python plot_zipf_distribution.py
# ... (see data/RSPEER/ for all 6 plotting scripts)
```

## Notable Insights

### Coverage is concentrated (RSPEER)

80% of Japanese text is covered by just ~1,700 words; 90% by ~5,000; 95% by ~9,700; 98% by ~16,000. Focusing on the top 5,000 words gives strong practical coverage for everyday reading.

([Full coverage analysis](data/RSPEER/INSIGHTS.md))

### CEJC rankings are heavily tied at the bottom

Only 430 of 29,534 entries have a unique rank. Most entries share ranks due to tied low-frequency counts, creating a 19,985-rank gap. This is a known artifact of standard competition ranking (1224 style).

([Rank distribution analysis](data/CEJC/insights/rank_distribution.md))

### Cross-source agreement is only partial — and datasets index words differently

> See [Data Quality Notes](#data-quality-notes) for why JPDB scores far lower than every other source. Subtitle sources (ANIME, NETFLIX, YOUTUBE) also contain inflected verb forms and proper nouns not found as dictionary headwords (evidenced by their 6–11% kana gaps), but JPDB exhibits this most severely — inflected forms dominate its top ranks.

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

### Pairwise overlap across all anchors (experiments1)

> JPDB's uniformly low scores (~25–45%) are explained in [Data Quality Notes](#data-quality-notes). Subtitle sources also contain inflected forms and proper nouns, but JPDB is the most extreme case — inflected forms like `だった` and `だろう` rank in its top 50.

[`data/ALL/___experiments1/anchor_pairwise_overlap.py`](data/ALL/___experiments1/anchor_pairwise_overlap.py) — reading-aware pairwise intersection between all 9 anchor datasets. Row = source A (denominator); cell = % of A's top-N that appear in B's top-N. Top-15k is the most reliable tier for BCCWJ (only 16,491 words; its top-25k row is inflated).

**Top-5k:**

|                     | CC100 | CEJC  | YOUTUBE_FREQ_V3 | WIKIPEDIA_V2 | NETFLIX | BCCWJ | ANIME_JDRAMA | RSPEER | JPDB  |
| ------------------- | ----- | ----- | --------------- | ------------ | ------- | ----- | ------------ | ------ | ----- |
| **CC100**           | —     | 63.1% | 75.0%           | 58.3%        | 57.5%   | 73.2% | 54.5%        | 65.2%  | 32.5% |
| **CEJC**            | 61.4% | —     | 61.3%           | 47.9%        | 52.9%   | 60.2% | 51.0%        | 53.9%  | 34.6% |
| **YOUTUBE_FREQ_V3** | 77.0% | 65.0% | —               | 57.8%        | 62.5%   | 71.3% | 60.6%        | 67.3%  | 37.3% |
| **WIKIPEDIA_V2**    | 62.8% | 53.1% | 60.3%           | —            | 54.6%   | 61.6% | 52.8%        | 65.4%  | 26.7% |
| **NETFLIX**         | 61.7% | 58.8% | 64.8%           | 54.6%        | —       | 63.8% | 79.9%        | 64.4%  | 41.8% |
| **BCCWJ**           | 71.9% | 60.7% | 67.9%           | 56.7%        | 58.5%   | —     | 55.7%        | 60.6%  | 29.7% |
| **ANIME_JDRAMA**    | 58.4% | 56.8% | 62.5%           | 51.8%        | 79.9%   | 61.2% | —            | 60.7%  | 42.0% |
| **RSPEER**          | 67.9% | 58.1% | 68.4%           | 63.6%        | 63.3%   | 64.4% | 60.0%        | —      | 33.3% |
| **JPDB**            | 26.9% | 30.2% | 29.6%           | 19.5%        | 32.3%   | 25.3% | 32.1%        | 26.1%  | —     |

**Top-10k:**

|                     | CC100 | CEJC  | YOUTUBE_FREQ_V3 | WIKIPEDIA_V2 | NETFLIX | BCCWJ | ANIME_JDRAMA | RSPEER | JPDB  |
| ------------------- | ----- | ----- | --------------- | ------------ | ------- | ----- | ------------ | ------ | ----- |
| **CC100**           | —     | 61.4% | 74.8%           | 60.2%        | 59.6%   | 73.8% | 55.1%        | 65.7%  | 35.5% |
| **CEJC**            | 58.9% | —     | 57.2%           | 47.8%        | 49.4%   | 56.9% | 48.0%        | 51.8%  | 35.4% |
| **YOUTUBE_FREQ_V3** | 76.4% | 61.7% | —               | 60.9%        | 63.2%   | 70.0% | 60.1%        | 67.7%  | 40.4% |
| **WIKIPEDIA_V2**    | 65.1% | 54.3% | 64.1%           | —            | 61.1%   | 63.9% | 59.0%        | 70.0%  | 32.9% |
| **NETFLIX**         | 63.0% | 55.3% | 64.9%           | 60.1%        | —       | 63.1% | 79.4%        | 66.1%  | 44.4% |
| **BCCWJ**           | 72.2% | 58.0% | 66.7%           | 58.2%        | 58.1%   | —     | 54.7%        | 60.5%  | 32.2% |
| **ANIME_JDRAMA**    | 58.6% | 53.8% | 61.9%           | 57.8%        | 79.6%   | 60.0% | —            | 62.2%  | 44.2% |
| **RSPEER**          | 67.8% | 56.8% | 68.7%           | 67.5%        | 65.5%   | 64.1% | 61.7%        | —      | 37.1% |
| **JPDB**            | 29.3% | 30.8% | 32.0%           | 24.1%        | 34.0%   | 27.2% | 33.2%        | 28.9%  | —     |

**Top-15k:**

|                     | CC100 | CEJC  | YOUTUBE_FREQ_V3 | WIKIPEDIA_V2 | NETFLIX | BCCWJ | ANIME_JDRAMA | RSPEER | JPDB  |
| ------------------- | ----- | ----- | --------------- | ------------ | ------- | ----- | ------------ | ------ | ----- |
| **CC100**           | —     | 61.0% | 75.0%           | 60.3%        | 61.5%   | 72.9% | 56.7%        | 65.4%  | 36.9% |
| **CEJC**            | 57.7% | —     | 55.5%           | 47.6%        | 48.8%   | 55.8% | 46.9%        | 50.6%  | 35.7% |
| **YOUTUBE_FREQ_V3** | 76.4% | 60.7% | —               | 61.5%        | 64.3%   | 68.3% | 60.9%        | 67.4%  | 41.6% |
| **WIKIPEDIA_V2**    | 65.0% | 54.7% | 64.5%           | —            | 64.0%   | 63.6% | 61.4%        | 71.1%  | 35.3% |
| **NETFLIX**         | 64.1% | 54.6% | 65.3%           | 62.4%        | —       | 63.0% | 78.8%        | 66.8%  | 45.5% |
| **BCCWJ**           | 70.5% | 57.2% | 64.5%           | 57.4%        | 58.0%   | —     | 54.3%        | 59.1%  | 32.5% |
| **ANIME_JDRAMA**    | 59.6% | 52.9% | 62.1%           | 59.7%        | 79.2%   | 59.5% | —            | 62.2%  | 44.4% |
| **RSPEER**          | 67.3% | 56.1% | 68.3%           | 68.7%        | 66.6%   | 63.2% | 62.1%        | —      | 38.8% |
| **JPDB**            | 30.5% | 31.3% | 32.7%           | 26.3%        | 35.1%   | 27.8% | 33.4%        | 29.9%  | —     |

**Top-25k** (BCCWJ capped at 16,491 — row inflated):

|                     | CC100 | CEJC  | YOUTUBE_FREQ_V3 | WIKIPEDIA_V2 | NETFLIX | BCCWJ | ANIME_JDRAMA | RSPEER | JPDB  |
| ------------------- | ----- | ----- | --------------- | ------------ | ------- | ----- | ------------ | ------ | ----- |
| **CC100**           | —     | 61.6% | 75.8%           | 61.7%        | 64.6%   | 57.2% | 60.6%        | 65.9%  | 39.8% |
| **CEJC**            | 57.6% | —     | 54.5%           | 48.2%        | 49.1%   | 45.2% | 48.0%        | 50.3%  | 36.0% |
| **YOUTUBE_FREQ_V3** | 75.9% | 59.1% | —               | 61.9%        | 65.7%   | 55.5% | 63.1%        | 67.2%  | 43.2% |
| **WIKIPEDIA_V2**    | 65.0% | 54.7% | 64.8%           | —            | 65.9%   | 52.6% | 64.3%        | 72.4%  | 37.7% |
| **NETFLIX**         | 65.5% | 53.9% | 66.0%           | 63.9%        | —       | 52.2% | 79.6%        | 66.7%  | 45.9% |
| **BCCWJ**           | 76.7% | 65.3% | 73.4%           | 66.1%        | 68.1%   | —     | 65.3%        | 67.6%  | 38.8% |
| **ANIME_JDRAMA**    | 61.4% | 52.5% | 63.1%           | 62.0%        | 79.5%   | 50.1% | —            | 63.1%  | 44.6% |
| **RSPEER**          | 66.1% | 54.5% | 67.2%           | 69.7%        | 66.5%   | 51.3% | 63.2%        | —      | 39.5% |
| **JPDB**            | 33.5% | 32.6% | 35.0%           | 29.6%        | 36.8%   | 22.9% | 35.0%        | 31.8%  | —     |

**Key observations:**

- **NETFLIX ↔ ANIME_JDRAMA** is the highest-overlap pair (~79–80% both directions at all tiers) — both are subtitle corpora covering similar spoken registers
- **JPDB rows score 25–45%** across all partners at all tiers, far below every other anchor, because it uses a different vocabulary model (surface forms vs lemmas)
- **YOUTUBE_FREQ_V3 and CC100** show strong mutual coverage (~75–77% / ~66–76%), both capturing broad everyday language across many domains
- **WIKIPEDIA_V2 ↔ RSPEER** is notably high (~70–72% at top-10k and above), consistent with both drawing from written, encyclopedic text
- **CEJC rows are consistently the lowest** among general-purpose anchors (~55–65%), reflecting spoken-only UniDic lemma forms (e.g. 其れ, 為る) that diverge from the surface forms used by written and subtitle sources
- **The matrix is asymmetric**: BCCWJ → CC100 is 72% but CC100 → BCCWJ is 74% at top-10k. A → B and B → A check different lookup sets: A → B tests each of A's top-N words against B's surface forms ∪ B's readings, while B → A tests against A's surface forms ∪ A's readings. Because each anchor has a different vocabulary and different reading coverage gaps (hiragana = `-` for some words), these sets differ in size and content — producing asymmetric percentages. The subtitle pair (ANIME_JDRAMA ↔ NETFLIX) is nearly symmetric because both sources have similar vocabulary and reading coverage, so their lookup sets are nearly the same size.

## License

MIT License — Copyright 2026 PikaPikaGems. Individual datasets retain their original licenses and attributions as documented in each source's README.
