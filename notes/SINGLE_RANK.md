# Single Rank Algorithm

- **Output:** [data/ALL/RIRIKKU_CONSOLIDATED.csv](../data/ALL/RIRIKKU_CONSOLIDATED.csv)
- **Script:** [data/ALL/\_\_\_data_generation/make_ririkku.py](../data/ALL/___data_generation/make_ririkku.py)
- **Category tables script:** [data/ALL/\_\_\_experiments3/category_tables.py](../data/ALL/___experiments3/category_tables.py)

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
- The **3-source threshold** prevents a single outlier source from inflating a word's rank. It requires at least minimal cross-source validation.

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
| `JITEN_DRAMA`          | Japanese drama frequency from jiten.moe (~217k source entries). Directly relevant to J-drama vocabulary — the live-action register closest to song lyrics.                                                                           |
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

| Column ID        | Reason Excluded                                                                                                                                                                                                       |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `MALTESAA_CSJ`   | Corpus of Spontaneous Japanese — primarily formal academic monologues and conference presentations. Register is far from lyrics.                                                                                      |
| `JITEN_ANIME_V2` | Superseded by `JITEN_DRAMA` for the drama/lyrics use case. Still included as an informational column in `RIRIKKU_CONSOLIDATED.csv` but not used for rank computation. The global `JITEN_GLOBAL` already covers anime. |

### Note on CEJC Lemma Forms

CEJC uses UniDic lemma forms (e.g. 為る for する, 其れ for それ). This is fine for our purposes: we rank the **word** (dictionary/lemma concept), not a specific written form. Each word entry on ririkku.com displays all forms it can appear in, so the lemma-based rank from CEJC feeds correctly into the algorithm.

---

## Category Breakdown and Threshold Selection

### Category Rank Ranges (Type A)

| Tier     | Rank range    | Word count ≥3 |
| -------- | ------------- | ------------- |
| BASIC    | 1–1,800       | 7,250         |
| COMMON   | 1,801–5,000   | 9,308         |
| FLUENT   | 5,001–12,000  | 16,836        |
| ADVANCED | 12,001–25,000 | 9,583         |

> **Note on inflated tiers:** because **RIRIKKU_RANK** uses the _minimum_ across 16 sources, a word only needs to be top-ranked in _one_ of those sources to land in BASIC, COMMON, or FLUENT. The ≥3 source threshold provides meaningful cross-validation while preserving domain-specific lyric vocabulary — words appearing in only 1–2 sources are treated as RARE. The full list is a backend reference; users only see ranks for words that appear in lyric content.

We evaluated ≥2, ≥3, and ≥4 before settling on ≥3:

| Threshold | TOTAL      | BASIC     | COMMON    | FLUENT     | ADVANCED  | Unranked   |
| --------- | ---------- | --------- | --------- | ---------- | --------- | ---------- |
| ≥2        | 63,421     | 7,877     | 10,999    | 22,601     | 21,944    | 28,750     |
| **≥3** ✅ | **42,977** | **7,250** | **9,308** | **16,836** | **9,583** | **49,194** |
| ≥4        | 36,071     | 7,118     | 8,901     | 14,405     | 5,647     | 56,100     |

### Category Rank Ranges (Type B)

| Tier     | Rank range    | Word count ≥3 |
| -------- | ------------- | ------------- |
| BASIC    | 1–1,000       | 4,489         |
| COMMON   | 1,001–4,000   | 9,359         |
| FLUENT   | 4,001–10,000  | 15,486        |
| ADVANCED | 10,001–25,000 | 13,643        |

| Threshold | TOTAL      | BASIC     | COMMON    | FLUENT     | ADVANCED   | Unranked   |
| --------- | ---------- | --------- | --------- | ---------- | ---------- | ---------- |
| ≥2        | 63,421     | 4,788     | 10,793    | 19,872     | 27,968     | 28,750     |
| **≥3** ✅ | **42,977** | **4,489** | **9,359** | **15,486** | **13,643** | **49,194** |
| ≥4        | 36,071     | 4,413     | 9,072     | 13,772     | 8,814      | 56,100     |

BASIC/COMMON/FLUENT are stable across all three thresholds — truly common words appear in many sources regardless. The threshold almost entirely controls how many ADVANCED words survive vs. fall into RARE.

≥3 was chosen over ≥4 because the shortlisted sources include 7 media/subtitle sources (ANIME_JDRAMA, NETFLIX, DD2_MORPHMAN_NETFLIX, YOUTUBE_FREQ_V3, DD2_MORPHMAN_SOL, JITEN_DRAMA, JITEN_GLOBAL). A word appearing in 3 of these is genuine signal — domain-specific lyric vocabulary that would be unfairly discarded at ≥4. Going ≥2 was rejected because two sources is insufficient cross-validation and produces an ADVANCED tier (28k words) that is too broad.

---

## Alternative: Bucket Count Algorithm

**Script:** [data/ALL/\_\_\_experiments3/bucket_category_tables.py](../data/ALL/___experiments3/bucket_category_tables.py)

Instead of taking the minimum rank across sources, this algorithm counts how many of a word's valid source ranks fall into each tier bucket, then assigns the tier with the most counts. Ties are broken by preferring the higher tier (BASIC > COMMON > FLUENT > ADVANCED).

```
bucket_tier(word) =
  sources = [rank for rank in included_sources if rank != -1]
  if len(sources) < 3: return UNRANKED
  counts = {tier: count of sources whose rank falls in that tier's range}
  return tier with max count (prefer higher tier on tie)
```

This contrasts with the minimum algorithm:

- **Minimum**: a word ranks highly if _any_ source considers it common (domain-inclusive).
- **Bucket**: a word ranks highly only if _most_ sources consider it common (majority-vote).

The bucket approach is more conservative — words that are top-ranked in just one or two domains (e.g. anime-specific vocabulary ranked #200 in ANIME_JDRAMA but #8000–#12000 elsewhere) will fall into a lower tier compared to the minimum algorithm.

### Category Rank Ranges (Type A)

| Tier     | Rank range    | Word count ≥3 |
| -------- | ------------- | ------------- |
| BASIC    | 1–1,800       | 3,032         |
| COMMON   | 1,801–5,000   | 4,368         |
| FLUENT   | 5,001–12,000  | 10,794        |
| ADVANCED | 12,001–25,000 | 24,783        |

| Threshold | TOTAL      | BASIC     | COMMON    | FLUENT     | ADVANCED   | Unranked   |
| --------- | ---------- | --------- | --------- | ---------- | ---------- | ---------- |
| ≥2        | 63,421     | 3,659     | 6,059     | 16,559     | 37,144     | 28,750     |
| **≥3** ✅ | **42,977** | **3,032** | **4,368** | **10,794** | **24,783** | **49,194** |
| ≥4        | 36,071     | 2,951     | 4,107     | 9,659      | 19,354     | 56,100     |

### Category Rank Ranges (Type B)

| Tier     | Rank range    | Word count ≥3 |
| -------- | ------------- | ------------- |
| BASIC    | 1–1,000       | 1,671         |
| COMMON   | 1,001–4,000   | 4,297         |
| FLUENT   | 4,001–10,000  | 7,737         |
| ADVANCED | 10,001–25,000 | 29,272        |

| Threshold | TOTAL      | BASIC     | COMMON    | FLUENT    | ADVANCED   | Unranked   |
| --------- | ---------- | --------- | --------- | --------- | ---------- | ---------- |
| ≥2        | 63,421     | 1,970     | 5,731     | 12,123    | 43,597     | 28,750     |
| **≥3** ✅ | **42,977** | **1,671** | **4,297** | **7,737** | **29,272** | **49,194** |
| ≥4        | 36,071     | 1,626     | 4,116     | 7,079     | 23,250     | 56,100     |

**Key observation:** The bucket algorithm produces substantially fewer BASIC and COMMON words (3,032 / 4,368 vs. 7,250 / 9,308 at ≥3 for Type A) because domain-specific vocabulary that is top-ranked in only a few sources gets pulled toward the ADVANCED tier. The minimum algorithm is the chosen approach for ririkku.com precisely because it preserves this domain-specific lyric vocabulary.

---

## Properties of This Rank

- **Domain-inclusive**: a word gains a good rank if it is frequent in _any_ relevant domain.
- **Not easily gamed by a single source**: the 3-source floor ensures meaningful cross-validation.
- **Learner-oriented**: prioritizes words a learner is likely to encounter in Japanese media and lyrics, rather than words that are statistically frequent in formal written corpora alone.
- **Stable**: uses only shortlisted, quality-vetted sources. Sources in the "Not Recommended" section of `dataset-catalog.md` are never included.
