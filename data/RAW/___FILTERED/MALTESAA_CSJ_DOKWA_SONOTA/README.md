# MALTESAA_CSJ_DOKWA_SONOTA — CSJ Domain: 独話・その他 (Monologue — Other)

## Source
- **GitHub:** https://github.com/Maltesaa/CSJ_and_NWJC_yomitan_freq_dict
- **Original corpus:** https://clrd.ninjal.ac.jp/csj/en/

## Description
Domain-specific frequency ranking from the Corpus of Spontaneous Japanese (CSJ) for the **独話・その他** (monologue, other) register. This domain covers monologue recordings that do not fit the other defined categories. Same vocabulary as the overall CSJ but with rankings reflecting relative frequency within this domain specifically.

## Format
Yomitan JSON (`term_meta_bank_1.json`) with entries in the format:
`[word, "freq", {"reading": str, "frequency": rank}]`

~42,542 entries.

## DATA.csv
Top 25,000 words by domain frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
