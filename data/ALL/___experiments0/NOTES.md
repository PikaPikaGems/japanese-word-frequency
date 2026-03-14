# Some Insights From Experiments

## JPDB Anchor

- **JPDB itself is excluded from coverage quality checks** for other anchors. Its anime/game corpus systematically misses real-world vocabulary: 男性 (man, YOUTUBE rank 1,100) is rank 180,271 in JPDB; 企業 (company) is entirely absent. This is a register mismatch, not a data quality issue.
- **Only ~10.5% zero-missing** at N=0 (vs 14–18% for other anchors) — JPDB's domain specificity means fewer words are covered by all sources.
- N≤3 threshold yields ~2,920 high-confidence words — fewer than other anchors due to JPDB's narrower domain.
- Best used when the learning goal is specifically anime/game/visual novel vocabulary.

## CEJC Anchor

- **~12.4% of CEJC words have zero missing ranks** (across 28 reliable sources after excluding 7 structurally broken ones). These are the most universally attested words across all corpora.
- **7 sources are excluded from quality checks** due to structural incompatibility: AOZORA_BUNKO (kanji-only), NIER (single game, ~10k words), ILYASEMENOV (HTML entities, Wikipedia bias), DD2_MIGAKU_NOVELS (curated learner deck), HERMITDAVE_2016/2018 (morpheme-split tokenization), JPDB (anime/game register misses general vocabulary like 男性, 企業).
- **N≤3 threshold** (missing from at most 3 of the 28 checked sources) yields ~6,047 high-confidence words — a practical working set for vocabulary study.
- CEJC's UniDic lemma forms (其れ、為る、此れ) are distinct from the surface hiragana forms (それ、する、これ) used by other sources; both exist as separate entries in CEJC.

## NETFLIX Anchor

- **17.4% zero-missing** across 28 checked sources (4,355 words) — tied with ANIME_JDRAMA for highest zero-missing rate among all anchors.
- N≤3 threshold yields ~7,712 high-confidence words.
- Very strong overlap with ANIME_JDRAMA anchor — both are subtitle-based with similar genre coverage and nearly identical coverage statistics.
- Good general-purpose anchor for learners who primarily watch Japanese video content.

## YOUTUBE_FREQ_V3 ANCHOR

- **14.9% zero-missing** across 28 checked sources — the highest of all non-CEJC anchors in absolute count (4,463 words).
- N≤3 threshold yields ~7,834 words — one of the largest high-confidence sets across all anchors.
- Top-500 words achieve **70.2% zero-missing** across all 28 sources — basic particles, core verbs, and high-frequency nouns appear universally.
- This anchor was used as the primary reference corpus for the coverage quality experiments (see `experiment/coverage_analysis/`).
- The morpheme-tokenization problem is most visible here: HERMITDAVE sources miss 24.8% of the top-1,000 YouTube words because verbs like 思う, 見る, できる don't exist as tokens in morpheme-split corpora.
