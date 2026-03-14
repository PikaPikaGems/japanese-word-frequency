# Duplicate Column Audit

Script: [`check_duplicates.py`](check_duplicates.py)

## How duplicates are detected

Two source columns are considered exact duplicates if they have identical `FREQUENCY_RANKING` values for every word (including `-1` / missing entries). The `word` column and all CEJC-derived `*_rank` columns are excluded from this check.

## Resolution strategy (if duplicates are found)

1. Prefer the **non-`DD2_`** column (original/established dataset) over the Dave Doebrick Part 2 variant.
2. Among ties, keep the **alphabetically first** column name.
3. Remove the losers from `consolidated.csv` and delete their `___FILTERED/<name>/` directories.

## Audit results

| Date | Source columns checked | Duplicate groups found | Columns removed |
|------|----------------------|----------------------|-----------------|
| 2026-03-14 (prior session) | 38 | 3 | `DD2_YOMICHAN_NETFLIX`, `DD2_MIGAKU_SOL`, `DD2_MIGAKU_SHONEN` |
| 2026-03-14 | 35 | 0 | none |

### Prior deduplication (prior session, not committed to git)

| Removed | Kept | Reason |
|---------|------|--------|
| `DD2_YOMICHAN_NETFLIX` | `NETFLIX` | Identical rankings; kept the original established source |
| `DD2_MIGAKU_SOL` | `DD2_YOMICHAN_SOL` | Identical rankings; kept YOMICHAN version (preferred) |
| `DD2_MIGAKU_SHONEN` | `DD2_YOMICHAN_SHONEN_STARS` | Identical rankings; kept YOMICHAN version (preferred) |

Their `___FILTERED/<name>/` directories were also deleted. Running the script again confirms no further duplicates.

## Source columns checked (as of 2026-03-14)

| Column | Origin |
|--------|--------|
| `ADNO` | |
| `ANIME_JDRAMA` | |
| `AOZORA_BUNKO` | |
| `BCCWJ` | |
| `CC100` | |
| `CHRISKEMPSON` | |
| `DAVE_DOEBRICK` | |
| `DD2_MIGAKU_NETFLIX` | Dave Doebrick Part 2 — Migaku Netflix |
| `DD2_MIGAKU_NOVELS` | Dave Doebrick Part 2 — Migaku Novels 5k |
| `DD2_MORPHMAN_NETFLIX` | Dave Doebrick Part 2 — Morphman Netflix (no names) |
| `DD2_MORPHMAN_NOVELS` | Dave Doebrick Part 2 — Morphman Japanese Novels |
| `DD2_MORPHMAN_SHONEN` | Dave Doebrick Part 2 — Morphman Shonen Manga |
| `DD2_MORPHMAN_SOL` | Dave Doebrick Part 2 — Morphman Slice-of-Life |
| `DD2_YOMICHAN_NOVELS` | Dave Doebrick Part 2 — Yomichan Novels 5k Stars |
| `DD2_YOMICHAN_SHONEN` | Dave Doebrick Part 2 — Yomichan Shonen Top 100 |
| `DD2_YOMICHAN_SHONEN_STARS` | Dave Doebrick Part 2 — Yomichan Shonen Stars |
| `DD2_YOMICHAN_SOL` | Dave Doebrick Part 2 — Yomichan SoL Top 100 |
| `DD2_YOMICHAN_VN` | Dave Doebrick Part 2 — Yomichan Visual Novel Stars |
| `HERMITDAVE_2016` | |
| `HERMITDAVE_2018` | |
| `H_FREQ` | |
| `ILYASEMENOV` | |
| `INNOCENT_RANKED` | |
| `JITEN_ANIME` | |
| `JPDB` | |
| `KOKUGOJITEN` | |
| `MONODICTS` | |
| `NAROU` | |
| `NETFLIX` | |
| `NIER` | |
| `NOVELS` | |
| `VN_FREQ` | |
| `WIKIPEDIA_V2` | |
| `YOUTUBE_FREQ` | |
| `YOUTUBE_FREQ_V3` | |
