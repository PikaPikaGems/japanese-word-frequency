# DD2_MORPHMAN_NETFLIX — Morphman Netflix Frequency Report (No Names)

## Source
- **Creator:** Dave Doebrick (compiled), Morphman format
- **Collection:** Dave Doebrick's Frequency List Compilation
- **Original document:** https://docs.google.com/document/d/1IUWkvBxhoazBSTyRbdyRVk7hfKE51yorE86DCRNQVuw/edit

## Description
Word frequency report derived from Netflix subtitle corpus, processed through Morphman with UniDic tokenization.
Proper names excluded. Contains ~105,306 entries. Rank column (index 6) used for ordering.

## Format (`Morphman netflix_unidic_3011_no_names_word_freq_report.txt`)
Tab-separated, columns: `count`, `word`, `reading`, `kana`, `POS`, `sub_POS`, `rank`, `rank2`, `freq%`, `cumfreq%`, `matches`, `number`.

## DATA.csv
Top 25,000 words by rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
