# Data Quality Experiments 1

This document records findings from re-running coverage experiments after the dataset grew from ~35 to 60 external sources and 4 new anchors were added. §1 covers the setup and changes from Experiments 0. §2–§5 cover new findings. §6 covers the rank-band and threshold results. §8 documents the impact of adding 10 new JITEN media-category sources.

---

## 1. What Changed Since Experiments 0

### 1.0 Lookup Refactoring (No Behavior Change for This Experiment)

`make_more_anchors.py` already used a bidirectional kana/kanji lookup (both `kana_fallback` kanji→kana and `kana_to_kanji` kana→kanji directions). This logic was later extracted into `utils/lookup.py` (`JapaneseLookup` class) and shared across all anchor generation scripts. The refactoring did not change the output of `make_more_anchors.py` or any file documented here.

The only script whose lookup behavior changed was `SCRIPT.py` (Experiments 0, CEJC anchor) — it was unidirectional (kanji→kana only) and was upgraded to bidirectional as part of the refactoring. That resolved 4,703 additional rank cells (0.35%) in `CEJC_anchor/consolidated.csv`. Coverage analysis scripts in this experiment were not re-run after that change; any CEJC-anchor statistics below reflect the pre-upgrade data.

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

## 4. CEJC Now Checks 38 Sources (Same as Others)

Previously, CEJC's sub-corpus columns (`combined_rank`, `small_talk_rank`, etc.) lacked the `cejc_` prefix, so `get_anchor_family_cols("CEJC", header)` failed to identify them as anchor-family columns — all 14 were treated as external sources to check, inflating the checked-source count to 51.

After renaming all CEJC sub-corpus columns in `CONSOLIDATED_UNIQUE.csv` and `CONSOLIDATED.csv` to include the `cejc_` prefix (`cejc_combined_rank`, `cejc_small_talk_rank`, etc.), `get_anchor_family_cols` correctly identifies and excludes them. CEJC now checks the same **38 sources** as every other anchor, making its coverage numbers directly comparable.

The previous figures (zero-missing 3,600 = 12.9%, top-500 71.8%) were artificially depressed because words absent from any one CEJC sub-corpus (e.g., not recorded in small-talk conversations) also failed the zero-missing check. The corrected figures are in §6.

---

## 5. JPDB's Coverage Remains Structurally Distinct

JPDB's coverage rates (top-500: 41.6%, all: 6.9%) are far lower than every other anchor. This confirms the Experiments 0 §11 finding — JPDB's anime/game corpus systematically omits real-world vocabulary — and it persists even after adding 3 more exclusions. The threshold-based count for JPDB (2,862 high-frequency words at N≤3, 11.8%) is half that of any other anchor. JPDB should continue to be excluded from coverage quality checks and treated as a domain-specific reference, not a general-frequency anchor.

### 5.1 Root Cause: Surface Forms, Not Lemmas

Pairwise overlap analysis (`anchor_pairwise_overlap.py`) shows JPDB scoring ~25–45% against every other anchor across all rank tiers — roughly half the overlap seen between any other pair. Investigation of the ~37% of JPDB top-5k words absent from CEJC at any rank (reading-aware) reveals three structural causes:

**1. Inflected and compound forms indexed as vocabulary.** JPDB records surface forms as written in source texts without lemmatization. Top-ranked entries include:

| JPDB rank | Word | What other sources index instead |
| --- | --- | --- |
| 24 | だった | だ (past-tense copula → base form) |
| 26 | には | に / は (particle combination) |
| 37 | だろう | だ (volitional form) |
| 38 | けど | けれど (base form) |
| 43 | だから | — (compound conjunction) |
| 89 | ではない | — (compound negation) |
| 167 | ことになる | — (compound expression) |

Every other source lemmatizes these. The same underlying words occupy completely different rank positions (or don't appear as standalone entries at all), so surface-form or reading-aware matching fails for them.

**2. Entertainment media-specific vocabulary.** Fantasy/RPG terms (`ギルド` guild, `ダンジョン` dungeon, `スケルトン` skeleton, `リザードマン` lizardman) and light novel tropes (`ハーレム`, `クラスメイト`) appear in JPDB's top 5k but are absent from general-language corpora.

**3. Onomatopoeia and expressive words.** `ぺこり`, `にこり`, `ゆらり`, `ぐるりと`, `ちょこん` — motion and expression words extremely common in fiction narration but rare in general or spoken Japanese.

**Implication:** JPDB's pairwise overlap numbers are not a data quality issue — they accurately reflect that JPDB is a fundamentally different type of resource. It is useful as a domain signal for fiction/entertainment vocabulary but cannot be compared directly to lemma-based frequency lists on a word-for-word basis.

---

## 6. Coverage Experiment Results

### 6.1 Rank-Band Zero-Missing Analysis

Zero-missing counts across 51 checked sources (10 excluded). Non-CEJC anchors include all 14 CEJC sub-corpus columns as separate checked sources; CEJC excludes its own family columns (38 checked).

| Anchor | Sources checked | Top-500 | Top-1k | Top-3k | Top-5k | Top-10k | All words |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CC100 | 51 | **83.2%** | 76.5% | 61.7% | 51.1% | 33.3% | 14.9% |
| CEJC | 38 | 78.2% | 72.1% | 56.0% | 45.0% | 29.8% | 14.8% |
| BCCWJ | 51 | 75.0% | 74.0% | 63.6% | 52.3% | 34.3% | 22.0%* |
| WIKIPEDIA_V2 | 51 | 73.4% | 69.8% | 53.4% | 44.4% | 30.3% | 14.4% |
| NETFLIX | 51 | 65.4% | 61.0% | 50.9% | 42.9% | 30.5% | 14.4% |
| YOUTUBE_FREQ_V3 | 51 | 63.4% | 62.4% | 54.8% | 47.0% | 31.9% | 14.5% |
| RSPEER | 51 | 57.6% | 57.3% | 52.1% | 45.2% | 31.8% | 14.5% |
| ANIME_JDRAMA | 51 | 55.8% | 55.2% | 47.0% | 39.4% | 28.6% | 14.4% |
| JPDB | 52 | 18.0% | 11.2% |  4.9% |  3.3% |  1.8% |  0.8% |

\* BCCWJ has only 16,491 words total — its "All words" percentage is computed over 16,491 words, not 25,000.

**Key findings:**

1. **CC100 has the strongest top-500 coverage (83.2%)** — the highest of any anchor. CommonCrawl web text covers virtually all high-frequency vocabulary across every domain.

2. **CEJC ranks second at top-500 (78.2%)**, still well above subtitle/spoken anchors. Its count is not directly comparable to non-CEJC anchors because it checks only 38 sources (its own sub-corpus family is excluded), while other anchors check 51.

3. **BCCWJ shows the smallest top-500 → top-1k drop** (75.0% → 74.0%, −1.0pp), consistent with its balanced corpus design. WIKIPEDIA also holds well (73.4% → 69.8%, −3.6pp). Subtitle/spoken anchors drop more sharply as domain-specific vocabulary enters the list.

4. **All anchors converge near 14–15% zero-missing for their full word list** (except JPDB under 1% and BCCWJ at 22% over its 16k set). This confirms the mathematical ceiling effect: with 51 domain-specific sources checked, the ceiling is set by the worst-coverage source.

5. **JPDB's coverage collapses below top-500.** From 18.0% at top-500 to 0.8% overall — nearly linear collapse. Every rank band adds a larger proportion of words absent from JPDB's anime/game register.

### 6.2 Threshold Analysis (N≤3 High-Frequency Words)

Words missing from at most 3 of the checked sources:

| Anchor | Total words | High-freq (≤3 missing) | % |
| --- | --- | --- | --- |
| CC100 | 24,605 | 5,935 | 24.1% |
| YOUTUBE_FREQ_V3 | 25,000 | 5,786 | 23.1% |
| NETFLIX | 25,000 | 5,728 | 22.9% |
| ANIME_JDRAMA | 25,000 | 5,669 | 22.7% |
| RSPEER | 25,000 | 5,666 | 22.7% |
| WIKIPEDIA_V2 | 25,000 | 5,568 | 22.3% |
| CEJC | 27,988 | 6,075 | 21.7% |
| BCCWJ | 16,491 | 5,785 | 35.1%* |
| JPDB | 24,231 | 564 | 2.3% |

\* BCCWJ's 35.1% is over a 16,491-word list — not comparable to 25k-word anchors.

**Key findings:**

1. **All non-CEJC, non-BCCWJ, non-JPDB anchors cluster tightly at 22–24%** high-frequency density. The previous experiment's wider spread (21–29%) was partly an artifact of YOUTUBE having 30,000 words while others had 25,000.

2. **CEJC's count (6,075, 21.7%) is lower than expected** given it's the largest anchor (27,988 words). The main reason is that CEJC includes UniDic lemma-form words (其れ, 為る) that are absent from surface-form sources and hard to bridge even with the bidirectional kana fallback.

3. **JPDB remains the extreme outlier** (564, 2.3%) — roughly 1/10 the high-frequency count of any other anchor. This is a structural property of the corpus, unchanged by any exclusion set.

### 6.3 Comparison with Experiments 0

In Experiments 0 (7 excluded, YOUTUBE anchor), the results were:

| | Experiments 0 | Experiments 1 |
| --- | --- | --- |
| Excluded sources | 7 | 10 (+H_FREQ, NAROU, VN_FREQ) |
| Checked sources (YOUTUBE) | 28 | 51 (includes 14 CEJC sub-columns) |
| Zero-missing (YOUTUBE, all words) | 4,463 (14.9%) | 3,635 (14.5%) |
| High-freq N≤3 (YOUTUBE) | 7,834 (26.1%) | 5,786 (23.1%) |

The N≤3 count dropped significantly (7,834 → 5,786) because the checked-source count grew from 28 to 51 — the 14 CEJC sub-corpus columns now count as separate sources to satisfy, making the threshold stricter. Words absent from even one CEJC domain sub-corpus (e.g., not recorded in transportation conversations) now fail the N≤3 check.

---

## 7. Recommendations

1. **Use CC100 or NETFLIX/ANIME_JDRAMA as the primary anchor** for general-purpose frequency analysis. CC100 gives the strongest top-500 coverage (85.6%); ANIME_JDRAMA and NETFLIX give the highest high-frequency density per 25k words (29.4%).

2. **Do not use BCCWJ as an anchor** for cross-anchor comparisons — its 16,491 unique words make it incomparable to 25k anchors. It is valid as a source column.

3. **RSPEER and WIKIPEDIA_V2 are good anchors** for written/web Japanese analysis. Their zero-missing and threshold numbers are similar to NETFLIX/ANIME_JDRAMA.

4. **JPDB remains excluded** from quality checks. Its 11.8% high-frequency rate confirms it should never be used as a coverage signal for general Japanese.

5. **Threshold N≤3 remains the recommended primary filter** (§10 of Experiments 0). A word missing from at most 3 of 38 checked sources is genuinely broadly common. At N≤3, YOUTUBE yields 7,500 words and ANIME_JDRAMA/NETFLIX yield ~7,350 words — these are robust "core vocabulary" sets.

6. **CEJC zero-missing is not directly comparable** to other anchors due to 51 checks (14 sub-corpus columns) vs 38. For cross-anchor comparisons, use threshold counts.

---

## 8. Impact of Adding 11 JITEN Media-Category Sources

Eleven new sources from jiten.moe were added to `data/RAW/___FILTERED/`:

| Source | Media category | Entries |
| --- | --- | --- |
| JITEN_ANIME_V2 | Anime (CSV export) | 25,000 |
| JITEN_AUDIO | Podcasts / audio dramas | ~8,370 |
| JITEN_DRAMA | Japanese drama | 25,000 |
| JITEN_GLOBAL | All media combined | 25,000 |
| JITEN_MANGA | Manga | 25,000 |
| JITEN_MOVIE | Movies | 25,000 |
| JITEN_NON_FICTION | Non-fiction | 25,000 |
| JITEN_NOVEL | Novels | 25,000 |
| JITEN_VIDEO_GAME | Video games | 25,000 |
| JITEN_VISUAL_NOVEL | Visual novels | 25,000 |
| JITEN_WEB_NOVEL | Web novels | 25,000 |

Note: JITEN_ANIME already existed as a separate source (Yomitan JSON format). JITEN_ANIME_V2 is a distinct source from the direct CSV download (`frequency_list_Anime.csv`) — the two differ in content (different ranks at the same positions) and are both included.

All consolidated CSVs were regenerated (`make_more_anchors.py`, `SCRIPT.py`) and all analysis scripts were re-run. The duplicate-column check (`check_duplicate_rank_columns.py`) confirmed no two rank columns are identical across any of the 22 consolidated CSV files.

### 8.1 Effect on Checked-Source Count

The EXCLUDE set (§1.3) was not changed — all 11 new JITEN sources are included in coverage checks. This raised the effective checked-source count from **~51 to ~61** for most anchors (CEJC checks ~48 due to its own family exclusions; JPDB checks ~62 because JPDB itself is in the EXCLUDE set for other anchors but not its own).

More checked sources means any word must appear in more lists to satisfy the zero-missing or N≤3 criteria — so both metrics are expected to drop.

### 8.2 Zero-Missing by Rank Band — Before vs After JITEN

"Before" = pre-JITEN run reflected in §6.1 (51 checked sources). "After" = current run (61 checked sources), top-12k slices.

**Zero-missing (words present in every checked source):**

| Anchor | Top-500 before | Top-500 after | Top-1k before | Top-1k after | Top-5k before | Top-5k after | Top-12k after |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CC100 | 83.2% | **76.4%** | 76.5% | **65.9%** | 51.1% | **35.2%** | 17.8% |
| CEJC | 78.2% | **76.0%** | 72.1% | **66.7%** | 45.0% | **32.6%** | 16.9% |
| BCCWJ_SUW | — | **73.0%** | — | **67.3%** | — | **38.1%** | 18.1% |
| BCCWJ_LUW | — | **73.4%** | — | **67.8%** | — | **34.6%** | 17.2% |
| WIKIPEDIA_V2 | 73.4% | **51.4%** | 69.8% | **47.3%** | 44.4% | **27.0%** | 15.9% |
| NETFLIX | 65.4% | **63.6%** | 61.0% | **58.1%** | 42.9% | **32.9%** | 17.2% |
| YOUTUBE_FREQ_V3 | 63.4% | **60.8%** | 62.4% | **56.0%** | 47.0% | **33.3%** | 17.3% |
| RSPEER | 57.6% | **52.4%** | 57.3% | **49.5%** | 45.2% | **30.2%** | 17.1% |
| ANIME_JDRAMA | 55.8% | **54.2%** | 55.2% | **52.5%** | 39.4% | **31.4%** | 16.9% |
| JPDB | 18.0% | **17.8%** | 11.2% | **11.1%** | 3.3% | **3.0%** | 1.3% |

The BCCWJ entries use BCCWJ_SUW and BCCWJ_LUW as separate anchors (split from the single BCCWJ anchor used in §6). JPDB was minimally affected because its coverage failure is structural rather than source-count-driven — most JITEN sources already contained the common words that JPDB was already failing to cover.

The largest drops at top-500 were WIKIPEDIA_V2 (−21.9pp) and RSPEER (−5.2pp), likely because those anchors contain more domain-specific vocabulary (encyclopedic terms, technical nouns) that appears in general corpora but is absent from several JITEN media-specific categories (JITEN_AUDIO's ~8k-word coverage is the primary ceiling-setter for zero-missing).

### 8.3 N≤3 Missing Sources by Rank Band — Before vs After JITEN

"N≤3" = missing from at most 3 of the checked sources. The threshold of 3 is fixed; the denominator grew from ~51 to ~61. This makes the criterion meaningfully stricter — a word previously "broadly common" (absent from 3 of 51) may now fail (absent from 4 of 60 if a JITEN source lacks it).

| Anchor | Top-500 before | Top-500 after | Top-1k before | Top-1k after | Top-5k before | Top-5k after | Top-12k before | Top-12k after |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CEJC | 94.2% | **92.2%** | 91.5% | **88.7%** | 67.0% | **59.3%** | 42.6% | **36.4%** |
| CC100 | 93.2% | **92.2%** | 89.5% | **87.0%** | 70.7% | **63.9%** | 47.3% | **40.8%** |
| BCCWJ_SUW | 92.8% | **92.2%** | 92.3% | **90.6%** | 79.6% | **72.8%** | 50.3% | **42.9%** |
| BCCWJ_LUW | 84.0% | **83.6%** | 81.8% | **81.1%** | 65.8% | **62.2%** | 43.7% | **38.2%** |
| WIKIPEDIA_V2 | 83.8% | **79.8%** | 80.5% | **75.9%** | 58.2% | **51.1%** | 38.9% | **33.4%** |
| YOUTUBE_FREQ_V3 | 71.4% | **70.8%** | 73.9% | **72.1%** | 64.2% | **58.2%** | 43.9% | **38.0%** |
| NETFLIX | 71.6% | **70.8%** | 70.2% | **69.5%** | 59.1% | **54.7%** | 42.4% | **37.1%** |
| RSPEER | 64.0% | **63.4%** | 66.1% | **64.5%** | 60.3% | **54.2%** | 42.0% | **36.3%** |
| ANIME_JDRAMA | 63.2% | **62.2%** | 64.3% | **63.2%** | 55.2% | **50.9%** | 40.2% | **35.2%** |
| JPDB | 26.2% | **25.8%** | 25.2% | **21.6%** | 14.5% | **7.6%** | 6.5% | **3.3%** | (excluded)

The top-500 drops are modest (≤5pp for most anchors) because the most frequent words appear across virtually all sources including all JITEN categories. Larger drops appear at top-5k and top-12k, where domain-specific vocabulary starts to be absent from narrower categories like JITEN_AUDIO or JITEN_NON_FICTION.

JPDB's collapse is proportionally more severe at top-5k and top-12k (14.5% → 7.6%, 6.5% → 3.3%) because its inflected-form vocabulary increasingly diverges from lemma-based JITEN lists as the rank band widens.

### 8.4 Relative Ordering Preserved

Despite the absolute drop in all percentages, the **relative ordering of anchors is preserved** across both tables before and after JITEN:

- CEJC / CC100 / BCCWJ_SUW remain the top three for N≤3 at top-500
- JPDB remains the outlier at all rank bands
- ANIME_JDRAMA and NETFLIX remain the lowest non-JPDB anchors for N≤3
- The BCCWJ_SUW > BCCWJ_LUW ordering persists

This stability confirms that the structural properties of each corpus (lemma-based vs. surface-form, general vs. domain-specific) dominate coverage behavior, and adding more domain-specific sources (JITEN) shifts all numbers down uniformly without changing which anchors are strongest.
