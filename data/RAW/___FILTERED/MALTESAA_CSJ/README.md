# MALTESAA_CSJ — Corpus of Spontaneous Japanese (CSJ) Frequency

## Source
- **GitHub:** https://github.com/Maltesaa/CSJ_and_NWJC_yomitan_freq_dict
- **Original corpus:** https://clrd.ninjal.ac.jp/csj/en/

## Description
A Yomitan-format frequency dictionary derived from the Corpus of Spontaneous Japanese (CSJ), jointly developed by NINJAL, NICT, and the Tokyo Institute of Technology. The CSJ is a large collection of Japanese spoken language data for linguistic research, world-class in both quantity and quality. Goes up to rank 31,605.

## Format
Yomitan JSON (`term_meta_bank_1.json`) with entries in the format:
`[word, "freq", {"reading": str, "frequency": rank}]`

The file has ~42,542 entries, ordered by frequency rank ascending (1 = most frequent).

## DATA.csv
Top 25,000 words by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
