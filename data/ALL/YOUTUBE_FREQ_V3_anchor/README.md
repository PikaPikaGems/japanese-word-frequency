# YOUTUBE_FREQ_V3 Anchor

Word frequency rankings anchored on **YouTube Frequency V3** — a frequency list built from YouTube Japanese video subtitles by MarvNC (Zetta, Vexxed, Anonymous contributors), representing contemporary conversational and informal Japanese.

## What this is

`consolidated.csv` lists the top 30,000 words by YouTube V3 frequency, with each word's rank across CEJC and 34 other sources as additional columns. `categorized.csv` maps those ranks to 5 vocabulary tiers.

Note: this is the largest anchor at 30,000 words (vs 25,000 for others).

## Why YouTube as an anchor

YouTube V3 captures real spoken Japanese as it appears online — a mix of conversational speech, commentary, vlogs, and educational content. It is broader than CEJC (which is lab-collected conversations) and more contemporary than subtitle corpora.

## Methodology

Same bidirectional kana/kanji lookup pipeline as other non-CEJC anchors. `-1` means absent; duplicates keep minimum rank.

## Columns

- `word` — surface form
- `YOUTUBE_FREQ_V3_rank` — rank in YouTube V3 corpus
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

- **14.9% zero-missing** across 28 checked sources — the highest of all non-CEJC anchors in absolute count (4,463 words).
- N≤3 threshold yields ~7,834 words — one of the largest high-confidence sets across all anchors.
- Top-500 words achieve **70.2% zero-missing** across all 28 sources — basic particles, core verbs, and high-frequency nouns appear universally.
- This anchor was used as the primary reference corpus for the coverage quality experiments (see `experiment/coverage_analysis/`).
- The morpheme-tokenization problem is most visible here: HERMITDAVE sources miss 24.8% of the top-1,000 YouTube words because verbs like 思う, 見る, できる don't exist as tokens in morpheme-split corpora.

## Regenerating

```bash
python data/ALL/experiment/data_generation/make_anchored.py
```
