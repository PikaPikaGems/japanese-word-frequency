# BCCWJ_SUW — Balanced Corpus of Contemporary Written Japanese (Short Unit Word)

## Source
- **Original dict:** https://github.com/toasted-nutbread/yomichan-bccwj-frequency-dictionary/releases
- **NINJAL official:** https://clrd.ninjal.ac.jp/bccwj/en/freq-list.html

## Description
Frequency dictionary derived from the BCCWJ (Balanced Corpus of Contemporary Written Japanese), Japan's first 100-million-word balanced corpus of written Japanese compiled by NINJAL. Designed to represent the breadth of contemporary written Japanese through random sampling across genres.

**Author:** toasted-nutbread
**Data type:** Books, magazines, newspapers, business reports, blogs, internet forums, textbooks, legal documents, National Diet minutes
**Coverage:** Materials from 1976–2006 (main: 1986–2006); 104.3 million words total

This is the **SUW (Short Unit Word)** version. SUW is the smallest morphological unit — particles, auxiliaries, and content words are all separate entries. This is the standard BCCWJ tokenization unit and is what most BCCWJ frequency references use. Compound words are split into their component morphemes; auxiliary verbs are counted separately from their host verbs.

See also: `BCCWJ_LUW` for the Long Unit Word version, where compound words and verb+auxiliary sequences are treated as single units.

## Format (Yomitan JSON)
Multiple `term_meta_bank_*.json` files — each an array of `[word, "freq", {"reading": reading, "frequency": rank}]` entries.

## DATA.csv
Top 25,000 words by frequency rank. Duplicates (same word surface form) are deduplicated by keeping the lowest (most frequent) rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
