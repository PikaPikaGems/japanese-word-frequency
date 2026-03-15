# BCCWJ_LUW — Balanced Corpus of Contemporary Written Japanese (Long Unit Word)

## Source
- **Original dict:** https://github.com/toasted-nutbread/yomichan-bccwj-frequency-dictionary/releases
- **NINJAL official:** https://clrd.ninjal.ac.jp/bccwj/en/freq-list.html

## Description
Frequency dictionary derived from the BCCWJ (Balanced Corpus of Contemporary Written Japanese), Japan's first 100-million-word balanced corpus of written Japanese compiled by NINJAL. Designed to represent the breadth of contemporary written Japanese through random sampling across genres.

**Author:** toasted-nutbread
**Data type:** Books, magazines, newspapers, business reports, blogs, internet forums, textbooks, legal documents, National Diet minutes
**Coverage:** Materials from 1976–2006 (main: 1986–2006); 104.3 million words total

This is the **LUW (Long Unit Word)** version. LUW groups compound words and verb+auxiliary sequences into single units. For example, 食べました is one LUW entry (polite past "ate"), whereas SUW counts 食べる and ます as separate vocabulary items. LUW ranks tend to surface more content words and compound expressions as learners would encounter them in context, and show more consistent frequency patterns across text difficulty levels.

See also: `BCCWJ_SUW` for the Short Unit Word version, where all morphological units are counted separately.

## Format (Yomitan JSON)
Multiple `term_meta_bank_*.json` files — each an array of `[word, "freq", {"reading": reading, "frequency": rank}]` entries.

## DATA.csv
Top 25,000 words by frequency rank. Duplicates (same word surface form) are deduplicated by keeping the lowest (most frequent) rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
