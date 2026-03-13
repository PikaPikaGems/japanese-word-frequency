# MONODICTS — Japanese Monolingual Dictionary Frequency (jpDicts 206k)

## Source
- **Shoui collection:** https://anacreondjt.gitlab.io/docs/freq/
- **MarvNC collection:** https://github.com/MarvNC/yomitan-dictionaries

## Description
Frequency list derived from multiple major Japanese monolingual dictionaries. Contains ~206k unique word entries.

**Source dictionaries:**
- ハイブリッド新辞林 v2
- 故事ことわざの辞典
- 漢字源
- 精選版 日本国語大辞典
- 新明解四字熟語辞典
- 学研 四字熟語辞典
- 実用日本語表現辞典
- 旺文社国語辞典 第十一版
- 大辞林 第三版
- デジタル大辞泉
- 岩波国語辞典 第六版
- 広辞苑 第六版

This represents vocabulary covered by mainstream Japanese dictionaries, which can serve as a useful filter for "real" words (as opposed to names, neologisms, etc.).

## Format (Yomitan JSON)
Single `term_meta_bank_1.json` — each entry: `[word, "freq", rank]` (integer rank, 1-indexed).

## DATA.csv
Top 25,000 words by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
