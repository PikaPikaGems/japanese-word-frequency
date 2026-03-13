# NOVELS — Japanese Novels Word Frequency (Kuuube / MarvNC)

## Source
- **Yomitan dict (MarvNC collection):** https://github.com/MarvNC/yomitan-dictionaries
- **Lookup tool (Kuuube):** https://kuuuube.github.io/japanese-word-frequency/

## Description
Frequency list derived from 10,000+ Japanese novels, created by Kuuube and distributed via MarvNC's collection. Larger novel count than the Innocent Corpus (which uses 5,000+ novels), providing broader coverage with ~270k unique word entries.

The frequency ranking starts at 0 (most frequent). Note that rank 0 is `、` (Japanese comma/punctuation). The data is fiction-focused.

## Format (Yomitan JSON)
Single `term_meta_bank_1.json` file — each entry: `[word, "freq", rank]` (integer, 0-indexed rank).

## DATA.csv
Top 25,000 words by frequency rank (rank 0 becomes FREQUENCY_RANKING 1). Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
