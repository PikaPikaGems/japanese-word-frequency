# WIKIPEDIA_V2 — Japanese Wikipedia Word Frequency (Shoui/MarvNC)

## Source
- **Yomitan dict (MarvNC / Shoui collections):** https://github.com/MarvNC/yomitan-dictionaries
- **Reference:** https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Japanese2015_10000
- **Author:** Thermospore

## Description
Japanese Wikipedia-based word frequency dictionary, v2. Moved to a much larger dataset in v2 — the list covers ~850k unique words. A community-created Yomitan frequency dictionary.

Revision history:
- v0.1: Shortened title + metadata
- v1: Reserved (never completed)
- v2: Expanded to ~850k entries from larger Wikipedia dataset

## Format (Yomitan JSON)
Single `term_meta_bank_1.json` — each entry: `[word, "freq", rank]` (integer rank, 1-indexed).

## DATA.csv
Top 25,000 words by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
