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

| Source                  | Type                                               |
| ----------------------- | -------------------------------------------------- |
| ADNO                    | Wikipedia (cleaned)                                |
| ANIME_JDRAMA            | Anime & J-drama subtitles                          |
| AOZORA_BUNKO            | Public domain literature                           |
| BCCWJ                   | Balanced written corpus (NINJAL, 100M words)       |
| CC100                   | Web text (Common Crawl)                            |
| CHRISKEMPSON            | Japanese subtitles                                 |
| DAVE_DOEBRICK           | Netflix subtitles (Dave Doebrick, full report)     |
| DD2_MIGAKU_NETFLIX      | Netflix subtitles (Migaku dictionary format)       |
| DD2_MIGAKU_NOVELS       | Novel corpus (Migaku dictionary format)            |
| DD2_MORPHMAN_NETFLIX    | Netflix subtitles (Morphman report, no names)      |
| DD2_MORPHMAN_NOVELS     | Novel corpus (Morphman report)                     |
| DD2_MORPHMAN_SHONEN     | Shonen anime/manga (Morphman report)               |
| DD2_MORPHMAN_SOL        | Slice of Life anime (Morphman report)              |
| DD2_YOMICHAN_NOVELS     | Novel corpus (Yomichan Stars format)               |
| DD2_YOMICHAN_SHONEN     | Shonen anime/manga (Yomichan integer rank format)  |
| DD2_YOMICHAN_SHONEN_STARS | Shonen anime/manga (Yomichan Stars format)       |
| DD2_YOMICHAN_SOL        | Slice of Life anime (Yomichan integer rank format) |
| DD2_YOMICHAN_VN         | Visual novels (Yomichan Stars format)              |
| HERMITDAVE_2016         | Subtitle corpus (2016)                             |
| HERMITDAVE_2018         | Subtitle corpus (2018)                             |
| H_FREQ                  | Community-compiled list                            |
| ILYASEMENOV             | Wikipedia word frequency                           |
| INNOCENT_RANKED         | Innocent Corpus (novels)                           |
| JITEN_ANIME             | Anime-focused frequency                            |
| JPDB                    | Entertainment media (jpdb.io)                      |
| KOKUGOJITEN             | Japanese dictionary headwords                      |
| MONODICTS               | Monolingual dictionary terms                       |
| NAROU                   | Web novels (Narou)                                 |
| NETFLIX                 | Netflix subtitle frequency                         |
| NIER                    | NieR game script frequency                         |
| NOVELS                  | Novel corpus                                       |
| VN_FREQ                 | Visual novel corpus                                |
| WIKIPEDIA_V2            | Wikipedia (v2)                                     |
| YOUTUBE_FREQ            | YouTube subtitle frequency                         |
| YOUTUBE_FREQ_V3         | YouTube subtitle frequency (v3, ~187k entries)     |

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

### Cross-source agreement is only partial

Only ~49% of RSPEER's top 25k overlaps with JPDB, and ~46% with CEJC — reflecting how differently spoken conversation, entertainment media, and general web text rank vocabulary. No single list covers everything.

([Cross-dataset comparison](data/RSPEER/INSIGHTS.md))

### Kanji dominates high-frequency words

Script type breakdown across RSPEER's top 25k: 45.8% kanji, 18.9% katakana, 18.3% mixed kanji+kana, 10.2% hiragana. Katakana (loanwords) cluster more in the middle and lower frequency tiers.

([Script breakdown analysis](data/RSPEER/INSIGHTS.md))

### Word length grows with lower frequency (Zipf's law of abbreviation)

Average word length in the top 1k is ~1.9 characters, growing to ~2.8 characters in the 10k–25k range. The most common words are also the shortest.

([Word length by tier](data/RSPEER/INSIGHTS.md))

### Gender differences in CEJC speech are real but vocabulary-specific

Male speech strongly favors rough first-person pronouns (俺, 僕), work/group vocabulary (会議, 担当, チーム), and masculine sentence-final particles (ぞ, ぜ). Female speech strongly favors 私 (vs 俺/僕), descriptive adjectives (可愛い, 素敵, 美味しい, 優しい), and food/domestic vocabulary (野菜, 卵, 菓子). Core function words show very little gender skew.

([Demographic analysis](data/CEJC/insights/demographic_analysis.md))

### CEJC rankings are heavily tied at the bottom

Only 430 of 29,534 entries have a unique rank. Most entries share ranks due to tied low-frequency counts, creating a 19,985-rank gap. This is a known artifact of standard competition ranking (1224 style).

([Rank distribution analysis](data/CEJC/insights/rank_distribution.md))

### Vocabulary priorities differ by conversation domain

Medical consultations and workplace conversations skew toward formal Sino-Japanese (漢語) vocabulary, while casual home conversation favors native Japanese (和語) and common verbs.

([Domain profiles](data/CEJC/insights/domain_profiles.md) · [Learning priority](data/CEJC/insights/learning_priority.md))

### Word origin composition shifts across frequency tiers

和語 (native Japanese) dominates the basic tier. 漢語 (Sino-Japanese) grows steadily through the advanced range. 外来語 (loanwords) peak in the fluent–advanced range.

([Origin trends](data/CEJC/insights/origin_trends.md))

### Source coverage varies widely — no word appears in all 35 sources

YOUTUBE_FREQ_V3 covers 78% of words; most sources cover 35–45%; HERMITDAVE_2018 covers only 22 words (likely a data issue). No word is ranked by all 35 sources. 4,140 words are CEJC-exclusive — mostly proper nouns and spoken-only vocabulary absent from every written corpus.

([Source coverage](data/ALL/insights/source_coverage.md))

### DAVE_DOEBRICK and NETFLIX are near-identical (r = 0.991)

The highest pairwise source correlation is between DAVE_DOEBRICK and NETFLIX (Spearman r = 0.991) — almost certainly the same underlying subtitle data in different formats. The lowest correlation is DD2_MORPHMAN_NETFLIX vs. KOKUGOJITEN (r = 0.100): media transcriptions and dictionary headwords are nearly orthogonal for frequency ranking.

([Source correlations](data/ALL/insights/source_correlations.md))

### Consistently ranked words are abstract 漢語; contested words are kanji/kana spelling alternates

Words with the lowest cross-source variance (most universally agreed upon) are general-purpose Sino-Japanese terms: 判断, 原因, 理解, 可能, 重要, 影響. The most contested words are archaic kanji spellings of common words — 其れ (それ), 此れ (これ), 矢張り (やはり) — ranked basic in literary corpora but rare or absent in web and subtitle corpora.

([Variance analysis](data/ALL/insights/variance_analysis.md))

### Only 114 words are universally "basic" across 25+ sources

Cross-source consensus on "basic" vocabulary is much stricter than expected: only 114 words are ranked in the top ~1,000 by 25 or more sources. Top consensus words: 者, 関係, 何, 自分, 必要, 時間, 意味, 場所, 人間, 相手.

([Variance analysis](data/ALL/insights/variance_analysis.md))

### Each media type has a strongly distinctive vocabulary profile

Slice-of-life anime sources disproportionately rank character names and school-life terms (席替え, 追試). YouTube distinctively ranks practical/DIY vocabulary (画角, コンセント, 付箋). Dictionary sources uniquely surface classical terms (なむ, 若紫, 雅楽). These signatures reveal the domain bias baked into each corpus.

([Media profiles](data/ALL/insights/media_profiles.md))

### Food vocabulary dominates spoken-only words; narrative vocabulary dominates written-only words

Words the CEJC spoken corpus ranks much higher than all written/media sources are predominantly food and ingredient terms: 竹の子, 山葵, 生姜, 蓮根, 鯵, 白子. Words far more common in written/media than in speech are narrative/action vocabulary: 真実, 兵士, 任務, 取り戻す, 死体, 竜, 一族 — staples of anime and novels that almost never come up in everyday conversation.

([Spoken vs. written](data/ALL/insights/spoken_vs_written.md))

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
- https://drive.google.com/drive/folders/1g1drkFzokc8KNpsPHoRmDJ4OtMTWFuXi
- https://drive.google.com/drive/folders/1xURpMJN7HTtSLuVs9ZtIbE7MDRCdoU29
- https://drive.google.com/file/d/1qHEfYHXjEp83i6PxxMlSxluFyQg2W8Up
- https://docs.google.com/document/d/1IUWkvBxhoazBSTyRbdyRVk7hfKE51yorE86DCRNQVuw/edit

## License

MIT License — Copyright 2026 PikaPikaGems. Individual datasets retain their original licenses and attributions as documented in each source's README.
