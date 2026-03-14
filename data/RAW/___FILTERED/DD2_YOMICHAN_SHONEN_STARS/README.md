# DD2_YOMICHAN_SHONEN_STARS — Yomichan Shonen Stars Frequency List

## Source
- **Creator:** Dave Doebrick (compiled), Yomichan format
- **Collection:** Dave Doebrick's Frequency List Compilation
- **Original document:** https://docs.google.com/document/d/1IUWkvBxhoazBSTyRbdyRVk7hfKE51yorE86DCRNQVuw/edit

## Description
Word frequency list derived from Shonen manga/anime corpus, packaged as a Yomichan dictionary with star ratings.
Contains ~56,396 entries.

## Format (`Shonen_freq_list_Stars/term_meta_bank_1.json`)
JSON array of `[word, "freq", "★★★★★ (rank)"]` entries. Rank is parsed from the parenthesized number.

## DATA.csv
Top 25,000 words by rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
