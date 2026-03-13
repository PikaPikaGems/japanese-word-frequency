# NETFLIX — Netflix Japanese Subtitles Word Frequency (Shoui)

## Source
- **Shoui collection:** https://anacreondjt.gitlab.io/docs/freq/
- **MarvNC collection:** https://github.com/MarvNC/yomitan-dictionaries

## Description
Word frequency list derived from Japanese subtitles available on Netflix. Part of the Shoui frequency dictionaries collection. Contains ~129k unique word entries.

Note: This is distinct from the DAVE_DOEBRICK dataset which is also Netflix-derived but comes from a different source/format (Dave Doebrick's word_freq_report.txt using cb's Japanese Text Analysis Tool).

## Format (Yomitan JSON)
Single `term_meta_bank_1.json` — each entry: `[word, "freq", rank]` (integer rank, 1-indexed).

## DATA.csv
Top 25,000 words by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
