> **Use at your own risk.** The code and logic for generating this data have not been fully reviewed. Data quality, coverage, and methodology vary across sources. No guarantees are made about accuracy, completeness, or fitness for any particular purpose.

# Japanese Word Frequency Rankings

A comprehensive collection of Japanese word frequency datasets, analysis scripts, and insights, consolidating datasets into unified formats for language learning, linguistics, and NLP research.

## TODO: What should be the name of this section?

Repository Structure

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

- `data/ALL/` - The primary output of this repo. Each `consolidated.csv` is a matrix of **words × rank columns**, one column per frequency source.
- [CONSOLIDATED_CSV_REFERENCEV1.md](CONSOLIDATED_CSV_REFERENCEV1.md) — How to read `consolidated.csv` (Aggregated Frequency Word Rankings): column layout, practical interpretation guide, and per-source caveats
- TODO: Add reference to dataset-directory-tree.md here
- TODO; Add reference to running-scripts.md here

## TODO: What should be the name of this section?

### Experiments

- [data/ALL/\_\_\_experiments2/PAIRWISE_OVERLAPS.md](data/ALL/___experiments2/PAIRWISE_OVERLAPS.md) — Pairwise reading-aware overlap tables for thematically grouped source datasets (Japanese web, Wikipedia, YouTube, Netflix/drama, slice-of-life, anime) at Top-2k, 5k, and 10k
- TODO: add notable-insights-03-18-2026.md here
- TODO: Add data-quality-summary-03-18-2026.md here
- [`data/ALL/___experiments0/HISTORY.md`](data/ALL/___experiments0/HISTORY.md) documents the bugs, anomalies, and design decisions discovered while consolidating frequency sources.
- [`data/ALL/___experiments1/HISTORY.md`](data/ALL/___experiments1/HISTORY.md) documents findings from re-running coverage experiments after the dataset grew from ~35 to 60 external sources and 4 new anchors were added.

### Dataset Descriptions

- [notes/cleaned-datasets-reference-v1.md](notes/cleaned-datasets-reference-v1.md) — Detailed descriptions of some frequency rank datasets included in the database, with source notes on corpus size, register, and tokenization
- [notes/consolidated-reference-verbose.md](notes/consolidated-reference-verbose.md) — Detailed descriptions of some frequency sources
- [notes/consolidated-reference-short.md](notes/consolidated-reference-short.md) — Bullet point information of some frequency sources

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

## License

MIT License — Copyright 2026 PikaPikaGems. Individual datasets retain their original licenses and attributions as documented in each source's README.
