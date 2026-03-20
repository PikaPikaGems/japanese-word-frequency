## Datasets

### ALL — Consolidated Rankings

`data/ALL/`

The primary output of this repo. Each `consolidated.csv` is a matrix of **words × rank columns**, one column per frequency source. The **anchor** is the source whose word list defines the rows — every word in the anchor appears as a row, and each column shows that word's rank in the other sources (`-1` if absent). Different anchors produce different matrices because each source has different vocabulary coverage and tokenization. Ten anchor variants exist: CEJC, BCCWJ_LUW, BCCWJ_SUW, CC100, RSPEER, WIKIPEDIA_V2, ANIME_JDRAMA, NETFLIX, YOUTUBE_FREQ_V3, and JPDB. Analysis scripts and reports in `___experiments0/` and `___experiments1/`:
Please see: [CONSOLIDATED_CSV_REFERENCEV1.md](CONSOLIDATED_CSV_REFERENCEV1.md) for more details.

### CEJC — Everyday Spoken Japanese

`data/CEJC/`

Based on 200 hours of recorded spontaneous speech. Rich demographic breakdown by conversation domain, gender, and age group.

- **`CONSOLIDATED.csv`** — 29,534 entries x 36 rank columns (domain + demographic breakdowns)
- **`CONSOLIDATED_UNIQUE.csv`** — 27,988 deduplicated entries
- insight reports in `insights/`
- analysis scripts in `scripts/`

See [data/CEJC/README.md](data/CEJC/README.md) for dataset details.

### JPDBV2 — Entertainment Media

`data/JPDBV2/`

Frequency data from jpdb.io, sourced from light novels, visual novels, anime, J-drama, and web novels.

- **`task1_top25k.csv`** — Top 25,000 words by reading frequency
- **`task2_kana_higher.csv`** — ~765 words where kana frequency exceeds kanji frequency (~3% of top 25k)
- **`process.py`** — Generates both files from the raw source CSV

See [data/JPDBV2/README.md](data/JPDBV2/README.md) for details.

### RSPEER — wordfreq Library

`data/RSPEER/`

Generated from the [rspeer/wordfreq](https://github.com/rspeer/wordfreq) Python library, which aggregates multiple large corpora.

- **`top_25000_japanese.csv`** — 25,000 words with `frequency` and `zipf_frequency` columns
- 6 plotting scripts for distribution analysis (Zipf, coverage curve, script type, word length, cross-dataset comparison)

See [data/RSPEER/INSIGHTS.md](data/RSPEER/INSIGHTS.md) for analysis results.

### RAW/\_\_\_FILTERED — 60+ Source Datasets + RSPEER

`data/RAW/___FILTERED/`

Each subdirectory contains a standardized `DATA.csv` (columns: `WORD`, `FREQUENCY_RANKING`, top 25k entries) and a `README.md` describing the source. `RSPEER` (`data/RSPEER/top_25000_japanese.csv`) is included as an additional source; its rank is derived from row position (row 1 = rank 1, sorted by descending zipf frequency).

| Source                     | Type                                                |
| -------------------------- | --------------------------------------------------- |
| ADNO                       | Wikipedia (cleaned)                                 |
| ANIME_JDRAMA               | Anime & J-drama subtitles                           |
| AOZORA_BUNKO               | Public domain literature                            |
| BCCWJ_LUW                  | Balanced written corpus — Long Unit Word (NINJAL)   |
| BCCWJ_SUW                  | Balanced written corpus — Short Unit Word (NINJAL)  |
| CC100                      | Web text (Common Crawl)                             |
| CHRISKEMPSON               | Japanese subtitles                                  |
| DAVE_DOEBRICK              | Netflix subtitles (Dave Doebrick, full report)      |
| DD2_MIGAKU_NETFLIX         | Netflix subtitles (Migaku dictionary format)        |
| DD2_MORPHMAN_NETFLIX       | Netflix subtitles (Morphman report, no names)       |
| DD2_MORPHMAN_NOVELS        | Novel corpus (Morphman report)                      |
| DD2_MORPHMAN_SHONEN        | Shonen anime/manga (Morphman report)                |
| DD2_MORPHMAN_SOL           | Slice of Life anime (Morphman report)               |
| DD2_YOMICHAN_NOVELS        | Novel corpus (Yomichan Stars format)                |
| DD2_YOMICHAN_SHONEN        | Shonen anime/manga (Yomichan integer rank format)   |
| DD2_YOMICHAN_SHONEN_STARS  | Shonen anime/manga (Yomichan Stars format)          |
| DD2_YOMICHAN_SOL           | Slice of Life anime (Yomichan integer rank format)  |
| DD2_YOMICHAN_VN            | Visual novels (Yomichan Stars format)               |
| HERMITDAVE_2016            | Subtitle corpus (2016)                              |
| HERMITDAVE_2018            | Subtitle corpus (2018)                              |
| HINGSTON                   | Japanese internet word frequency (Leeds corpus)     |
| HLORENZI_ANIMEDRAMA        | Anime & drama subtitle rankings (hlorenzi/jisho-open) |
| HLORENZI_WIKIPEDIA         | Wikipedia word rankings (hlorenzi/jisho-open)       |
| H_FREQ                     | Adult content corpus                                |
| ILYASEMENOV                | Wikipedia word frequency                            |
| INNOCENT_RANKED            | Innocent Corpus (novels)                            |
| JITEN_ANIME                | Anime-focused frequency (jiten.moe, Yomitan JSON)   |
| JITEN_ANIME_V2             | Anime-focused frequency (jiten.moe, CSV format)     |
| JITEN_AUDIO                | Audio media frequency (jiten.moe)                   |
| JITEN_DRAMA                | Japanese drama frequency (jiten.moe)                |
| JITEN_GLOBAL               | All-media combined frequency (jiten.moe)            |
| JITEN_MANGA                | Manga frequency (jiten.moe)                         |
| JITEN_MOVIE                | Movie frequency (jiten.moe)                         |
| JITEN_NON_FICTION          | Non-fiction media frequency (jiten.moe)             |
| JITEN_NOVEL                | Novel frequency (jiten.moe)                         |
| JITEN_VIDEO_GAME           | Video game frequency (jiten.moe)                    |
| JITEN_VISUAL_NOVEL         | Visual novel frequency (jiten.moe)                  |
| JITEN_WEB_NOVEL            | Web novel frequency (jiten.moe)                     |
| JLAB                       | Anime frequency (Japanese Like a Breeze)            |
| JPDB                       | Entertainment media (jpdb.io)                       |
| KUUUUBE_JMDICT_FREQ        | JMdict newspaper frequency (Kuuube)                 |
| MALTESAA_CSJ               | Corpus of Spontaneous Japanese (CSJ), overall       |
| MALTESAA_CSJ_DOKWA_GAKKAI  | CSJ monologue — academic presentations (独話・学会) |
| MALTESAA_CSJ_DOKWA_MOGI    | CSJ monologue — simulated speeches (独話・模擬)     |
| MALTESAA_CSJ_DOKWA_ROUDOKU | CSJ monologue — reading aloud (独話・朗読)          |
| MALTESAA_CSJ_DOKWA_SAIRO   | CSJ monologue — re-reading (独話・再朗読)           |
| MALTESAA_CSJ_DOKWA_SONOTA  | CSJ monologue — other (独話・その他)                |
| MALTESAA_CSJ_TAIKA_JIYU    | CSJ dialogue — free conversation (対話・自由)       |
| MALTESAA_CSJ_TAIKA_KADAI   | CSJ dialogue — task-based (対話・課題)              |
| MALTESAA_CSJ_TAIKA_MOGI    | CSJ dialogue — simulated (対話・模擬)               |
| MALTESAA_NWJC              | NINJAL Web Japanese Corpus (NWJC)                   |
| NAROU                      | Web novels (Narou)                                  |
| NETFLIX                    | Netflix subtitle frequency                          |
| NIER                       | NieR game script frequency                          |
| NOVELS                     | Novel corpus                                        |
| RSPEER                     | rspeer/wordfreq multi-corpus aggregate              |
| VN_FREQ                    | Visual novel corpus                                 |
| WIKIPEDIA_V2               | Wikipedia (v2)                                      |
| YOUTUBE_FREQ               | YouTube subtitle frequency                          |
| YOUTUBE_FREQ_V3            | YouTube subtitle frequency (v3, top 25k)            |

Note: `DD2_*` sources are from Dave Doebrick's Frequency List Compilation (MIGAKU, MORPHMAN, and YOMICHAN dictionary formats). Three were removed as duplicates: `DD2_YOMICHAN_NETFLIX` (= `NETFLIX`), `DD2_MIGAKU_SOL` (= `DD2_YOMICHAN_SOL`), `DD2_MIGAKU_SHONEN` (= `DD2_YOMICHAN_SHONEN_STARS`). `MALTESAA_*` sources are from Maltesaa's CSJ and NWJC yomitan frequency dictionaries.

See [notes/consolidated-reference-verbose.md](notes/consolidated-reference-verbose.md) for detailed descriptions of all sources.
