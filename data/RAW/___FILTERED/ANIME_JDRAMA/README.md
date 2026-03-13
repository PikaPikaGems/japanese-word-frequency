# ANIME_JDRAMA — Anime & J-drama Japanese Word Frequency (Shoui)

## Source
- **Shoui's collection:** https://anacreondjt.gitlab.io/docs/freq/
- **MarvNC collection:** https://github.com/MarvNC/yomitan-dictionaries

## Description
Word frequency list derived from anime and Japanese drama (J-drama) subtitles. Part of the Shoui frequency dictionaries collection. Contains ~100k unique word entries.

Useful for learners consuming anime and drama content.

## Format (Yomitan JSON)
Single `term_meta_bank_1.json` — each entry: `[word, "freq", rank]` (integer rank, 1-indexed).

## DATA.csv
Top 25,000 words by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
