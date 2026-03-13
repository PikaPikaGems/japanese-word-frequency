# CHRISKEMPSON — Japanese Subtitles Word Frequency

## Source
- **GitHub:** https://github.com/chriskempson/japanese-subtitles-word-kanji-frequency-lists
- **Subtitle source:** https://github.com/Matchoo95/JP-Subtitles

## Description
Word frequency list derived from 12,277 Japanese subtitle files for drama, anime, and films. Generated using JParser and cb's Japanese Text Analysis Tool.

## Format
Tab-separated file (`word_freq_report.txt`) with columns:
1. `occurrence_count` — total occurrences in corpus
2. `word` — the Japanese word
3. `frequency_group` — broader frequency bucket
4. `frequency_rank` — sequential rank (1 = most frequent)
5. `percentage` — percentage of total corpus
6. `cumulative_percentage` — running cumulative percentage
7. `POS` — part of speech tag(s)

The file has ~120,488 entries, pre-sorted by occurrence count descending. The rank column directly gives the ordering.

## License
MIT

## DATA.csv
Top 25,000 words by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
