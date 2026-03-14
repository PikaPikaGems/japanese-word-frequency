# ALL — Consolidated Word Frequency Rankings

This folder merges Japanese word frequency rankings from multiple sources into unified CSVs.

## Files

| File | Description |
|------|-------------|
| `SCRIPT.py` | Generates `consolidated.csv` from CEJC and RAW/___FILTERED sources |
| `CATEGORIZED.py` | Generates `categorized.csv` from `consolidated.csv` |
| `consolidated.csv` | 27,988 words × 49 rank columns (word order from CEJC CONSOLIDATED_UNIQUE) |
| `categorized.csv` | Same shape — rank values mapped to vocabulary tier categories |

## consolidated.csv

**Row order:** Sorted by CEJC `combined_rank` (as in `data/CEJC/CONSOLIDATED_UNIQUE.csv`).

**Columns:**

| Column | Source | Description |
|--------|--------|-------------|
| `word` | — | — |
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
| `BCCWJ` | RAW/___FILTERED/BCCWJ | Balanced Corpus of Contemporary Written Japanese (Kuuube/yomitan) |
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
| `H_FREQ` | RAW/___FILTERED/H_FREQ | Adult (18+) Japanese content word frequency by Kuuube |
| `ILYASEMENOV` | RAW/___FILTERED/ILYASEMENOV | Japanese Wikipedia word frequency by IlyaSemenov |
| `INNOCENT_RANKED` | RAW/___FILTERED/INNOCENT_RANKED | Innocent Corpus Japanese novel frequency (ranked, MarvNC/yomitan) |
| `JITEN_ANIME` | RAW/___FILTERED/JITEN_ANIME | Anime word frequency from jiten.moe |
| `JPDB` | RAW/___FILTERED/JPDB | Japanese entertainment media frequency from jpdb.io |
| `KOKUGOJITEN` | RAW/___FILTERED/KOKUGOJITEN | 国語辞典 Japanese monolingual dictionary frequency by Shoui |
| `MONODICTS` | RAW/___FILTERED/MONODICTS | Japanese monolingual dictionary frequency (jpDicts 206k) by Shoui |
| `NAROU` | RAW/___FILTERED/NAROU | 小説家になろう web novel frequency by Shoui/wareya |
| `NETFLIX` | RAW/___FILTERED/NETFLIX | Netflix Japanese subtitle frequency by Shoui |
| `NIER` | RAW/___FILTERED/NIER | Nier game series Japanese word frequency by Shoui |
| `NOVELS` | RAW/___FILTERED/NOVELS | Japanese novels frequency by Kuuube/MarvNC |
| `VN_FREQ` | RAW/___FILTERED/VN_FREQ | Visual novel Japanese word frequency by Shoui/wareya |
| `WIKIPEDIA_V2` | RAW/___FILTERED/WIKIPEDIA_V2 | Japanese Wikipedia word frequency v2 by Shoui/MarvNC |
| `YOUTUBE_FREQ` | RAW/___FILTERED/YOUTUBE_FREQ | YouTube Japanese video frequency by Shoui |
| `YOUTUBE_FREQ_V3` | RAW/___FILTERED/YOUTUBE_FREQ_V3 | YouTube Japanese video frequency v3 by MarvNC (Zetta, Vexxed, Anonymous) |

`-1` means the word was not found in that source.

## categorized.csv

Same columns as `consolidated.csv`, but each rank value is replaced with a vocabulary tier number:

| Value | Tier | Rank Range | Description |
|-------|------|-----------|-------------|
| `5` | basic | 1–1,000 | Foundational and essential vocabulary |
| `4` | common | 1,001–4,000 | Frequent in everyday speech and writing |
| `3` | fluent | 4,001–10,000 | Expansive vocabulary for natural expression |
| `2` | advanced | 10,001–25,000 | Formal, academic, technical or specialized |
| `1` | rare | 25,001+ or not in source | Archaic, obscure, uncommon, invalid, or absent |

## Regenerating

```bash
python data/ALL/SCRIPT.py       # produces consolidated.csv
python data/ALL/CATEGORIZED.py  # produces categorized.csv
```
