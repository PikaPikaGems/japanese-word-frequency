# JPDB v2.2 Frequency Data

Source: [jpdb_v2.2_freq_list_2024-10-13.csv](https://github.com/Kuuuube/yomitan-dictionaries/blob/main/data/jpdb_v2.2_freq_list_2024-10-13.csv)

## Files

### `jpdb_v2.2_freq_list_2024-10-13.csv`
Original source data. Tab-separated, columns: `term`, `reading`, `frequency`, `kana_frequency`.

### `task1_top25k.csv`
Top 25,000 words by reading frequency. Two columns: `term`, `reading_frequency`.

### `task2_kana_higher.csv`
A filtered subset of the top 25,000 words where the kana frequency rank is higher (lower rank number) than the reading frequency rank. Four columns: `term`, `reading_frequency`, `kana_frequency`.

## Insight

Out of the top 25,000 words, ~765 terms (~3%) are encountered more often written in kana than in their kanji form. This is notable — it suggests these words, despite having a kanji spelling, are commonly written in hiragana or katakana in practice (e.g. 事 → こと, 物 → もの). These may be good candidates to learn in their kana form first.

## Scripts

`process.py` — generates `task1_top25k.csv` and `task2_kana_higher.csv` from the source file.
