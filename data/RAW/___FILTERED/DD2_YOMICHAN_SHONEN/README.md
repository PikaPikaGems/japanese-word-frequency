# DD2_YOMICHAN_SHONEN — Yomichan Shonen Top 100 Frequency List

## Source
- **Creator:** Dave Doebrick (compiled), Yomichan format
- **Collection:** Dave Doebrick's Frequency List Compilation
- **Original document:** https://docs.google.com/document/d/1IUWkvBxhoazBSTyRbdyRVk7hfKE51yorE86DCRNQVuw/edit

## Description
Word frequency list derived from the top 100 Shonen manga/anime titles, packaged as a Yomichan dictionary (no star ratings, integer ranks).
Contains ~56,389 entries. Note: `DD2_YOMICHAN_SHONEN_STARS` contains star-formatted data from the same corpus (different ranking).

## Format (`Shonen Top 100/term_meta_bank_1.json`)
JSON array of `[word, "freq", rank_integer]` entries.

## DATA.csv
Top 25,000 words by rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
