# NIER — Nier Game Japanese Word Frequency (Shoui)

## Source
- **Shoui's collection:** https://anacreondjt.gitlab.io/docs/freq/
- **MarvNC collection:** https://github.com/MarvNC/yomitan-dictionaries

## Description
Game-specific word frequency list derived from the Nier game series (Japanese). Part of the Shoui frequency dictionaries collection. Contains ~10k unique word entries.

Useful as a domain-specific reference for game vocabulary, particularly for the Nier series.

## Format (Yomitan JSON)
Single `term_meta_bank_1.json` — each entry: `[word, "freq", "rank/total"]` (rank stored as fraction string, e.g. `"1/10077"`).

## DATA.csv
All ~10k words by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
