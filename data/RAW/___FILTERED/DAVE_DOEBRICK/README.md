# DAVE_DOEBRICK — Netflix Japanese Subtitles Word Frequency

## Source
- **Creator:** Dave Doebrick (YouTube: OhTalkWho オタク, Twitter: @DaveDoeb)
- **Video:** https://www.youtube.com/watch?v=DwJWld8hW0M
- **Google Drive:** https://drive.google.com/file/d/1qHEfYHXjEp83i6PxxMlSxluFyQg2W8Up

## Description
Word frequency list derived from all Japanese subtitles available on Netflix Japan at the time of collection (~2019). Created using cb's Japanese Text Analysis Tool. The corpus contains 53 million total kanji occurrences.

## Files in Source
- `word_freq_report.txt`: Full word frequency report (~124,360 entries) — **used for DATA.csv**
- `Netflix 95% 12K.txt`: A curated list of ~12,000 words covering 95% of Netflix Japanese subtitle content (word names only, no frequency numbers)

## Format (`word_freq_report.txt`)
Tab-separated with BOM, columns:
1. `occurrence_count`
2. `word`
3. `frequency_group`
4. `frequency_rank` (1 = most frequent)
5. `percentage`
6. `cumulative_percentage`
7. `POS` (Japanese POS tags)

## DATA.csv
Top 25,000 words by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
