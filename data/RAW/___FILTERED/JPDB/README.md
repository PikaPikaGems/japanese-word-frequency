# JPDB — Japanese Entertainment Media Word Frequency

## Source
- **Shoui/MarvNC collections:** https://github.com/MarvNC/yomitan-dictionaries
- **jpdb.io:** https://jpdb.io/
- **Scraper:** https://github.com/MarvNC/jpdb-freq-list
- **Authors:** jpdb, Marv (MarvNC)

## Description
Frequency dictionary scraped from jpdb.io's large corpus of Japanese entertainment media. This is the "Recommended" version distributed by Shoui (JPDBv2 is a more recent expanded version).

**Data type:** Light novels, visual novels, anime, J-drama, web novels — Japanese entertainment/fiction media
**Data date:** May 10, 2022
**Coverage:** ~515k entries

Notable feature: displays separate frequencies for kanji and kana versions of words (marked with ㋕). Words not appearing in the JPDB corpus are marked with ❌.

The `displayValue` field shows the rank with ㋕ suffix (e.g., `"1㋕"`) to indicate kana readings.

## Format (Yomitan JSON)
Single `term_meta_bank_1.json` — each entry: `[word, "freq", {"value": rank, "displayValue": "rank㋕"}]`.

## DATA.csv
Top 25,000 words by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
