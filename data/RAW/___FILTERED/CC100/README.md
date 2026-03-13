# CC100 — CommonCrawl Japanese Word Frequency

## Source
- **Yomitan dict (MarvNC collection):** https://github.com/MarvNC/yomitan-dictionaries#cc100
- **CC-100 dataset:** https://data.statmt.org/cc-100/
- **Author:** xydustc (developer of arujisho)

## Description
Frequency list derived from the CC-100 dataset — a high-quality monolingual web text dataset filtered from CommonCrawl, used to train XLM-R. The Japanese portion contains ~70GB of text.

Tokenized using **SudachiPy (Mode B)** and **fugashi (MeCab wrapper)**, then filtered using monolingual dictionaries, resulting in ~160k unique word entries.

Formal/written language tends to rank higher compared to fiction-oriented lists. Recommended in community guides as a good sort dictionary due to broad, well-differentiated readings.

**Dataset released:** ~2020

## Format (Yomitan JSON)
`term_meta_bank_1.json` — array of `[word, "freq", {"reading": reading, "frequency": rank}]` entries. Single file, ~160k entries.

## DATA.csv
Top 25,000 words by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
