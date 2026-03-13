# KOKUGOJITEN — 国語辞典 Japanese Dictionary Word Frequency (Shoui)

## Source
- **Shoui collection:** https://anacreondjt.gitlab.io/docs/freq/
- **MarvNC collection:** https://github.com/MarvNC/yomitan-dictionaries

## Description
Word frequency list derived from a Japanese monolingual dictionary (国語辞典, kokugojiten). Part of the Shoui frequency dictionaries collection. Contains ~156k unique word entries.

This represents vocabulary from a standard Japanese dictionary, prioritizing commonly-used native Japanese words. Note that rank 5 is `・` (interpunct/nakaguro), suggesting some punctuation is included.

## Format (Yomitan JSON)
Single `term_meta_bank_1.json` — each entry: `[word, "freq", rank]` (integer rank, 1-indexed).

## DATA.csv
Top 25,000 words by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
