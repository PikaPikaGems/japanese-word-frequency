# DD2_MIGAKU_NOVELS — Migaku Novel 5k Frequency List

## Source
- **Creator:** Dave Doebrick (compiled), Migaku format
- **Collection:** Dave Doebrick's Frequency List Compilation
- **Original document:** https://docs.google.com/document/d/1IUWkvBxhoazBSTyRbdyRVk7hfKE51yorE86DCRNQVuw/edit

## Description
Word frequency list derived from a Japanese novel corpus (top 5k coverage), reformatted as a Migaku dictionary.
Contains ~16,469 entries. Rank is determined by position in the JSON array (index 0 = rank 1).

## Format (`Novel_5k.json`)
JSON array of `[word, reading]` pairs ordered by frequency rank (most frequent first). BOM-encoded (utf-8-sig).

## DATA.csv
All ~16,469 entries. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
