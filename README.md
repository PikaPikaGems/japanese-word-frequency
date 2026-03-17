> **Use at your own risk.** The code and logic for generating this data have not been fully reviewed. Data quality, coverage, and methodology vary across sources. No guarantees are made about accuracy, completeness, or fitness for any particular purpose.

# Japanese Word Frequency Rankings

A comprehensive collection of Japanese word frequency datasets, analysis scripts, and insights, consolidating datasets into unified formats for language learning, linguistics, and NLP research.

## Notes

- [CONSOLIDATED_CSV_REFERENCEV1.md](CONSOLIDATED_CSV_REFERENCEV1.md) — How to read `consolidated.csv` (Aggregated Frequency Word Rankings): column layout, practical interpretation guide, and per-source caveats
- [notes/cleaned-datasets-reference-v1.md](notes/cleaned-datasets-reference-v1.md) — Detailed descriptions of some frequency rank datasets included in the database, with source notes on corpus size, register, and tokenization
- [notes/consolidated-reference-verbose.md](notes/consolidated-reference-verbose.md) — Detailed descriptions of some frequency sources
- [notes/consolidated-reference-short.md](notes/consolidated-reference-short.md) — Bullet point information of some frequency sources

- [data/ALL/___experiments2/PAIRWISE_OVERLAPS.md](data/ALL/___experiments2/PAIRWISE_OVERLAPS.md) — Pairwise reading-aware overlap tables for thematically grouped source datasets (Japanese web, Wikipedia, YouTube, Netflix/drama, slice-of-life, anime) at Top-2k, 5k, and 10k

### Main Data Sources

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
- https://docs.google.com/document/d/1IUWkvBxhoazBSTyRbdyRVk7hfKE51yorE86DCRNQVuw/
- https://jiten.moe/other

## Repository Structure

```
word-frequency-rankings/
├── data/
│   ├── ALL/          # Consolidated multi-source rankings (27,988 words × 70+ rank columns)
│   ├── CEJC/         # Corpus of Everyday Japanese Conversation (~2.4M words, 577 conversations)
│   ├── JPDBV2/       # JPDB v2.2 entertainment media frequency list (~497k entries)
│   ├── RSPEER/       # rspeer/wordfreq library output (top 25,000 words)
│   └── RAW/
│       └── ___FILTERED/   # All datasets, each with a standardized DATA.csv
├── notes/            # Reference documentation for all frequency sources
└── utils/            # Shared Python utilities (formatting, kana conversion, JP word lookup)
```

## Datasets

### ALL — Consolidated Rankings

`data/ALL/`

The primary output of this repo. Each `consolidated.csv` is a matrix of **words × rank columns**, one column per frequency source. The **anchor** is the source whose word list defines the rows — every word in the anchor appears as a row, and each column shows that word's rank in the other sources (`-1` if absent). Different anchors produce different matrices because each source has different vocabulary coverage and tokenization. Ten anchor variants exist: CEJC, BCCWJ_LUW, BCCWJ_SUW, CC100, RSPEER, WIKIPEDIA_V2, ANIME_JDRAMA, NETFLIX, YOUTUBE_FREQ_V3, and JPDB. Analysis scripts and reports in `___experiments0/` and `___experiments1/`:
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

### RAW/\_\_\_FILTERED — 60+ Source Datasets + RSPEER

`data/RAW/___FILTERED/`

Each subdirectory contains a standardized `DATA.csv` (columns: `WORD`, `FREQUENCY_RANKING`, top 25k entries) and a `README.md` describing the source. `RSPEER` (`data/RSPEER/top_25000_japanese.csv`) is included as an additional source; its rank is derived from row position (row 1 = rank 1, sorted by descending zipf frequency).

| Source                     | Type                                                |
| -------------------------- | --------------------------------------------------- |
| ADNO                       | Wikipedia (cleaned)                                 |
| ANIME_JDRAMA               | Anime & J-drama subtitles                           |
| AOZORA_BUNKO               | Public domain literature                            |
| BCCWJ_LUW                  | Balanced written corpus — Long Unit Word (NINJAL)   |
| BCCWJ_SUW                  | Balanced written corpus — Short Unit Word (NINJAL)  |
| CC100                      | Web text (Common Crawl)                             |
| CHRISKEMPSON               | Japanese subtitles                                  |
| DAVE_DOEBRICK              | Netflix subtitles (Dave Doebrick, full report)      |
| DD2_MIGAKU_NETFLIX         | Netflix subtitles (Migaku dictionary format)        |
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
| JITEN_ANIME                | Anime-focused frequency (jiten.moe, Yomitan JSON)   |
| JITEN_ANIME_V2             | Anime-focused frequency (jiten.moe, CSV format)     |
| JITEN_AUDIO                | Audio media frequency (jiten.moe)                   |
| JITEN_DRAMA                | Japanese drama frequency (jiten.moe)                |
| JITEN_GLOBAL               | All-media combined frequency (jiten.moe)            |
| JITEN_MANGA                | Manga frequency (jiten.moe)                         |
| JITEN_MOVIE                | Movie frequency (jiten.moe)                         |
| JITEN_NON_FICTION          | Non-fiction media frequency (jiten.moe)             |
| JITEN_NOVEL                | Novel frequency (jiten.moe)                         |
| JITEN_VIDEO_GAME           | Video game frequency (jiten.moe)                    |
| JITEN_VISUAL_NOVEL         | Visual novel frequency (jiten.moe)                  |
| JITEN_WEB_NOVEL            | Web novel frequency (jiten.moe)                     |
| JLAB                       | Anime frequency (Japanese Like a Breeze)            |
| JPDB                       | Entertainment media (jpdb.io)                       |
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

## Setup

### Requirements

- Python 3.10+
- For plotting scripts: `matplotlib`, `numpy`
- For RSPEER generation: `wordfreq`

### Install dependencies

```bash
# To get RSPeer dataset
pip install wordfreq
# For generating graphs and insights
pip install matplotlib numpy
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

#### Step 3 — Generate consolidated.csv and categorized.csv

Run from the repo root. Reads CEJC `CONSOLIDATED_UNIQUE.csv`, all `DATA.csv` files from `RAW/___FILTERED`, and RSPEER `top_25000_japanese.csv`.

```bash
# Check for duplicate rank columns across all consolidated.csv files
python data/ALL/___data_generation/check_duplicate_rank_columns.py

# Generate CEJC_anchor/consolidated.csv (CEJC as the anchor word list)
python data/ALL/___data_generation/SCRIPT.py

# Generate CEJC_anchor/categorized.csv (vocab tier categories from consolidated.csv)
python data/ALL/___data_generation/CATEGORIZED.py

# Generate consolidated.csv + categorized.csv for all non-CEJC anchors
python data/ALL/___data_generation/make_more_anchors.py
```

#### Step 4 — Analysis Reports (optional)

Coverage and threshold analysis

> These steps reproduce the analysis in `___experiments0/` and `___experiments1/`. They are not required when adding new frequency sources — only re-run if you want updated coverage statistics or reports.

```bash
# experiments0: coverage and threshold analysis
python data/ALL/___experiments0/coverage_analysis/analyze_coverage.py
python data/ALL/___experiments0/coverage_analysis/filter_words.py
python data/ALL/___experiments0/threshold_analysis/threshold_analysis.py

# experiments1: coverage, threshold, top-12k analysis
python data/ALL/___experiments1/coverage_analysis/analyze_coverage.py
python data/ALL/___experiments1/coverage_analysis/threshold_analysis.py
python data/ALL/___experiments1/top12k/generate_12k.py
python data/ALL/___experiments1/top12k/analyze_coverage.py
python data/ALL/___experiments1/top12k/threshold_analysis.py
python data/ALL/___experiments1/top12k/n_leq3_by_rank_band.py
python data/ALL/___experiments1/anchor_pairwise_overlap.py
```

CEJC analysis reports (optional)

```bash
cd data/CEJC/scripts
python vocab_tier_breakdown.py ../json
python domain_profiles.py ../json
python demographic_analysis.py ../json
# ... (see data/CEJC/scripts/ for all scripts — all take ../json as the first argument)
```

#### RSPEER plots (optional)

```bash
cd data/RSPEER
python plot_coverage_curve.py
python plot_zipf_distribution.py
# ... (see data/RSPEER/ for all 6 plotting scripts)
```

## Data Quality Notes (Last Run March 18, 2026)

### Inspecting the JPDB dataset

- **Surface forms, not lemmas.** JPDB records exactly what was written in the source texts. Inflected and compound forms appear as separate top-ranked entries: `だった` (rank 24), `には` (rank 26), `だろう` (rank 37), `けど` (rank 38), `だから` (rank 43), `ではない` (rank 89), `ことになる` (rank 167). Every other source (CEJC, RSPEER, BCCWJ_LUW, etc.) lemmatizes these to their base forms (`だ`, `けれど`, etc.), so the same underlying word occupies a completely different slot in JPDB's list.

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

[`data/ALL/___experiments1/HISTORY.md`](data/ALL/___experiments1/HISTORY.md) documents findings from re-running coverage experiments after the dataset grew from ~35 to 60 external sources and 4 new anchors were added.

**New anchors added (10 total):**

| Anchor       | Type                                     | Words  |
| ------------ | ---------------------------------------- | ------ |
| BCCWJ_LUW    | Balanced written Japanese — LUW (NINJAL) | 25,000 |
| BCCWJ_SUW    | Balanced written Japanese — SUW (NINJAL) | 25,000 |
| CC100        | CommonCrawl web text                     | 24,605 |
| RSPEER       | Multi-source aggregated (wordfreq)       | 25,000 |
| WIKIPEDIA_V2 | Wikipedia (clean)                        | 25,000 |

**Updated EXCLUDE set (10 sources):** H_FREQ, NAROU, and VN_FREQ added to the original 7 — all use UniDic kanji lemma forms or domain-skewed tokenization that causes basic particles to score as absent.

**How to read these tables:**

- **Top-N %** (zero-missing): of the first N words in the anchor's frequency list, the percentage that appear in _every_ checked source (no `-1` rank). A high Top-500 means the most common words are universally found everywhere. The percentage naturally falls as N grows because rarer words start appearing in fewer domain-specific corpora.
- **N≤3**: words missing from _at most 3_ of the ~61 checked sources — the "broadly common" core vocabulary present in nearly all corpora.

**Zero-missing by rank band** ([`top12k/`](data/ALL/___experiments1/top12k/HISTORY.md)):

| Anchor          | Top-500 | Top-1k | Top-3k | Top-5k | Top-12k |
| --------------- | ------- | ------ | ------ | ------ | ------- |
| CC100           | 76.4%   | 65.9%  | 46.6%  | 35.2%  | 17.8%   |
| CEJC            | 76.0%   | 66.7%  | 44.1%  | 32.6%  | 16.9%   |
| BCCWJ_SUW       | 73.0%   | 67.3%  | 51.1%  | 38.1%  | 18.1%   |
| BCCWJ_LUW       | 73.4%   | 67.8%  | 47.1%  | 34.6%  | 17.2%   |
| YOUTUBE_FREQ_V3 | 60.8%   | 56.0%  | 42.3%  | 33.3%  | 17.3%   |
| NETFLIX         | 63.6%   | 58.1%  | 43.0%  | 32.9%  | 17.2%   |
| WIKIPEDIA_V2    | 51.4%   | 47.3%  | 33.9%  | 27.0%  | 15.9%   |
| ANIME_JDRAMA    | 54.2%   | 52.5%  | 40.6%  | 31.4%  | 16.9%   |
| RSPEER          | 52.4%   | 49.5%  | 38.1%  | 30.2%  | 17.1%   |
| JPDB            | 17.8%   | 11.1%  | 4.5%   | 3.0%   | 1.3%    |

**N≤3 missing sources by rank band** (top-12k slices, [`n_leq3_by_rank_band.py`](data/ALL/___experiments1/top12k/n_leq3_by_rank_band.py)):

| Anchor          | Top-500 | Top-1k | Top-3k | Top-5k | Top-12k | N≤3 @25k     |
| --------------- | ------- | ------ | ------ | ------ | ------- | ------------ |
| CEJC            | 92.2%   | 88.7%  | 72.5%  | 59.3%  | 36.4%   | —            |
| CC100           | 92.2%   | 87.0%  | 74.2%  | 63.9%  | 40.8%   | —            |
| BCCWJ_SUW       | 92.2%   | 90.6%  | 82.2%  | 72.8%  | 42.9%   | —            |
| WIKIPEDIA_V2    | 79.8%   | 75.9%  | 60.2%  | 51.1%  | 33.4%   | —            |
| BCCWJ_LUW       | 83.6%   | 81.1%  | 70.7%  | 62.2%  | 38.2%   | —            |
| YOUTUBE_FREQ_V3 | 70.8%   | 72.1%  | 65.4%  | 58.2%  | 38.0%   | —            |
| NETFLIX         | 70.8%   | 69.5%  | 61.6%  | 54.7%  | 37.1%   | —            |
| RSPEER          | 63.4%   | 64.5%  | 60.6%  | 54.2%  | 36.3%   | —            |
| ANIME_JDRAMA    | 62.2%   | 63.2%  | 58.0%  | 50.9%  | 35.2%   | —            |
| JPDB            | 25.8%   | 21.6%  | 11.9%  | 7.6%   | 3.3%    | — (excluded) |

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

[`data/ALL/___experiments1/anchor_pairwise_overlap.py`](data/ALL/___experiments1/anchor_pairwise_overlap.py) — reading-aware pairwise intersection between all 10 anchor datasets. Row = source A (denominator); cell = % of A's top-N that appear in B's top-N.

**Top-5k:**

|                     | CC100 | CEJC  | YOUTUBE_FREQ_V3 | WIKIPEDIA_V2 | NETFLIX | BCCWJ_LUW | BCCWJ_SUW | ANIME_JDRAMA | RSPEER | JPDB  |
| ------------------- | ----- | ----- | --------------- | ------------ | ------- | --------- | --------- | ------------ | ------ | ----- |
| **CC100**           | —     | 63.1% | 75.0%           | 58.3%        | 57.5%   | 68.1%     | 77.3%     | 54.5%        | 65.2%  | 32.5% |
| **CEJC**            | 61.4% | —     | 61.3%           | 47.9%        | 52.9%   | 55.9%     | 66.2%     | 51.0%        | 53.9%  | 34.6% |
| **YOUTUBE_FREQ_V3** | 77.0% | 65.0% | —               | 57.8%        | 62.6%   | 67.9%     | 73.0%     | 60.6%        | 67.3%  | 37.3% |
| **WIKIPEDIA_V2**    | 62.8% | 53.1% | 60.3%           | —            | 54.6%   | 54.4%     | 66.0%     | 52.8%        | 65.4%  | 26.7% |
| **NETFLIX**         | 61.7% | 58.8% | 64.8%           | 54.6%        | —       | 62.6%     | 64.4%     | 79.9%        | 64.4%  | 41.8% |
| **BCCWJ_LUW**       | 64.6% | 54.2% | 62.2%           | 47.9%        | 55.2%   | —         | 70.6%     | 53.0%        | 52.8%  | 29.8% |
| **BCCWJ_SUW**       | 77.9% | 68.0% | 71.2%           | 62.6%        | 60.4%   | 74.4%     | —         | 56.8%        | 64.4%  | 31.4% |
| **ANIME_JDRAMA**    | 58.4% | 56.8% | 62.5%           | 51.8%        | 79.9%   | 60.4%     | 60.8%     | —            | 60.7%  | 42.0% |
| **RSPEER**          | 67.9% | 58.1% | 68.4%           | 63.6%        | 63.3%   | 58.7%     | 66.7%     | 60.0%        | —      | 33.3% |
| **JPDB**            | 26.9% | 30.2% | 29.6%           | 19.5%        | 32.3%   | 26.6%     | 26.3%     | 32.1%        | 26.1%  | —     |

**Top-10k:**

|                     | CC100 | CEJC  | YOUTUBE_FREQ_V3 | WIKIPEDIA_V2 | NETFLIX | BCCWJ_LUW | BCCWJ_SUW | ANIME_JDRAMA | RSPEER | JPDB  |
| ------------------- | ----- | ----- | --------------- | ------------ | ------- | --------- | --------- | ------------ | ------ | ----- |
| **CC100**           | —     | 61.4% | 74.8%           | 60.2%        | 59.6%   | 68.5%     | 75.9%     | 55.1%        | 65.7%  | 35.5% |
| **CEJC**            | 58.9% | —     | 57.2%           | 47.8%        | 49.4%   | 51.7%     | 63.2%     | 48.0%        | 51.8%  | 35.4% |
| **YOUTUBE_FREQ_V3** | 76.4% | 61.7% | —               | 61.0%        | 63.2%   | 65.5%     | 70.3%     | 60.1%        | 67.7%  | 40.4% |
| **WIKIPEDIA_V2**    | 65.1% | 54.3% | 64.2%           | —            | 61.1%   | 56.5%     | 67.9%     | 59.0%        | 70.0%  | 32.9% |
| **NETFLIX**         | 63.0% | 55.3% | 64.9%           | 60.1%        | —       | 61.5%     | 63.5%     | 79.4%        | 66.1%  | 44.4% |
| **BCCWJ_LUW**       | 64.3% | 50.3% | 59.8%           | 48.6%        | 54.1%   | —         | 67.4%     | 51.3%        | 51.8%  | 31.1% |
| **BCCWJ_SUW**       | 76.7% | 66.2% | 69.1%           | 64.1%        | 60.4%   | 72.1%     | —         | 56.5%        | 64.5%  | 34.7% |
| **ANIME_JDRAMA**    | 58.6% | 53.8% | 61.9%           | 57.8%        | 79.6%   | 58.9%     | 59.8%     | —            | 62.2%  | 44.2% |
| **RSPEER**          | 67.8% | 56.8% | 68.7%           | 67.5%        | 65.5%   | 58.1%     | 66.2%     | 61.7%        | —      | 37.1% |
| **JPDB**            | 29.3% | 30.8% | 32.0%           | 24.1%        | 34.0%   | 27.4%     | 29.0%     | 33.2%        | 28.9%  | —     |

**Top-15k:**

|                     | CC100 | CEJC  | YOUTUBE_FREQ_V3 | WIKIPEDIA_V2 | NETFLIX | BCCWJ_LUW | BCCWJ_SUW | ANIME_JDRAMA | RSPEER | JPDB  |
| ------------------- | ----- | ----- | --------------- | ------------ | ------- | --------- | --------- | ------------ | ------ | ----- |
| **CC100**           | —     | 61.0% | 75.0%           | 60.3%        | 61.5%   | 69.1%     | 74.7%     | 56.7%        | 65.4%  | 36.9% |
| **CEJC**            | 57.7% | —     | 55.5%           | 47.6%        | 48.8%   | 49.7%     | 63.3%     | 46.9%        | 50.6%  | 35.7% |
| **YOUTUBE_FREQ_V3** | 76.4% | 60.7% | —               | 61.5%        | 64.3%   | 65.1%     | 68.8%     | 60.9%        | 67.4%  | 41.6% |
| **WIKIPEDIA_V2**    | 65.0% | 54.7% | 64.5%           | —            | 64.0%   | 57.2%     | 67.4%     | 61.4%        | 71.1%  | 35.3% |
| **NETFLIX**         | 64.1% | 54.6% | 65.3%           | 62.4%        | —       | 61.4%     | 63.6%     | 78.8%        | 66.8%  | 45.5% |
| **BCCWJ_LUW**       | 64.1% | 48.5% | 58.6%           | 48.6%        | 53.9%   | —         | 65.7%     | 50.9%        | 51.2%  | 30.9% |
| **BCCWJ_SUW**       | 75.2% | 66.9% | 67.5%           | 63.8%        | 61.2%   | 71.0%     | —         | 56.7%        | 63.9%  | 36.6% |
| **ANIME_JDRAMA**    | 59.6% | 52.9% | 62.1%           | 59.7%        | 79.2%   | 58.7%     | 59.4%     | —            | 62.2%  | 44.4% |
| **RSPEER**          | 67.3% | 56.1% | 68.3%           | 68.7%        | 66.6%   | 57.9%     | 65.5%     | 62.1%        | —      | 38.8% |
| **JPDB**            | 30.5% | 31.3% | 32.7%           | 26.3%        | 35.1%   | 27.3%     | 30.9%     | 33.4%        | 29.9%  | —     |

**Top-25k:**

|                     | CC100 | CEJC  | YOUTUBE_FREQ_V3 | WIKIPEDIA_V2 | NETFLIX | BCCWJ_LUW | BCCWJ_SUW | ANIME_JDRAMA | RSPEER | JPDB  |
| ------------------- | ----- | ----- | --------------- | ------------ | ------- | --------- | --------- | ------------ | ------ | ----- |
| **CC100**           | —     | 61.6% | 75.8%           | 61.7%        | 64.6%   | 69.0%     | 73.8%     | 60.6%        | 65.9%  | 39.8% |
| **CEJC**            | 57.6% | —     | 54.5%           | 48.2%        | 49.1%   | 49.0%     | 64.5%     | 48.0%        | 50.3%  | 36.0% |
| **YOUTUBE_FREQ_V3** | 75.9% | 59.1% | —               | 61.9%        | 65.7%   | 64.2%     | 66.7%     | 63.1%        | 67.2%  | 43.2% |
| **WIKIPEDIA_V2**    | 65.0% | 54.7% | 64.8%           | —            | 65.9%   | 57.9%     | 66.3%     | 64.3%        | 72.4%  | 37.7% |
| **NETFLIX**         | 65.5% | 53.9% | 66.0%           | 63.9%        | —       | 61.9%     | 62.8%     | 79.6%        | 66.7%  | 45.9% |
| **BCCWJ_LUW**       | 62.3% | 46.8% | 57.2%           | 48.9%        | 54.5%   | —         | 61.9%     | 52.0%        | 50.4%  | 31.5% |
| **BCCWJ_SUW**       | 73.2% | 67.9% | 65.5%           | 63.0%        | 61.1%   | 67.7%     | —         | 57.8%        | 62.8%  | 39.5% |
| **ANIME_JDRAMA**    | 61.4% | 52.5% | 63.1%           | 62.0%        | 79.5%   | 59.3%     | 59.4%     | —            | 63.1%  | 44.6% |
| **RSPEER**          | 66.1% | 54.5% | 67.2%           | 69.7%        | 66.5%   | 57.1%     | 63.5%     | 63.2%        | —      | 39.5% |
| **JPDB**            | 33.5% | 32.6% | 35.0%           | 29.6%        | 36.8%   | 28.9%     | 35.1%     | 35.0%        | 31.8%  | —     |

**Key observations:**

- **NETFLIX ↔ ANIME_JDRAMA** is the highest-overlap pair (~79–80% both directions at all tiers) — both are subtitle corpora covering similar spoken registers
- **JPDB rows score 25–45%** across all partners at all tiers, far below every other anchor, because it uses a different vocabulary model (surface forms vs lemmas)
- **YOUTUBE_FREQ_V3 and CC100** show strong mutual coverage (~75–77% / ~66–76%), both capturing broad everyday language across many domains
- **WIKIPEDIA_V2 ↔ RSPEER** is notably high (~70–72% at top-10k and above), consistent with both drawing from written, encyclopedic text
- **CEJC rows are consistently the lowest** among general-purpose anchors (~55–65%), reflecting spoken-only UniDic lemma forms (e.g. 其れ, 為る) that diverge from the surface forms used by written and subtitle sources
- **BCCWJ_SUW scores significantly higher than BCCWJ_LUW** across most partners (~73–78% vs ~62–65% at top-5k) because SUW's fine morphological segmentation produces more particles and grammatical morphemes that appear universally across all corpora; LUW's compound units are more content-word-specific and miss more domain-specific sources
- **The matrix is asymmetric**: BCCWJ_SUW → CC100 is 78% but CC100 → BCCWJ_SUW is 77% at top-5k; ANIME_JDRAMA → NETFLIX is ~79% but NETFLIX → ANIME_JDRAMA is also ~79% — the subtitle pair happens to be nearly symmetric, while written ↔ spoken pairs diverge more

## License

MIT License — Copyright 2026 PikaPikaGems. Individual datasets retain their original licenses and attributions as documented in each source's README.
