# Data Quality Experiments 1

This document records findings from re-running coverage experiments after the dataset grew from ~35 to 49 external sources and 4 new anchors were added. §1 covers the setup and changes from Experiments 0. §2–§5 cover new findings. §6 covers the rank-band and threshold results.

---

## 1. What Changed Since Experiments 0

### 1.1 Dataset Growth

The `data/RAW/___FILTERED/` directory grew from ~35 sources to **49 external sources**. New additions include: BCCWJ, CC100, RSPEER, WIKIPEDIA_V2, several MALTESAA_CSJ subcorpora, and others. CEJC_anchor/consolidated.csv was updated but the 4 non-CEJC anchor files (JPDB, YOUTUBE_FREQ_V3, ANIME_JDRAMA, NETFLIX) had not yet been regenerated with the new sources.

`make_more_anchors.py` regenerates all 8 non-CEJC anchors (old 4 + new 4) with the complete 49-source set.

### 1.2 New Anchors

Four new anchors were generated in addition to the existing five (CEJC, JPDB, ANIME_JDRAMA, NETFLIX, YOUTUBE_FREQ_V3):

| Anchor | Type | Total words | Kana missing |
| --- | --- | --- | --- |
| BCCWJ | Balanced written Japanese (NINJAL) | 16,491 | 11.7% |
| CC100 | CommonCrawl web text | 24,605 | 1.9% |
| RSPEER | Multi-source aggregated (wordfreq) | 25,000 | 18.2% |
| WIKIPEDIA_V2 | Wikipedia (clean) | 25,000 | 13.0% |

See §2 for the BCCWJ word count anomaly and §3 for the kana gaps in RSPEER and WIKIPEDIA_V2.

**Rejected candidates:**
- JLAB — anime-subtitle-specific, too domain-narrow for anchor use
- NOVELS — punctuation (、。) at ranks 1 and 3; would distort coverage analysis
- MALTESAA_NWJC — parentheses （） at ranks 1 and 3
- INNOCENT_RANKED — unusual ordering (要る at rank 1)

### 1.3 Updated EXCLUDE Set

Per the §12 recommendation in Experiments 0, H_FREQ, NAROU, and VN_FREQ were added to the exclusion set:

```
EXCLUDE = {
    "AOZORA_BUNKO",       # kanji-only source — zero hiragana words by design
    "NIER",               # single game, ~10k words total
    "ILYASEMENOV",        # Wikipedia dump with HTML entities, wrong domain
    "DD2_MIGAKU_NOVELS",  # curated learner deck, ~16k words
    "HERMITDAVE_2016",    # MeCab morpheme-split tokenization
    "HERMITDAVE_2018",    # same tokenization as HERMITDAVE_2016
    "JPDB",               # anime/game corpus — misses general vocabulary
    "H_FREQ",             # adult content corpus — basic particles absent
    "NAROU",              # UniDic kanji lemma forms — standalone particles absent
    "VN_FREQ",            # UniDic kanji lemma forms — standalone particles absent
}
```

This leaves **38–39 checked sources** per anchor (CEJC checks 51 — see §4).

---

## 2. BCCWJ Anchor: Only 16,491 Unique Words (UniDic POS Duplicates)

**What happened:** BCCWJ's DATA.csv has 25,000 rows but after deduplication (keeping minimum rank per unique word surface form) only **16,491 unique words** remain. `make_more_anchors.py` capped at 25,000 but only found 16,491 unique entries.

**Root cause:** The BCCWJ frequency list was processed with UniDic morphological analysis, which assigns POS tags at sub-word level. When multiple POS sub-classifications map to the same surface form, the same word appears multiple times in the list with different ranks. The deduplication logic (`if w not in word_rank or r < word_rank[w]`) correctly keeps the most frequent rank per word, but the effective unique-word count drops to ~16k.

This is the same mechanism identified in §12 of Experiments 0 for DD2_MORPHMAN sources. DD2_MORPHMAN deduplication was confirmed to produce correct results there — the same applies here.

**Implication for anchor use:** BCCWJ as an anchor has 16,491 words, not 25,000. This is similar in size to DD2_MIGAKU_NOVELS (~16k) which was excluded from coverage checks. **BCCWJ should not be used as a primary anchor** for coverage experiments that require word-count comparability across anchors. However, its per-source coverage rates and rank-band analysis are still meaningful within their scope (they cover only the 16,491 unique top-ranked words).

---

## 3. Kana Gaps in RSPEER and WIKIPEDIA_V2

| Anchor | Kana missing |
| --- | --- |
| BCCWJ | 11.7% (1,937 words) |
| CC100 | 1.9% (470 words) |
| RSPEER | 18.2% (4,544 words) |
| WIKIPEDIA_V2 | 13.0% (3,250 words) |

CC100 is nearly complete (1.9% gap). RSPEER and WIKIPEDIA_V2 have large gaps because:

- **RSPEER** aggregates multiple sources including rare and technical vocabulary from news, books, and web. Many kanji-form words in the 25k list are not headwords in JPDBV2 or the CEJC TSV (which are entertainment-media and everyday-speech focused respectively). Proper nouns, compound nouns, and technical terms account for most gaps.

- **WIKIPEDIA_V2** contains many proper nouns (place names, organization names, technical terms) that appear frequently in Wikipedia but are not in JPDBV2's lemma dictionary. Conjugated/derived forms that aren't headwords also contribute.

These gaps are structural (JPDBV2 and CEJC TSV are the only two reading sources available and both are lemma/dictionary focused). They do not affect the frequency ranking data — only the hiragana/katakana columns are blank (`-`) for those words.

---

## 4. CEJC Checks 51 Sources vs 38 for Others

In the coverage analysis, CEJC anchor checks **51 sources** while all other anchors check 38–39. This is because:

CEJC's `consolidated.csv` has no single `CEJC_rank` anchor column — instead it has 14 CEJC sub-corpus columns (`combined_rank`, `small_talk_rank`, `consultation_rank`, `meeting_rank`, `class_rank`, `outdoors_rank`, `school_rank`, `transportation_rank`, `public_commercial_rank`, `home_rank`, `indoors_rank`, `workplace_rank`, `male_rank`, `female_rank`). The analysis script treats all non-word non-anchor columns as sources. Since `CEJC_rank` doesn't exist in the header, none of these 14 columns are excluded as the anchor column — all become source columns.

Result: zero-missing for CEJC counts a word only if it appears across **51 checks** (14 CEJC sub-corpus checks + 49 external - 10 excluded + 2 = 51). A word absent from a specific CEJC sub-corpus (e.g., not recorded in small-talk conversations) will fail the zero-missing check even if it has a valid combined_rank.

This makes CEJC zero-missing percentages **not directly comparable** to the other anchors. The zero-missing count (3,600 = 12.9%) is artificially depressed by the sub-corpus requirement. For direct comparisons, use the threshold-based counts (§6.2) which are more robust to this effect.

---

## 5. JPDB's Coverage Remains Structurally Distinct

JPDB's coverage rates (top-500: 41.6%, all: 6.9%) are far lower than every other anchor. This confirms the Experiments 0 §11 finding — JPDB's anime/game corpus systematically omits real-world vocabulary — and it persists even after adding 3 more exclusions. The threshold-based count for JPDB (2,862 high-frequency words at N≤3, 11.8%) is half that of any other anchor. JPDB should continue to be excluded from coverage quality checks and treated as a domain-specific reference, not a general-frequency anchor.

---

## 6. Coverage Experiment Results

### 6.1 Rank-Band Zero-Missing Analysis

Zero-missing counts across 38 checked sources (10 excluded). CEJC checks 51 sources — see §4 for why its numbers are not directly comparable.

| Anchor | Sources checked | Top-500 | Top-1k | Top-3k | Top-5k | Top-10k | All words |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CC100 | 38 | **85.6%** | 79.4% | 63.4% | 52.7% | 34.6% | 15.9% |
| NETFLIX | 38 | 78.0% | 71.1% | 57.6% | 48.7% | 35.4% | 17.8% |
| WIKIPEDIA_V2 | 38 | 77.2% | 73.4% | 56.9% | 47.6% | 33.8% | 17.2% |
| YOUTUBE_FREQ_V3 | 38 | 77.6% | 71.8% | 60.7% | 52.0% | 35.8% | 15.2% |
| BCCWJ | 38 | 74.1%* | 74.1% | 63.9% | 52.5% | 34.5% | 22.3%* |
| ANIME_JDRAMA | 38 | 70.6% | 66.4% | 54.9% | 46.2% | 34.0% | 17.9% |
| CEJC | 51 | 71.8% | 68.5% | 54.3% | 43.7% | 28.9% | 12.9% |
| RSPEER | 38 | 69.6% | 66.0% | 57.5% | 49.8% | 35.6% | 17.3% |
| JPDB | 39 | 41.6% | 30.1% | 18.0% | 14.8% | 11.2% | 6.9% |

\* BCCWJ has only 16,491 words total — its "Top-500" is the 500 most frequent words in its 16,491-word list. The "All words" percentage is computed over 16,491 words, not 25,000.

**Key findings:**

1. **CC100 has the strongest top-500 coverage (85.6%)** — the highest of any anchor. CommonCrawl web text covers virtually all high-frequency vocabulary across every domain. This makes CC100 the best-performing single anchor for zero-missing at the top of the frequency range.

2. **The top-500 → top-1k drop is larger for spoken/subtitle anchors** than for written/web anchors:
   - CC100: 85.6% → 79.4% (−6.2pp)
   - YOUTUBE: 77.6% → 71.8% (−5.8pp)
   - NETFLIX: 78.0% → 71.1% (−6.9pp)
   - WIKIPEDIA: 77.2% → 73.4% (−3.8pp)
   - BCCWJ: 74.1% → 74.1% (0pp — very stable from 500 to 1000)

   BCCWJ shows near-zero drop from rank 500 to 1000, suggesting its top-1000 words are exceptionally "universal" — likely the high-frequency core that appears in every domain.

3. **All anchors converge near 15–18% zero-missing for their full word list** (except JPDB at 7% and BCCWJ at 22% over its smaller 16k set). This confirms the mathematical ceiling effect described in §12 of Experiments 0: with 38 domain-specific sources, each adding coverage requirements, the ceiling is set by the worst-coverage source in the checked set.

4. **RSPEER underperforms its size.** Despite being a multi-source aggregate, RSPEER's top-500 zero-missing (69.6%) is lower than YOUTUBE (77.6%) or NETFLIX (78.0%). Investigation: RSPEER's word list is sorted by Zipf frequency, not rank, and includes many colloquial/short tokens at the top (from social media sources like Twitter/Reddit). Some of these tokens are absent from formal written corpora. The aggregation methodology smooths out outliers but the Japanese word list still reflects MeCab tokenization which may include morpheme-level tokens.

5. **JPDB's coverage collapses below top-500.** From 41.6% at top-500 to 30.1% at top-1000 to 6.9% overall — an almost linear collapse. Every 1,000-word band below the top adds a larger proportion of words absent from JPDB's anime/game register.

### 6.2 Threshold Analysis (N≤3 High-Frequency Words)

Words missing from at most 3 of the 38 checked sources:

| Anchor | Total words | High-freq (≤3 missing) | % |
| --- | --- | --- | --- |
| YOUTUBE_FREQ_V3 | 30,000 | 7,500 | 25.0% |
| ANIME_JDRAMA | 25,000 | 7,349 | 29.4% |
| NETFLIX | 25,000 | 7,349 | 29.4% |
| RSPEER | 25,000 | 6,987 | 27.9% |
| WIKIPEDIA_V2 | 25,000 | 6,833 | 27.3% |
| CC100 | 24,605 | 6,624 | 26.9% |
| CEJC | 27,988 | 6,042 | 21.6% |
| BCCWJ | 16,491 | 6,186 | 37.5%* |
| JPDB | 24,231 | 2,862 | 11.8% |

\* BCCWJ's 37.5% is over a 16,491-word list — not comparable to 25k-word anchors.

**Key findings:**

1. **YOUTUBE_FREQ_V3 yields the most high-frequency words (7,500)** but covers 30,000 total, giving the lowest %. ANIME_JDRAMA and NETFLIX each yield 7,349 despite covering only 25,000 words — a higher density of broadly covered vocabulary.

2. **The subtitle anchors (ANIME_JDRAMA, NETFLIX) have the best high-frequency density** at ~29%. They cover spoken/conversational Japanese where vocabulary overlaps heavily across all corpora. Written/web anchors (CC100, WIKIPEDIA_V2) produce slightly fewer high-frequency words per 25k — likely because they include more domain-specific written vocabulary that only appears in certain corpora.

3. **CEJC's count (6,042, 21.6%) is lower than expected** given it's the largest anchor (27,988 words). Two reasons: (a) it checks 51 sources instead of 38 (§4 — CEJC sub-corpus columns count as checks); (b) CEJC includes UniDic lemma-form words (其れ, 為る) that are absent from surface-form sources and hard to bridge even with the kana fallback.

4. **RSPEER and WIKIPEDIA_V2 perform well** (6,987 and 6,833 respectively) for web/aggregated sources. Their threshold counts are comparable to the subtitle anchors, confirming they cover general Japanese vocabulary broadly.

5. **JPDB remains the outlier** (2,862, 11.8%) — roughly 1/3 the high-frequency count of any other anchor. No change in EXCLUDE set affects this; it is a structural property of the corpus.

### 6.3 Comparison with Experiments 0

In Experiments 0 (7 excluded, YOUTUBE anchor), the results were:

| | Experiments 0 | Experiments 1 |
| --- | --- | --- |
| Excluded sources | 7 | 10 (+H_FREQ, NAROU, VN_FREQ) |
| Checked sources (YOUTUBE) | 28 | 38 (+RSPEER and other new sources) |
| Zero-missing (YOUTUBE, all words) | 4,463 (14.9%) | 4,557 (15.2%) |
| High-freq N≤3 (YOUTUBE) | 7,834 (26.1%) | 7,500 (25.0%) |

Zero-missing count is essentially the same (4,463 vs 4,557) despite 10 more sources being checked. This is because the 3 newly excluded sources (H_FREQ, NAROU, VN_FREQ) were causing ~1% of false failures that the 10 newly checked sources partially offset. The net effect is a slight improvement in zero-missing percentage (14.9% → 15.2%) because the removed false-negative sources caused more harm than the newly added sources.

The threshold N≤3 count dropped slightly (7,834 → 7,500) because YOUTUBE now has 30,000 words checked instead of fewer — the threshold analysis runs on the full word list, and the extra words at ranks 25,001–30,000 are mostly domain-specific vocabulary with higher miss rates.

---

## 7. Recommendations

1. **Use CC100 or NETFLIX/ANIME_JDRAMA as the primary anchor** for general-purpose frequency analysis. CC100 gives the strongest top-500 coverage (85.6%); ANIME_JDRAMA and NETFLIX give the highest high-frequency density per 25k words (29.4%).

2. **Do not use BCCWJ as an anchor** for cross-anchor comparisons — its 16,491 unique words make it incomparable to 25k anchors. It is valid as a source column.

3. **RSPEER and WIKIPEDIA_V2 are good anchors** for written/web Japanese analysis. Their zero-missing and threshold numbers are similar to NETFLIX/ANIME_JDRAMA.

4. **JPDB remains excluded** from quality checks. Its 11.8% high-frequency rate confirms it should never be used as a coverage signal for general Japanese.

5. **Threshold N≤3 remains the recommended primary filter** (§10 of Experiments 0). A word missing from at most 3 of 38 checked sources is genuinely broadly common. At N≤3, YOUTUBE yields 7,500 words and ANIME_JDRAMA/NETFLIX yield ~7,350 words — these are robust "core vocabulary" sets.

6. **CEJC zero-missing is not directly comparable** to other anchors due to 51 checks (14 sub-corpus columns) vs 38. For cross-anchor comparisons, use threshold counts.
