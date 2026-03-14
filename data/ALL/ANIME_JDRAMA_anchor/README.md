# ANIME_JDRAMA Anchor

Word frequency rankings anchored on **Anime + J-Drama subtitles** — a frequency list from Shoui's collection of anime and Japanese drama subtitle files.

## What this is

`consolidated.csv` lists the top 25,000 words by anime/J-drama frequency, with each word's rank across CEJC and 34 other sources as additional columns. `categorized.csv` maps those ranks to 5 vocabulary tiers.

## Why Anime/J-Drama as an anchor

Anime and J-drama subtitles are among the most common immersion material for Japanese learners. This corpus reflects the vocabulary actually encountered when watching Japanese media — a mix of conversational speech, dramatic dialogue, and genre-specific vocabulary.

## Methodology

Same bidirectional kana/kanji lookup pipeline as other non-CEJC anchors. `-1` means absent; duplicates keep minimum rank.

## Columns

- `word` — surface form
- `ANIME_JDRAMA_rank` — rank in the anime/J-drama corpus
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

- **17.5% zero-missing** across 28 checked sources (4,377 words) — tied with NETFLIX for highest zero-missing rate among all anchors.
- N≤3 threshold yields ~7,721 high-confidence words.
- Strong alignment with NETFLIX anchor — both are subtitle-based corpora covering similar registers. Coverage patterns are nearly identical between them.
- Anime-specific vocabulary (character archetypes, fantasy/sci-fi terms) will rank higher here than in general spoken corpora.

## Regenerating

```bash
python data/ALL/experiment/data_generation/make_anchored.py
```
