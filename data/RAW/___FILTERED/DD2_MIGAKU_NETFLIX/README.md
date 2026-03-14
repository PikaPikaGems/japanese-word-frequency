# DD2_MIGAKU_NETFLIX — Migaku Netflix Frequency List

## Source
- **Creator:** Dave Doebrick (compiled), Migaku format
- **Collection:** Dave Doebrick's Frequency List Compilation
- **Original document:** https://docs.google.com/document/d/1IUWkvBxhoazBSTyRbdyRVk7hfKE51yorE86DCRNQVuw/edit

## Description
Word frequency list derived from Japanese Netflix subtitles, reformatted as a Migaku dictionary.
Contains ~102,844 entries. Rank is determined by position in the JSON array (index 0 = rank 1).

## Format (`MigakuNetflixfrequency.json`)
JSON array of `[word, reading]` pairs ordered by frequency rank (most frequent first).

## DATA.csv
Top 25,000 words by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
