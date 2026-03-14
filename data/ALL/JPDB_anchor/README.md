# JPDB Anchor

Word frequency rankings anchored on **JPDB** — a frequency list derived from jpdb.io's corpus of anime, manga, visual novels, and games.

## What this is

`consolidated.csv` lists the top 25,000 words by JPDB frequency, with each word's rank across CEJC and 34 other sources as additional columns. `categorized.csv` maps those ranks to 5 vocabulary tiers.

## Why JPDB as an anchor

JPDB is widely used in the Japanese learner community as a reference for media-consumption vocabulary (anime, games, visual novels). Anchoring on JPDB gives a word list ordered for learners focused on that media register.

## Methodology

Same pipeline as CEJC anchor, with bidirectional kanji/kana lookup:
- kanji anchor words → look up kana-keyed sources via JPDB v2 reading map
- kana anchor words → look up CEJC's kanji lemma entries
- `-1` means absent from that source
- Duplicate entries within a source keep minimum (most frequent) rank

## Columns

- `word` — surface form from JPDB source
- `JPDB_rank` — rank in JPDB corpus (1 = most frequent)
- `CEJC_rank` — CEJC combined spoken frequency rank
- One column per other source (34 total)

## Tier categories (`categorized.csv`)

| Value | Tier | Rank range |
|-------|------|-----------|
| 5 | basic | 1–1,000 |
| 4 | common | 1,001–4,000 |
| 3 | fluent | 4,001–10,000 |
| 2 | advanced | 10,001–25,000 |
| 1 | rare | 25,001+ or absent |

## Key insights

- **JPDB itself is excluded from coverage quality checks** for other anchors. Its anime/game corpus systematically misses real-world vocabulary: 男性 (man, YOUTUBE rank 1,100) is rank 180,271 in JPDB; 企業 (company) is entirely absent. This is a register mismatch, not a data quality issue.
- **Only ~10.5% zero-missing** at N=0 (vs 14–18% for other anchors) — JPDB's domain specificity means fewer words are covered by all sources.
- N≤3 threshold yields ~2,920 high-confidence words — fewer than other anchors due to JPDB's narrower domain.
- Best used when the learning goal is specifically anime/game/visual novel vocabulary.

## Regenerating

```bash
python data/ALL/experiment/data_generation/make_anchored.py
```
