# AOZORA_BUNKO — Aozora Bunko Kanji/Jukugo Frequency

## Source
- **Yomitan dict (MarvNC collection):** https://github.com/MarvNC/yomitan-dictionaries
- **Data source:** https://vtrm.net/japanese/kanji-jukugo-frequency/en
- **Aozora Bunko:** https://www.aozora.gr.jp/
- **Authors:** vtrm (data), Marv (Yomitan conversion)

## Description
Rank-based kanji and jukugo (compound word) frequency list derived from the **Aozora Bunko** (青空文庫), Japan's public-domain digital library of primarily pre-1953 literature whose copyrights have expired.

**Important caveats:**
- Does **not** cover words with kana — only kanji and jukugo are included
- ~120k word entries (plus ~8k kanji entries)
- Useful as a supplement for classical/literary vocabulary and rare jukugo not found in other frequency lists
- Parsing is kana-agnostic: different readings of the same kanji form are grouped together

The `displayValue` field includes the occurrence count in parentheses, e.g. `"1 (12407)"` means rank 1, appeared in 12,407 documents.

## Format (Yomitan JSON)
Single `term_meta_bank_1.json` — each entry: `[word, "freq", {"value": rank, "displayValue": "rank (count)"}]`.

## DATA.csv
Top 25,000 entries by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
