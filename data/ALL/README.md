# ALL — Consolidated Word Frequency Rankings

This folder merges Japanese word frequency rankings from multiple sources into unified CSVs.

## Files

| File | Description |
|------|-------------|
| `SCRIPT.py` | Generates `consolidated.csv` from CEJC and RAW/___FILTERED sources |
| `CATEGORIZED.py` | Generates `categorized.csv` from `consolidated.csv` |
| `consolidated.csv` | 27,988 words × 36 rank columns (word order from CEJC CONSOLIDATED_UNIQUE) |
| `categorized.csv` | Same shape — rank values mapped to vocabulary tier categories |

## consolidated.csv

**Row order:** Sorted by CEJC `combined_rank` (as in `data/CEJC/CONSOLIDATED_UNIQUE.csv`).

**Columns:**

| Column | Source |
|--------|--------|
| `word` | — |
| `combined_rank` | CEJC overall |
| `small_talk_rank` | CEJC domain |
| `consultation_rank` | CEJC domain |
| `meeting_rank` | CEJC domain |
| `class_rank` | CEJC domain |
| `outdoors_rank` | CEJC domain |
| `school_rank` | CEJC domain |
| `transportation_rank` | CEJC domain |
| `public_commercial_rank` | CEJC domain |
| `home_rank` | CEJC domain |
| `indoors_rank` | CEJC domain |
| `workplace_rank` | CEJC domain |
| `male_rank` | CEJC gender |
| `female_rank` | CEJC gender |
| `ADNO` | RAW/___FILTERED/ADNO |
| `ANIME_JDRAMA` | RAW/___FILTERED/ANIME_JDRAMA |
| `AOZORA_BUNKO` | RAW/___FILTERED/AOZORA_BUNKO |
| `BCCWJ` | RAW/___FILTERED/BCCWJ |
| `CC100` | RAW/___FILTERED/CC100 |
| `CHRISKEMPSON` | RAW/___FILTERED/CHRISKEMPSON |
| `DAVE_DOEBRICK` | RAW/___FILTERED/DAVE_DOEBRICK |
| `HERMITDAVE_2016` | RAW/___FILTERED/HERMITDAVE_2016 |
| `HERMITDAVE_2018` | RAW/___FILTERED/HERMITDAVE_2018 |
| `H_FREQ` | RAW/___FILTERED/H_FREQ |
| `ILYASEMENOV` | RAW/___FILTERED/ILYASEMENOV |
| `INNOCENT_RANKED` | RAW/___FILTERED/INNOCENT_RANKED |
| `JITEN_ANIME` | RAW/___FILTERED/JITEN_ANIME |
| `JPDB` | RAW/___FILTERED/JPDB |
| `KOKUGOJITEN` | RAW/___FILTERED/KOKUGOJITEN |
| `MONODICTS` | RAW/___FILTERED/MONODICTS |
| `NAROU` | RAW/___FILTERED/NAROU |
| `NETFLIX` | RAW/___FILTERED/NETFLIX |
| `NOVELS` | RAW/___FILTERED/NOVELS |
| `VN_FREQ` | RAW/___FILTERED/VN_FREQ |
| `WIKIPEDIA_V2` | RAW/___FILTERED/WIKIPEDIA_V2 |
| `YOUTUBE_FREQ` | RAW/___FILTERED/YOUTUBE_FREQ |

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
