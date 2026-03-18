# KUUUUBE_JMDICT_FREQ — JMdict Newspaper Frequency (Rank-Based)

## Source
- **GitHub:** https://github.com/Kuuuube/jmdict_kanji_freq (distributed as a Yomitan frequency dictionary)

## Description
Rank-based frequency data derived from JMdict's newspaper processing. Created by Kuuube. Distributed as a Yomitan dictionary with the title "JMdict Freq".

**Author:** Kuuube
**Data type:** Newspaper / dictionary-derived frequency ranks
**Source description (from index.json):** "Rank-based frequency data from JMdict newspaper processing"

## Format (Yomitan JSON)
Single `term_meta_bank_1.json` file — an array of `[word, "freq", {"value": rank, "displayValue": rank}]` entries. Some words appear multiple times with different rank values (duplicate surface forms across different readings or dictionary senses); duplicates are resolved by keeping the lowest (most frequent) rank.

## DATA.csv
Top 25,000 words by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
