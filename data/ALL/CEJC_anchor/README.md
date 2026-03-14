# CEJC Anchor

Word frequency rankings anchored on the **CEJC (Corpus of Everyday Japanese Conversation)** — a large-scale spoken Japanese corpus collected by NINJAL using UniDic morphological analysis.

## What this is

`consolidated.csv` lists ~27,988 words in CEJC frequency order, with each word's rank across 35 other frequency sources as additional columns. `categorized.csv` maps those ranks to 5 vocabulary tiers.

**Row order:** Sorted by CEJC `combined_rank` (most frequent first).

## Why CEJC as an anchor

CEJC is the most authentic spoken-Japanese corpus available — real conversations across 11 domains (small talk, meetings, school, home, workplace, etc.) and stratified by speaker gender. It captures the actual vocabulary of everyday speech, not subtitles, novels, or web text.

Using CEJC as the backbone means the word list is ordered by how common words are in real spoken Japanese — making it particularly useful for learners focused on conversational fluency.

## Methodology

1. Word order comes from `data/CEJC/CONSOLIDATED_UNIQUE.csv` (CEJC `combined_rank`).
2. For each word, ranks are looked up across all 35 `___FILTERED` sources.
3. A kanji→kana fallback via JPDB v2 handles UniDic lemma mismatches (e.g., 其れ → それ). Without this, CEJC's kanji lemma forms would show -1 in nearly every other source.
4. `-1` means the word was not found in that source.
5. Duplicate word entries within a source keep the minimum (most frequent) rank.

## Columns

- `word` — the Japanese word (UniDic lemma form)
- `combined_rank`, `small_talk_rank`, `consultation_rank`, `meeting_rank`, `class_rank`, `outdoors_rank`, `school_rank`, `transportation_rank`, `public_commercial_rank`, `home_rank`, `indoors_rank`, `workplace_rank` — CEJC domain-specific ranks
- `male_rank`, `female_rank` — CEJC gender-stratified ranks
- One column per external source (35 total) — rank in that source, or -1 if absent

## Tier categories (`categorized.csv`)

| Value | Tier | Rank range |
|-------|------|-----------|
| 5 | basic | 1–1,000 |
| 4 | common | 1,001–4,000 |
| 3 | fluent | 4,001–10,000 |
| 2 | advanced | 10,001–25,000 |
| 1 | rare | 25,001+ or absent |

## Key insights

- **~12.4% of CEJC words have zero missing ranks** (across 28 reliable sources after excluding 7 structurally broken ones). These are the most universally attested words across all corpora.
- **7 sources are excluded from quality checks** due to structural incompatibility: AOZORA_BUNKO (kanji-only), NIER (single game, ~10k words), ILYASEMENOV (HTML entities, Wikipedia bias), DD2_MIGAKU_NOVELS (curated learner deck), HERMITDAVE_2016/2018 (morpheme-split tokenization), JPDB (anime/game register misses general vocabulary like 男性, 企業).
- **N≤3 threshold** (missing from at most 3 of the 28 checked sources) yields ~6,047 high-confidence words — a practical working set for vocabulary study.
- CEJC's UniDic lemma forms (其れ、為る、此れ) are distinct from the surface hiragana forms (それ、する、これ) used by other sources; both exist as separate entries in CEJC.

## Regenerating

```bash
python data/ALL/experiment/data_generation/SCRIPT.py
```
