# NETFLIX Anchor

Word frequency rankings anchored on **Netflix subtitles** — a frequency list compiled by Shoui from Japanese Netflix subtitle files.

## What this is

`consolidated.csv` lists the top 25,000 words by Netflix subtitle frequency, with each word's rank across CEJC and 34 other sources as additional columns. `categorized.csv` maps those ranks to 5 vocabulary tiers.

## Why Netflix as an anchor

Netflix Japanese content spans a wide range of genres — drama, documentary, variety, anime, film. The subtitle corpus captures contemporary spoken Japanese across more diverse contexts than a single genre source. It sits between CEJC (controlled spoken lab data) and anime-only corpora in terms of register range.

## Methodology

Same bidirectional kana/kanji lookup pipeline as other non-CEJC anchors. `-1` means absent; duplicates keep minimum rank.

Note: `DD2_MIGAKU_NETFLIX` and `DD2_MORPHMAN_NETFLIX` are distinct sources included as separate columns — they are Migaku/Morphman-formatted versions of a different Netflix compilation by Dave Doebrick, not duplicates of this anchor.

## Columns

- `word` — surface form
- `NETFLIX_rank` — rank in Netflix subtitle corpus
- `CEJC_rank` — CEJC combined spoken frequency rank
- One column per other source (34 total)

## Tier categories (`categorized.csv`)

| Value | Tier     | Rank range        |
| ----- | -------- | ----------------- |
| 5     | basic    | 1–1,000           |
| 4     | common   | 1,001–4,000       |
| 3     | fluent   | 4,001–10,000      |
| 2     | advanced | 10,001–25,000     |
| 1     | rare     | 25,001+ or absent |

## Regenerating

```bash
python data/ALL/experiment/data_generation/make_anchored.py
```
