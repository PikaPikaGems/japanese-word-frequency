# HLORENZI_WIKIPEDIA — hlorenzi Jisho-open Wikipedia Rankings

## Source

- **GitHub:** https://github.com/hlorenzi/jisho-open/blob/main/backend/src/data/word_rankings_wikipedia.txt
- **Wiktionary mirror:** https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Japanese/Wikipedia2013

## Description

Word frequency rankings derived from Japanese Wikipedia, used by the jisho-open dictionary project.

**Author:** hlorenzi
**Data type:** web text / encyclopedia (Wikipedia)
**Coverage:** Japanese Wikipedia (~2013 snapshot, ~20,000 entries)

## Format (plain text)

One word per line, ordered by frequency rank. Line 1 is the most frequent word (rank 1). No header row.

## DATA.csv

Top 25,000 words by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
(Source has ~20,000 entries, so all entries are included.)
