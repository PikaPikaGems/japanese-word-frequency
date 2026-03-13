# VN_FREQ — Visual Novel Japanese Word Frequency (Shoui / wareya)

## Source
- **Shoui collection:** https://anacreondjt.gitlab.io/docs/freq/
- **Wareya VN stats:** http://wiki.wareya.moe/Stats
- **jpstats GitHub:** https://github.com/wareya/jpstats

## Description
Word frequency list derived from 100+ visual novel script dumps (30+ million words total). Created by wareya using the jpstats tool with Kuromoji for word segmentation. This is version 2 of the VN frequency list.

Contains ~35k unique word entries. Wareya notes these are hobbyist analyses with no quality guarantees.

Useful for learners reading visual novels. Entries use the dictionary/lemma form of words (e.g., 為る for する, 居る for いる).

## Format (Yomitan JSON)
Single `term_meta_bank_1.json` — each entry: `[word, "freq", {"reading": reading, "frequency": rank}]`.

## DATA.csv
Top 25,000 words by frequency rank (35k total entries). Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
