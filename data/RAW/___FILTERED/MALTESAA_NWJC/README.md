# MALTESAA_NWJC — NINJAL Web Japanese Corpus (NWJC) Frequency

## Source
- **GitHub:** https://github.com/Maltesaa/CSJ_and_NWJC_yomitan_freq_dict
- **Original corpus:** https://masayu-a.github.io/NWJC/

## Description
A Yomitan-format frequency dictionary derived from the NINJAL Web Japanese Corpus (NWJC), a large web-based written Japanese corpus. The NWJC is a broad written language resource covering a wide range of web text. Goes up to rank 106,762.

## Format
Yomitan JSON (`term_meta_bank_1.json`) in the " NWJC" subdirectory (note the leading space in the directory name) with entries in the format:
`[word, "freq", {"reading": str, "frequency": rank}]`

The file has ~106,754 entries, ordered by frequency rank ascending (1 = most frequent).

## DATA.csv
Top 25,000 words by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
