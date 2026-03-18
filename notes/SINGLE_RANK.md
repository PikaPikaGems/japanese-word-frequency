# Single Rank Algorithm

**Output:** `data/ALL/RIRIKKU_CONSOLIDATED.csv`
**Script:** `data/ALL/___experiments1/data_generation/make_ririkku.py`

---

## Use Case

This ranking is designed for **ririkku.com**, a Japanese lyric immersion app. Users encounter Japanese through song lyrics — a register that mixes colloquial spoken language, emotional/poetic vocabulary, and media-adjacent terms (anime, J-pop, drama). The goal of the rank is to answer: **how important is this word for a learner to know?**

A word is important if it appears frequently in _any_ domain that meaningfully overlaps with the vocabulary a learner will encounter in lyrics and related Japanese media.

---

## Algorithm

For each word:

1. Collect its rank from each **included source** (see below). Ignore `-1` (absent / outside top-25k).
2. Require the word to appear in **at least 3 included sources**. If it appears in fewer, treat it as unranked.
3. Take the **minimum rank** across those sources (lowest number = highest frequency = best rank).

```
single_rank(word) =
  sources = [rank for rank in included_sources if rank != -1]
  if len(sources) < 3: return UNRANKED
  return min(sources)
```

---

## Why Minimum (Not Mean or Median)?

- **Minimum = best-case rank**: if _any_ shortlisted source considers this word very common, it gets a good rank.
- For a lyric app, this is the right signal. A word that's very frequent in anime/drama subtitles but only middling in web text is still a high-priority word for a learner — minimum surfaces it appropriately.
- **Mean/median** would dilute domain-specific vocabulary. A lyric-relevant word ranked #200 in ANIME_JDRAMA but #8000 in Wikipedia would land around #4000 — burying it unfairly.
- The **2-source threshold** prevents a single outlier source from inflating a word's rank. It requires at least minimal cross-source validation.

---

## Included Sources

These are the shortlisted datasets from `dataset-catalog.md` that are included in the minimum rank calculation.

| Column ID              | Rationale                                                                                                                                                                                                                            |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `RSPEER`               | Multi-source aggregate (subtitles, web, Twitter/Reddit, books, news). Robust baseline.                                                                                                                                               |
| `cejc_combined_rank`   | Everyday spoken Japanese. Captures colloquial vocabulary common in lyrics.                                                                                                                                                           |
| `cejc_small_talk_rank` | Casual small talk — the spoken register closest to lyric language.                                                                                                                                                                   |
| `BCCWJ_LUW`            | Authoritative written Japanese. Compound-word tokenization; top ranks are content words, not particles.                                                                                                                              |
| `CC100`                | Broad contemporary web Japanese (~2020). Strong overlap with YOUTUBE_FREQ_V3 (~75%); well-differentiated rankings.                                                                                                                   |
| `MALTESAA_NWJC`        | Web Japanese corpus (~25.8B tokens). Broad informal written coverage.                                                                                                                                                                |
| `JITEN_GLOBAL`         | All jiten.moe media combined. Actively maintained; covers anime, manga, VN, novels, games.                                                                                                                                           |
| `JITEN_ANIME_V2`       | Anime-specific frequency. Directly relevant to anime song vocabulary. Most recent jiten.moe export.                                                                                                                                  |
| `ANIME_JDRAMA`         | Anime + J-drama subtitles. Widely cited in the immersion community. Close register to lyrics.                                                                                                                                        |
| `YOUTUBE_FREQ_V3`      | Manually transcribed YouTube across 16 spoken domains. Spoken Japanese with broad domain coverage.                                                                                                                                   |
| `NETFLIX`              | Netflix Japan subtitles (anime + drama + live-action). Broad subtitle coverage.                                                                                                                                                      |
| `DD2_MORPHMAN_NETFLIX` | Netflix subtitles, proper names excluded, cleaner lemmatization. Complements `NETFLIX`.                                                                                                                                              |
| `WIKIPEDIA_V2`         | Wikipedia frequency (~850k source entries). Broad written coverage; helps anchor rarer content words.                                                                                                                                |
| `ADNO`                 | Wikipedia (Oct 2022), carefully filtered. Complements `WIKIPEDIA_V2`.                                                                                                                                                                |
| `DD2_MORPHMAN_SOL`     | Slice-of-Life anime. Consistent lemmatization; recommended SOL pick.                                                                                                                                                                 |
| `BCCWJ_SUW`            | Same BCCWJ corpus, Short Unit Word tokenization. Top ranks are dominated by particles and auxiliaries, but those are excluded from the vocabulary list anyway — for content words that do appear, SUW provides an additional signal. |

---

## Excluded Sources (and Why)

| Column ID      | Reason Excluded                                                                                                                  |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `MALTESAA_CSJ` | Corpus of Spontaneous Japanese — primarily formal academic monologues and conference presentations. Register is far from lyrics. |

### Note on CEJC Lemma Forms

CEJC uses UniDic lemma forms (e.g. 為る for する, 其れ for それ). This is fine for our purposes: we rank the **word** (dictionary/lemma concept), not a specific written form. Each word entry on ririkku.com displays all forms it can appear in, so the lemma-based rank from CEJC feeds correctly into the algorithm.

---

## Output Summary (RIRIKKU_CONSOLIDATED.csv)

| Stat                         | Count  |
| ---------------------------- | ------ |
| Union word list (total rows) | 92,092 |
| Ranked (≥3 sources)          | 43,060 |
| Unranked / RARE (<3 sources) | 49,032 |

**Category breakdown of ranked words** (using same tier thresholds as `CATEGORIZED.py`):

| Tier     | Rank range    | Word count |
| -------- | ------------- | ---------- |
| BASIC    | 1–1,800       | 7,271      |
| COMMON   | 1,801–5,000   | 9,338      |
| FLUENT   | 5,001–12,000  | 16,787     |
| ADVANCED | 12,001–25,000 | 9,664      |

> **Note on inflated BASIC:** because RIRIKKU*RANK uses the \_minimum* across 16 sources, a word only needs to be top-1k in _one_ of those sources to land in BASIC. The ≥3 source threshold provides meaningful cross-validation while preserving domain-specific lyric vocabulary — words appearing in only 1–2 sources are treated as RARE. The full list is a backend reference; users only see ranks for words that appear in lyric content.

### Threshold selection

We evaluated ≥2, ≥3, and ≥4 before settling on ≥3:

| Threshold | Ranked     | BASIC (1–1,800) | COMMON (1,801–5,000) | FLUENT (5,001–12,000) | ADVANCED (12,001–25,000) | Unranked   |
| --------- | ---------- | --------------- | -------------------- | --------------------- | ------------------------ | ---------- |
| ≥2        | 63,539     | 7,873           | 11,023               | 22,549                | 22,094                   | 28,553     |
| **≥3** ✅ | **43,060** | **7,271**       | **9,338**            | **16,787**            | **9,664**                | **49,032** |
| ≥4        | 36,130     | 7,129           | 8,908                | 14,375                | 5,718                    | 55,962     |

BASIC/COMMON/FLUENT are stable across all three thresholds — truly common words appear in many sources regardless. The threshold almost entirely controls how many ADVANCED words survive vs. fall into RARE.

≥3 was chosen over ≥4 because the shortlisted sources include 7 media/subtitle sources (ANIME_JDRAMA, NETFLIX, DD2_MORPHMAN_NETFLIX, YOUTUBE_FREQ_V3, DD2_MORPHMAN_SOL, JITEN_ANIME_V2, JITEN_GLOBAL). A word appearing in 3 of these is genuine signal — domain-specific lyric vocabulary that would be unfairly discarded at ≥4. Going ≥2 was rejected because two sources is insufficient cross-validation and produces an ADVANCED tier (28k words) that is too broad.

## Category Tiers V1 (Historical Purposes)

| Tier     | Rank range    | Word count |
| -------- | ------------- | ---------- |
| BASIC    | 1–1,000       | 4,512      |
| COMMON   | 1,001–4,000   | 9,379      |
| FLUENT   | 4,001–10,000  | 15,480     |
| ADVANCED | 10,001–25,000 | 13,689     |

## Results

Threshold Ranked BASIC COMMON FLUENT ADVANCED Unranked
≥2 63,539 4,799 10,784 19,849 28,107 28,553
≥3 43,060 4,512 9,379 15,480 13,689 49,032
≥4 36,130 4,433 9,074 13,753 8,870 55,962

---

## Properties of This Rank

- **Domain-inclusive**: a word gains a good rank if it is frequent in _any_ relevant domain.
- **Not easily gamed by a single source**: the 2-source floor ensures some cross-validation.
- **Learner-oriented**: prioritizes words a learner is likely to encounter in Japanese media and lyrics, rather than words that are statistically frequent in formal written corpora alone.
- **Stable**: uses only shortlisted, quality-vetted sources. Sources in the "Not Recommended" section of `dataset-catalog.md` are never included.
