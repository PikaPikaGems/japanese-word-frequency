# INNOCENT_RANKED — Innocent Corpus Japanese Novel Frequency (Ranked)

## Source
- **Yomitan dict (MarvNC collection):** https://github.com/MarvNC/yomitan-dictionaries
- **Original Koohii thread (archived):** https://web.archive.org/web/20190309073023/https://forum.koohii.com/thread-9459.html
- **Original creator:** cb4960 (Koohii forum). Ranked version by Marv (MarvNC).

## Description
Frequency list based on a large collection of 5,000+ Japanese novels. The "InnocentRanked" version reorders the original occurrence-based list by rank (most frequent word = rank 1).

Known limitation: does not differentiate by reading — all readings of a term share the same frequency value.

~285k word entries total, split across 28 JSON bank files (10,000 entries each).

Widely used in the Yomichan/Yomitan community as a general-purpose fiction frequency reference.

## Format (Yomitan JSON)
28 `term_meta_bank_N.json` files — each entry: `[word, "freq", rank]` (integer rank, no reading info).

## DATA.csv
Top 25,000 words by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
