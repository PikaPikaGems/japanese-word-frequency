# NAROU — 小説家になろう (Narou Web Novels) Word Frequency

## Source
- **Shoui collection:** https://anacreondjt.gitlab.io/docs/freq/
- **Wareya's analysis:** http://wiki.wareya.moe/Narou
- **jpstats GitHub:** https://github.com/wareya/jpstats/tree/master/narou

## Description
Word frequency list derived from the top 300 stories on 小説家になろう (Shousetsuka ni Narou), Japan's most popular web novel platform. Created by wareya using the jpstats tool with Kuromoji for word segmentation.

Contains ~49k unique word entries. Wareya notes these are hobbyist analyses with no quality guarantees.

Useful for learners reading web novels (isekai, fantasy, etc.) on Narou or similar platforms.

## Format (Yomitan JSON)
Single `term_meta_bank_1.json` — each entry: `[word, "freq", {"reading": reading, "frequency": rank}]`.

## DATA.csv
Top 25,000 words by frequency rank (all 49k entries fit within this limit). Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
