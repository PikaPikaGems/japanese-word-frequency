# ADNO — Japanese Wikipedia Word Frequency (Cleaned)

## Source
- **GitHub:** https://github.com/adno/wikipedia-word-frequency-clean
- **Original data:** https://github.com/IlyaSemenov/wikipedia-word-frequency
- **Data date:** October 20, 2022 (jawiki dump)

## Description
A cleaned word frequency list derived from the Japanese Wikipedia dump. This is a fork/refinement of IlyaSemenov's `wikipedia-word-frequency` project, with additional filtering applied. The base file (`jawiki-frequency-20221020.tsv`) is used here (no lowercasing, no NFKC normalization, no minimum document threshold).

Multiple variants are available in the source:
- **Base** (`jawiki-frequency-20221020.tsv`): all words, case-preserved
- **-nfkc**: Unicode NFKC normalization applied
- **-lower**: Lowercased
- **-310**: Filtered to words appearing in at least 310 documents

## Format
TSV with 3 columns: `word`, `count` (total occurrences), `documents` (number of articles containing the word). Data is pre-sorted by `count` descending.

## File Used
`jawiki-frequency-20221020.tsv` (~550k entries)

## DATA.csv
Top 25,000 words by occurrence count. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
