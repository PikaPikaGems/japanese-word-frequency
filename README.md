> **Work in progress — use at your own risk.** The code and logic for generating this data have not been fully reviewed. Data quality, coverage, and methodology vary across sources. No guarantees are made about accuracy, completeness, or fitness for any particular purpose.

# Japanese Word Frequency Rankings

A comprehensive collection of Japanese word frequency datasets, analysis scripts, and insights, consolidating 35+ sources into unified formats for language learning, linguistics, and NLP research.

## Vocabulary Tier System

Words are assigned to one of five frequency tiers based on their ranking across sources:

| Tier            | Range          | Description                                       |
| --------------- | -------------- | ------------------------------------------------- |
| 🌱 **basic**    | Top ~1,000     | Foundational and essential vocabulary             |
| ☘️ **common**   | ~1,001–4,000   | Frequent in everyday speech and writing           |
| 🌷 **fluent**   | ~4,001–10,000  | Expansive vocabulary for natural expression       |
| 📚 **advanced** | ~10,001–25,000 | Formal, academic, technical, or specialized terms |
| 🦉 **rare**     | 25,000+        | Archaic, obscure, uncommon, or invalid terms      |

## Repository Structure

```
word-frequency-rankings/
├── data/
│   ├── ALL/          # Consolidated multi-source rankings (27,988 words x 49 sources)
│   ├── CEJC/         # Corpus of Everyday Japanese Conversation (~2.4M words, 577 conversations)
│   ├── JPDBV2/       # JPDB v2.2 entertainment media frequency list (~497k entries)
│   ├── RSPEER/       # rspeer/wordfreq library output (top 25,000 words)
│   └── RAW/
│       └── ___FILTERED/   # 35 standardized source datasets (DATA.csv per source)
├── notes/            # Reference documentation for all 22+ frequency sources
└── utils/            # Shared Python utilities (formatting helpers)
```

## Datasets

### ALL — Consolidated Rankings

`data/ALL/`

The primary output of this repo. Combines CEJC rankings with all 35 filtered sources into a single file.

- **`consolidated.csv`** — 27,988 unique words x 49 rank columns (14 CEJC + 35 source)
- **`categorized.csv`** — Same structure, with ranks mapped to tier labels (basic/common/fluent/advanced/rare)
- **`SCRIPT.py`** — Generates `consolidated.csv` from CEJC + filtered sources
- **`CATEGORIZED.py`** — Generates `categorized.csv` from `consolidated.csv`
- **`check_duplicates.py`** — Detects and removes source columns with identical rankings
- 5 insight reports in `insights/`
- 5 analysis scripts in `scripts/`

### CEJC — Everyday Spoken Japanese

`data/CEJC/`

Based on 200 hours of recorded spontaneous speech. Rich demographic breakdown by conversation domain, gender, and age group.

- **`CONSOLIDATED.csv`** — 29,534 entries x 36 rank columns (domain + demographic breakdowns)
- **`CONSOLIDATED_UNIQUE.csv`** — 27,988 deduplicated entries
- 8 insight reports in `insights/`
- 13 analysis scripts in `scripts/`

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

### RAW/\_\_\_FILTERED — 35 Source Datasets

`data/RAW/___FILTERED/`

Each subdirectory contains a standardized `DATA.csv` (columns: `WORD`, `FREQUENCY_RANKING`, top 25k entries) and a `README.md` describing the source.

| Source                    | Type                                               |
| ------------------------- | -------------------------------------------------- |
| ADNO                      | Wikipedia (cleaned)                                |
| ANIME_JDRAMA              | Anime & J-drama subtitles                          |
| AOZORA_BUNKO              | Public domain literature                           |
| BCCWJ                     | Balanced written corpus (NINJAL, 100M words)       |
| CC100                     | Web text (Common Crawl)                            |
| CHRISKEMPSON              | Japanese subtitles                                 |
| DAVE_DOEBRICK             | Netflix subtitles (Dave Doebrick, full report)     |
| DD2_MIGAKU_NETFLIX        | Netflix subtitles (Migaku dictionary format)       |
| DD2_MIGAKU_NOVELS         | Novel corpus (Migaku dictionary format)            |
| DD2_MORPHMAN_NETFLIX      | Netflix subtitles (Morphman report, no names)      |
| DD2_MORPHMAN_NOVELS       | Novel corpus (Morphman report)                     |
| DD2_MORPHMAN_SHONEN       | Shonen anime/manga (Morphman report)               |
| DD2_MORPHMAN_SOL          | Slice of Life anime (Morphman report)              |
| DD2_YOMICHAN_NOVELS       | Novel corpus (Yomichan Stars format)               |
| DD2_YOMICHAN_SHONEN       | Shonen anime/manga (Yomichan integer rank format)  |
| DD2_YOMICHAN_SHONEN_STARS | Shonen anime/manga (Yomichan Stars format)         |
| DD2_YOMICHAN_SOL          | Slice of Life anime (Yomichan integer rank format) |
| DD2_YOMICHAN_VN           | Visual novels (Yomichan Stars format)              |
| HERMITDAVE_2016           | Subtitle corpus (2016)                             |
| HERMITDAVE_2018           | Subtitle corpus (2018)                             |
| H_FREQ                    | Community-compiled list                            |
| ILYASEMENOV               | Wikipedia word frequency                           |
| INNOCENT_RANKED           | Innocent Corpus (novels)                           |
| JITEN_ANIME               | Anime-focused frequency                            |
| JPDB                      | Entertainment media (jpdb.io)                      |
| KOKUGOJITEN               | Japanese dictionary headwords                      |
| MONODICTS                 | Monolingual dictionary terms                       |
| NAROU                     | Web novels (Narou)                                 |
| NETFLIX                   | Netflix subtitle frequency                         |
| NIER                      | NieR game script frequency                         |
| NOVELS                    | Novel corpus                                       |
| VN_FREQ                   | Visual novel corpus                                |
| WIKIPEDIA_V2              | Wikipedia (v2)                                     |
| YOUTUBE_FREQ              | YouTube subtitle frequency                         |
| YOUTUBE_FREQ_V3           | YouTube subtitle frequency (v3, ~187k entries)     |

Note: `DD2_*` sources are from Dave Doebrick's Frequency List Compilation (MIGAKU, MORPHMAN, and YOMICHAN dictionary formats). Three were removed as duplicates: `DD2_YOMICHAN_NETFLIX` (= `NETFLIX`), `DD2_MIGAKU_SOL` (= `DD2_YOMICHAN_SOL`), `DD2_MIGAKU_SHONEN` (= `DD2_YOMICHAN_SHONEN_STARS`).

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

All scripts are standalone and can be run from their respective directories:

```bash
# Generate consolidated multi-source rankings
cd data/ALL
python SCRIPT.py
python CATEGORIZED.py

# Generate ALL cross-source analysis reports
cd data/ALL/scripts
python source_coverage.py > ../insights/source_coverage.md
python source_correlations.py > ../insights/source_correlations.md
python variance_analysis.py > ../insights/variance_analysis.md
python media_profiles.py > ../insights/media_profiles.md
python spoken_vs_written.py > ../insights/spoken_vs_written.md

# Generate CEJC analysis reports
cd data/CEJC/scripts
python vocab_tier_breakdown.py
python domain_profiles.py
python demographic_analysis.py
# ... (see data/CEJC/scripts/ for all 13 scripts)

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

### Coverage is surprisingly concentrated

80% of Japanese text is covered by just ~1,700 words; 90% by ~5,000; 95% by ~9,700; 98% by ~16,000. Focusing on the top 5,000 words gives strong practical coverage for everyday reading.

([Full coverage analysis](data/RSPEER/INSIGHTS.md))

### Cross-source agreement is only partial — and datasets index words differently

The three main sources use different word representations: wordfreq uses surface/written forms; JPDB stores both a `term` (kanji form) and `reading` (kana) and ranks by **reading frequency**, not written frequency (it also tracks `kana_frequency` separately); CEJC uses 語彙素 (canonical lexeme/headword form, e.g. 食べる not 食べた) alongside its kana reading (語彙素読み).

Two methodologies are compared below.

**Result A — exact string match** (surface form only, no reading lookup):

| Comparison    | Top 5k | Top 10k | Top 25k |
| ------------- | ------ | ------- | ------- |
| RSPEER ∩ JPDB | 48.2%  | 48.4%   | 49.0%   |
| RSPEER ∩ CEJC | 47.9%  | 46.2%   | 44.1%   |
| JPDB ∩ CEJC   | 42.6%  | 39.7%   | 39.4%   |
| All three     | 32.2%  | 31.8%   | 31.6%   |

**Result B — reading-aware match** (surface form OR kana reading, readings normalized to hiragana): a word in source A counts as matching source B if its surface form equals either the term/key or the reading in B. This catches cases like RSPEER `くれる` ↔ CEJC `呉れる` or JPDB `今` (reading `いま`) ↔ RSPEER `いま`.

| Comparison    | Top 5k | Top 10k | Top 25k |
| ------------- | ------ | ------- | ------- |
| RSPEER ∩ JPDB | 49.7%  | 49.9%   | 50.4%   |
| RSPEER ∩ CEJC | 53.6%  | 51.1%   | 48.8%   |
| JPDB ∩ CEJC   | 54.6%  | 52.1%   | 54.1%   |
| All three     | 40.3%  | 39.9%   | 40.7%   |

Result B is the better estimate of true conceptual overlap. The JPDB ∩ CEJC improvement (~+12 pp) is the largest because JPDB indexes by reading frequency (kana canonical key) while CEJC indexes by kanji 語彙素 — the same word routinely appears under different scripts in each source. The three-way overlap rises from ~32% to ~40–41%.

Caveats for Result B: (1) **Homophones** — the same kana reading can belong to unrelated words (e.g. particle `ば` vs noun `場`), so reading-based matching can introduce false positives; this affects mostly short function words that already match exactly anyway. (2) **Inflected forms** — RSPEER `なく` (auxiliary) could spuriously match JPDB `泣く` (verb); without POS tagging these are indistinguishable from the kana string alone. (3) **RSPEER kanji words have no reading** — for RSPEER words containing kanji, matching falls back to surface-form only; full reading-aware matching would require MeCab. Result B is therefore an upper bound; the true overlap lies between A and B.

No single list covers everything — even under Result B, only ~40–41% of any tier is shared across all three sources.

([Cross-dataset comparison](data/RSPEER/INSIGHTS.md))

### Kanji dominates at every tier; hiragana and katakana diverge with frequency

Script type composition shifts significantly depending on which tier cutoff you examine:

| Script   | Top 1k | Top 5k | Top 10k | Top 25k |
| -------- | ------ | ------ | ------- | ------- |
| Kanji    | 45.9%  | 49.5%  | 48.6%   | 45.8%   |
| Mixed    | 14.8%  | 18.2%  | 18.5%   | 18.3%   |
| Hiragana | 29.0%  | 14.6%  | 11.8%   | 10.2%   |
| Katakana | 4.6%   | 13.8%  | 16.7%   | 18.9%   |
| Other    | 5.7%   | 3.8%   | 4.4%    | 6.8%    |

Hiragana collapses from 29% in the top 1k to 10% by top 25k — grammatical function words (particles, copulas) are uniquely concentrated at the very top. Katakana (loanwords) grows from 4.6% to 18.9% — loanwords accumulate progressively in lower-frequency ranges. Kanji is consistently the largest category at every cutoff.

([Script breakdown analysis](data/RSPEER/INSIGHTS.md))

### Gender differences in CEJC speech: some robust, some confounded

Some findings are well-supported and linguistically established: gendered first-person pronouns (俺/僕 strongly male, 私 strongly female) and gendered sentence-final particles (ぞ/ぜ male, かしら female) show extreme M/F PMW ratios (3–30×). These reflect real speech style differences.

However, the methodology (raw PMW ratio across all speech by gender) does **not** control for conversation domain. Work/meeting vocabulary (会議, 担当, チーム) skewing male, and food/home vocabulary (野菜, 卵, 菓子) skewing female, may reflect which domains male vs. female participants in this corpus happened to participate in — not an intrinsic property of how men and women speak. Core function words show very little gender skew regardless.

([Demographic analysis](data/CEJC/insights/demographic_analysis.md))

### CEJC rankings are heavily tied at the bottom

Only 430 of 29,534 entries have a unique rank. Most entries share ranks due to tied low-frequency counts, creating a 19,985-rank gap. This is a known artifact of standard competition ranking (1224 style).

([Rank distribution analysis](data/CEJC/insights/rank_distribution.md))

## Source References

- [notes/consolidated-reference-verbose.md](notes/consolidated-reference-verbose.md) — Detailed descriptions of all 22+ frequency sources
- [notes/consolidated-reference-short.md](notes/consolidated-reference-short.md) — Concise reference format

### Main upstream sources

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

## License

MIT License — Copyright 2026 PikaPikaGems. Individual datasets retain their original licenses and attributions as documented in each source's README.
