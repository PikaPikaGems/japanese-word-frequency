# JITEN_ANIME — Anime Word Frequency from jiten.moe

## Source
- **Shoui collection / jiten.moe:** https://jiten.moe
- **API:** https://api.jiten.moe/api/frequency-list/download?mediaType=Anime
- **Author:** Jiten

## Description
Word frequency dictionary based on anime media frequency data from jiten.moe. Contains ~257k entries. Rank-based frequency, updated periodically (revision: 2026-01-10).

Two entry types exist in the source data:
1. Primary entries: `[word, "freq", {"value": rank, "displayValue": "rank㋕"}]`
2. Reading variants: `[word, "freq", {"reading": reading, "frequency": {"value": rank, ...}}]`

Both are included; when a word appears in multiple entry types, the lowest rank (most frequent) is used.

## Format (Yomitan JSON)
Single `term_meta_bank_1.json` — mixed format entries.

## DATA.csv
Top 25,000 words by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
