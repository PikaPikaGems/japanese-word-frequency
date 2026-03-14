# JLAB — Japanese Like a Breeze Anime Frequency List

## Source
- **Website:** https://www.japanese-like-a-breeze.com
- **Data:** https://docs.google.com/spreadsheets/d/1xeG-b85EHwo-yUDgwDLuWyYdwtnDgJAzr3VTmteMOaA/edit

## Description
A Japanese word frequency list computed from 301 Anki decks (mostly anime, some dorama), totaling ~1.85 million flashcards/sentences. Source decks come from the Japanese Decks blog (https://japanesedecks.blogspot.com). Only the `Expression` column is relevant for frequency; readings are incomplete (first jmdict entry only).

## Format
Tab-separated file (`JLAB.tsv`) with 2 metadata lines followed by a header row:
1. `Expression` — the Japanese word/expression
2. `Occurences` — total occurrence count in the corpus
3. `Reading` — kana reading (may be incomplete or contain multiple readings)
4. `Roumaji` — romanization

The file has ~67,587 entries, pre-sorted by occurrence count descending.

## DATA.csv
Top 25,000 words by occurrence count. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
