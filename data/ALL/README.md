# ALL — Consolidated Word Frequency Rankings

This folder merges Japanese word frequency rankings from multiple sources into unified CSVs.

## Files

Data lives in anchor-specific subdirectories; generation scripts are in `___experiments0/data_generation/`.

| Path | Description |
|------|-------------|
| `___experiments0/data_generation/SCRIPT.py` | Generates `CEJC_anchor/consolidated.csv` from CEJC and RAW/___FILTERED sources |
| `___experiments0/data_generation/CATEGORIZED.py` | Generates `CEJC_anchor/categorized.csv` from `consolidated.csv` |
| `___experiments0/data_generation/make_anchored.py` | Generates consolidated + categorized for JPDB, ANIME_JDRAMA, NETFLIX, YOUTUBE_FREQ_V3 anchors |
| `CEJC_anchor/consolidated.csv` | 27,988 words × 65 columns (word + hiragana + katakana + 62 rank columns) |
| `CEJC_anchor/categorized.csv` | Same shape — rank values mapped to vocabulary tier categories |
| `{ANCHOR}_anchor/consolidated.csv` | Same structure for JPDB, ANIME_JDRAMA, NETFLIX, YOUTUBE_FREQ_V3 anchors |
| `{ANCHOR}_anchor/categorized.csv` | Same structure, tier-mapped |

## consolidated.csv

**Row order:** Sorted by CEJC `combined_rank` (as in `data/CEJC/CONSOLIDATED_UNIQUE.csv`). Other anchors are sorted by their own source ranking.

**Columns:**

| Column | Source | Description |
|--------|--------|-------------|
| `word` | — | — |
| `hiragana` | JPDBV2 / CEJC | Reading in hiragana. Sourced from JPDBV2 first; CEJC used as fallback. Pure-kana words use themselves as the reading. Empty if reading is unknown. |
| `katakana` | JPDBV2 / CEJC | Same reading converted to katakana. |
| `combined_rank` | CEJC overall | — |
| `small_talk_rank` | CEJC domain | — |
| `consultation_rank` | CEJC domain | — |
| `meeting_rank` | CEJC domain | — |
| `class_rank` | CEJC domain | — |
| `outdoors_rank` | CEJC domain | — |
| `school_rank` | CEJC domain | — |
| `transportation_rank` | CEJC domain | — |
| `public_commercial_rank` | CEJC domain | — |
| `home_rank` | CEJC domain | — |
| `indoors_rank` | CEJC domain | — |
| `workplace_rank` | CEJC domain | — |
| `male_rank` | CEJC gender | — |
| `female_rank` | CEJC gender | — |
| `ADNO` | RAW/___FILTERED/ADNO | Cleaned Japanese Wikipedia frequency list by adno (fork of IlyaSemenov) |
| `ANIME_JDRAMA` | RAW/___FILTERED/ANIME_JDRAMA | Anime & J-drama subtitle frequency from Shoui's collection |
| `AOZORA_BUNKO` | RAW/___FILTERED/AOZORA_BUNKO | Kanji/jukugo frequency from Aozora Bunko public-domain literature |
| `BCCWJ_LUW` | RAW/___FILTERED/BCCWJ_LUW | Balanced Corpus of Contemporary Written Japanese — Long Unit Word (toasted-nutbread) |
| `BCCWJ_SUW` | RAW/___FILTERED/BCCWJ_SUW | Balanced Corpus of Contemporary Written Japanese — Short Unit Word (toasted-nutbread) |
| `CC100` | RAW/___FILTERED/CC100 | CommonCrawl Japanese web text frequency (CC-100 dataset) |
| `CHRISKEMPSON` | RAW/___FILTERED/CHRISKEMPSON | Japanese subtitle word frequency by chriskempson |
| `DAVE_DOEBRICK` | RAW/___FILTERED/DAVE_DOEBRICK | Netflix Japanese subtitle frequency compiled by Dave Doebrick |
| `DD2_MIGAKU_NETFLIX` | RAW/___FILTERED/DD2_MIGAKU_NETFLIX | Migaku-format Netflix frequency list from Dave Doebrick's compilation |
| `DD2_MIGAKU_NOVELS` | RAW/___FILTERED/DD2_MIGAKU_NOVELS | Migaku-format novel 5k frequency list from Dave Doebrick's compilation |
| `DD2_MORPHMAN_NETFLIX` | RAW/___FILTERED/DD2_MORPHMAN_NETFLIX | Morphman-format Netflix frequency report (no names) from Dave Doebrick's compilation |
| `DD2_MORPHMAN_NOVELS` | RAW/___FILTERED/DD2_MORPHMAN_NOVELS | Morphman-format Japanese novels frequency list from Dave Doebrick's compilation |
| `DD2_MORPHMAN_SHONEN` | RAW/___FILTERED/DD2_MORPHMAN_SHONEN | Morphman-format shonen manga frequency report from Dave Doebrick's compilation |
| `DD2_MORPHMAN_SOL` | RAW/___FILTERED/DD2_MORPHMAN_SOL | Morphman-format slice-of-life frequency report from Dave Doebrick's compilation |
| `DD2_YOMICHAN_NOVELS` | RAW/___FILTERED/DD2_YOMICHAN_NOVELS | Yomichan-format novel 5k stars frequency list from Dave Doebrick's compilation |
| `DD2_YOMICHAN_SHONEN` | RAW/___FILTERED/DD2_YOMICHAN_SHONEN | Yomichan-format shonen top 100 frequency list from Dave Doebrick's compilation |
| `DD2_YOMICHAN_SHONEN_STARS` | RAW/___FILTERED/DD2_YOMICHAN_SHONEN_STARS | Yomichan-format shonen stars frequency list from Dave Doebrick's compilation |
| `DD2_YOMICHAN_SOL` | RAW/___FILTERED/DD2_YOMICHAN_SOL | Yomichan-format slice-of-life top 100 frequency list from Dave Doebrick's compilation |
| `DD2_YOMICHAN_VN` | RAW/___FILTERED/DD2_YOMICHAN_VN | Yomichan-format visual novel stars frequency list from Dave Doebrick's compilation |
| `HERMITDAVE_2016` | RAW/___FILTERED/HERMITDAVE_2016 | OpenSubtitles 2016 Japanese word frequency by hermitdave |
| `HERMITDAVE_2018` | RAW/___FILTERED/HERMITDAVE_2018 | OpenSubtitles 2018 Japanese word frequency by hermitdave |
| `HINGSTON` | RAW/___FILTERED/HINGSTON | Japanese internet word frequency by hingston (Leeds corpus) |
| `H_FREQ` | RAW/___FILTERED/H_FREQ | Adult (18+) Japanese content word frequency by Kuuube |
| `ILYASEMENOV` | RAW/___FILTERED/ILYASEMENOV | Japanese Wikipedia word frequency by IlyaSemenov |
| `INNOCENT_RANKED` | RAW/___FILTERED/INNOCENT_RANKED | Innocent Corpus Japanese novel frequency (ranked, MarvNC/yomitan) |
| `JITEN_ANIME` | RAW/___FILTERED/JITEN_ANIME | Anime word frequency from jiten.moe |
| `JLAB` | RAW/___FILTERED/JLAB | Anime word frequency from Japanese Like a Breeze |
| `JPDB` | RAW/___FILTERED/JPDB | Japanese entertainment media frequency from jpdb.io |
| `KOKUGOJITEN` | RAW/___FILTERED/KOKUGOJITEN | 国語辞典 Japanese monolingual dictionary frequency by Shoui |
| `MALTESAA_CSJ` | RAW/___FILTERED/MALTESAA_CSJ | Corpus of Spontaneous Japanese (CSJ) overall frequency by Maltesaa |
| `MALTESAA_CSJ_DOKWA_GAKKAI` | RAW/___FILTERED/MALTESAA_CSJ_DOKWA_GAKKAI | CSJ monologue sub-corpus — academic presentations (独話・学会) |
| `MALTESAA_CSJ_DOKWA_MOGI` | RAW/___FILTERED/MALTESAA_CSJ_DOKWA_MOGI | CSJ monologue sub-corpus — simulated speeches (独話・模擬) |
| `MALTESAA_CSJ_DOKWA_ROUDOKU` | RAW/___FILTERED/MALTESAA_CSJ_DOKWA_ROUDOKU | CSJ monologue sub-corpus — reading aloud (独話・朗読) |
| `MALTESAA_CSJ_DOKWA_SAIRO` | RAW/___FILTERED/MALTESAA_CSJ_DOKWA_SAIRO | CSJ monologue sub-corpus — re-reading (独話・再朗読) |
| `MALTESAA_CSJ_DOKWA_SONOTA` | RAW/___FILTERED/MALTESAA_CSJ_DOKWA_SONOTA | CSJ monologue sub-corpus — other (独話・その他) |
| `MALTESAA_CSJ_TAIKA_JIYU` | RAW/___FILTERED/MALTESAA_CSJ_TAIKA_JIYU | CSJ dialogue sub-corpus — free conversation (対話・自由) |
| `MALTESAA_CSJ_TAIKA_KADAI` | RAW/___FILTERED/MALTESAA_CSJ_TAIKA_KADAI | CSJ dialogue sub-corpus — task-based (対話・課題) |
| `MALTESAA_CSJ_TAIKA_MOGI` | RAW/___FILTERED/MALTESAA_CSJ_TAIKA_MOGI | CSJ dialogue sub-corpus — simulated (対話・模擬) |
| `MALTESAA_NWJC` | RAW/___FILTERED/MALTESAA_NWJC | NINJAL Web Japanese Corpus (NWJC) word frequency by Maltesaa |
| `MONODICTS` | RAW/___FILTERED/MONODICTS | Japanese monolingual dictionary frequency (jpDicts 206k) by Shoui |
| `NAROU` | RAW/___FILTERED/NAROU | 小説家になろう web novel frequency by Shoui/wareya |
| `NETFLIX` | RAW/___FILTERED/NETFLIX | Netflix Japanese subtitle frequency by Shoui |
| `NIER` | RAW/___FILTERED/NIER | Nier game series Japanese word frequency by Shoui |
| `NOVELS` | RAW/___FILTERED/NOVELS | Japanese novels frequency by Kuuube/MarvNC |
| `RSPEER` | data/RSPEER/top_25000_japanese.csv | Japanese word frequency from the rspeer/wordfreq library (multi-corpus aggregate) |
| `VN_FREQ` | RAW/___FILTERED/VN_FREQ | Visual novel Japanese word frequency by Shoui/wareya |
| `WIKIPEDIA_V2` | RAW/___FILTERED/WIKIPEDIA_V2 | Japanese Wikipedia word frequency v2 by Shoui/MarvNC |
| `YOUTUBE_FREQ` | RAW/___FILTERED/YOUTUBE_FREQ | YouTube Japanese video frequency by Shoui |
| `YOUTUBE_FREQ_V3` | RAW/___FILTERED/YOUTUBE_FREQ_V3 | YouTube Japanese video frequency v3 by MarvNC (Zetta, Vexxed, Anonymous) |

`-1` means the word was not found in that source.

## categorized.csv

Same columns as `consolidated.csv`, but each rank value is replaced with a vocabulary tier number:

| Value | Tier | Rank Range | Description |
|-------|------|-----------|-------------|
| `5` | basic | 1–1,800 | Foundational and essential vocabulary |
| `4` | common | 1,801–5,000 | Frequent in everyday speech and writing |
| `3` | fluent | 5,001–12,000 | Expansive vocabulary for natural expression |
| `2` | advanced | 12,001–25,000 | Formal, academic, technical or specialized |
| `1` | rare | 25,001+ or not in source | Archaic, obscure, uncommon, invalid, or absent |

## Regenerating

```bash
# CEJC anchor
python data/ALL/___experiments0/data_generation/SCRIPT.py       # produces CEJC_anchor/consolidated.csv
python data/ALL/___experiments0/data_generation/CATEGORIZED.py  # produces CEJC_anchor/categorized.csv

# Other anchors (JPDB, ANIME_JDRAMA, NETFLIX, YOUTUBE_FREQ_V3)
python data/ALL/___experiments0/data_generation/make_anchored.py

# BCCWJ_LUW, BCCWJ_SUW, CC100, RSPEER, WIKIPEDIA_V2 anchors
python data/ALL/___experiments1/data_generation/make_more_anchors.py
```

## Kana reading coverage

Reading lookup is built from two sources (280k entries combined):

| Source | Reading format | Priority |
|--------|---------------|----------|
| `data/JPDBV2/jpdb_v2.2_freq_list_2024-10-13.csv` | hiragana | primary |
| `data/CEJC/2_cejc_frequencylist_suw_token.tsv` | katakana | fallback |

Coverage after lookup + pure-kana fill (categorized and consolidated are identical):

| Anchor | Words | Missing reading | % missing |
|--------|-------|----------------|-----------|
| CEJC | 27,988 | 0 | 0.0% |
| JPDB | 24,231 | 0 | 0.0% |
| ANIME_JDRAMA | 25,000 | 2,636 | 10.5% |
| NETFLIX | 25,000 | 1,728 | 6.9% |
| YOUTUBE_FREQ_V3 | 25,000 | 1,426 | 5.7% |
| BCCWJ_LUW | 25,000 | 4,904 | 19.6% |
| BCCWJ_SUW | 25,000 | 349 | 1.4% |
| CC100 | 24,605 | 470 | 1.9% |
| RSPEER | 25,000 | 4,544 | 18.2% |
| WIKIPEDIA_V2 | 25,000 | 3,250 | 13.0% |

Remaining gaps are almost entirely conjugated verb forms (`会える`, `行ける`, `使える`) and proper nouns/names (`悟`, `宮近`, `中村`). Non-Japanese tokens are negligible (1 across all files: `々`, the kanji repetition mark).
