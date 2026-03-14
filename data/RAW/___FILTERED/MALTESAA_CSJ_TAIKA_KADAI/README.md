# MALTESAA_CSJ_TAIKA_KADAI — CSJ Domain: 対話・課題 (Dialogue — Task-based)

## Source
- **GitHub:** https://github.com/Maltesaa/CSJ_and_NWJC_yomitan_freq_dict
- **Original corpus:** https://clrd.ninjal.ac.jp/csj/en/

## Description
Domain-specific frequency ranking from the Corpus of Spontaneous Japanese (CSJ) for the **対話・課題** (dialogue, task-based) register. This domain covers dialogue recorded during structured task completion. Same vocabulary as the overall CSJ but with rankings reflecting relative frequency within this domain specifically.

## Format
Yomitan JSON (`term_meta_bank_1.json`) with entries in the format:
`[word, "freq", {"reading": str, "frequency": rank}]`

~42,542 entries.

## DATA.csv
Top 25,000 words by domain frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
