# DD2_YOMICHAN_SOL — Yomichan Slice of Life Top 100 Frequency List

## Source
- **Creator:** Dave Doebrick (compiled), Yomichan format
- **Collection:** Dave Doebrick's Frequency List Compilation
- **Original document:** https://docs.google.com/document/d/1IUWkvBxhoazBSTyRbdyRVk7hfKE51yorE86DCRNQVuw/edit

## Description
Word frequency list derived from the top 100 Slice of Life anime titles, packaged as a Yomichan dictionary (no star ratings, integer ranks).
Contains ~43,125 entries. Note: `SOL_Top_100_Stars` contains the same data with star formatting.

## Format (`SoL Top 100/term_meta_bank_1.json`)
JSON array of `[word, "freq", rank_integer]` entries.

## DATA.csv
Top 25,000 words by rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
