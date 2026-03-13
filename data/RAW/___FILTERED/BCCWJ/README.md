# BCCWJ — Balanced Corpus of Contemporary Written Japanese

## Source
- **Yomitan dict by Kuuube:** https://github.com/Kuuuube/yomitan-dictionaries
- **Original dict:** https://github.com/toasted-nutbread/yomichan-bccwj-frequency-dictionary
- **NINJAL official:** https://clrd.ninjal.ac.jp/bccwj/en/freq-list.html

## Description
Frequency dictionary derived from the BCCWJ (Balanced Corpus of Contemporary Written Japanese), Japan's first 100-million-word balanced corpus of written Japanese compiled by NINJAL. Designed to represent the breadth of contemporary written Japanese through random sampling across genres.

**Authors:** toasted-nutbread, Kuuube
**Data type:** Books, magazines, newspapers, business reports, blogs, internet forums, textbooks, legal documents, National Diet minutes
**Coverage:** Materials from 1976–2006 (main: 1986–2006); 104.3 million words total

This is the **combined SUW (Short Unit Word) + LUW (Long Unit Word)** version, containing ~1 million unique entries. The frequency value represents frequency rank (lower = more frequent). Ties exist (multiple words at same rank).

## Format (Yomitan JSON)
`term_meta_bank_1.json` — array of `[word, "freq", {"reading": reading, "frequency": rank}]` entries.

## DATA.csv
Top 25,000 words by frequency rank. When multiple words share the same rank, they are ordered by their position in the source file (stable sort). Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
