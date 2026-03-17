## Notable Insights

### Coverage is concentrated (RSPEER)

80% of Japanese text is covered by just ~1,700 words; 90% by ~5,000; 95% by ~9,700; 98% by ~16,000. Focusing on the top 5,000 words gives strong practical coverage for everyday reading.

([Full coverage analysis](data/RSPEER/INSIGHTS.md))

### CEJC rankings are heavily tied at the bottom

Only 430 of 29,534 entries have a unique rank. Most entries share ranks due to tied low-frequency counts, creating a 19,985-rank gap. This is a known artifact of standard competition ranking (1224 style).

([Rank distribution analysis](data/CEJC/insights/rank_distribution.md))

### Cross-source agreement is only partial — and datasets index words differently

> See [Data Quality Notes](#data-quality-notes) for why JPDB scores far lower than every other source. Subtitle sources (ANIME, NETFLIX, YOUTUBE) also contain inflected verb forms and proper nouns not found as dictionary headwords (evidenced by their 6–11% kana gaps), but JPDB exhibits this most severely — inflected forms dominate its top ranks.

**Reading-aware match** (surface form OR kana reading, readings normalized to hiragana): a word in source A counts as matching source B if its surface form equals either the term/key or the reading in B. This catches cases like RSPEER `くれる` ↔ CEJC `呉れる` or JPDB `今` (reading `いま`) ↔ RSPEER `いま`.

| Comparison    | Top 5k | Top 10k | Top 25k |
| ------------- | ------ | ------- | ------- |
| RSPEER ∩ JPDB | 49.7%  | 49.9%   | 50.4%   |
| RSPEER ∩ CEJC | 53.6%  | 51.1%   | 48.8%   |
| JPDB ∩ CEJC   | 54.6%  | 52.1%   | 54.1%   |
| All three     | 40.3%  | 39.9%   | 40.7%   |

Caveats: **Homophones** — the same kana reading can belong to unrelated words (e.g. particle `ば` vs noun `場`), so reading-based matching can introduce false positives.

([Cross-dataset comparison](data/RSPEER/INSIGHTS.md))

### Gender differences in CEJC speech: some robust, some confounded (CEJC)

Some findings are well-supported and linguistically established: gendered first-person pronouns (俺/僕 strongly male, 私 strongly female) and gendered sentence-final particles (ぞ/ぜ male, かしら female) show extreme M/F PMW ratios (3–30×). These reflect real speech style differences.

However, the methodology (raw PMW ratio across all speech by gender) does **not** control for conversation domain. Work/meeting vocabulary (会議, 担当, チーム) skewing male, and food/home vocabulary (野菜, 卵, 菓子) skewing female, may reflect which domains male vs. female participants in this corpus happened to participate in — not an intrinsic property of how men and women speak. Core function words show very little gender skew regardless.

([Demographic analysis](data/CEJC/insights/demographic_analysis.md))

### Pairwise overlap across all anchors (experiments1)

> JPDB's uniformly low scores (~25–45%) are explained in [Data Quality Notes](#data-quality-notes). Subtitle sources also contain inflected forms and proper nouns, but JPDB is the most extreme case — inflected forms like `だった` and `だろう` rank in its top 50.

[`data/ALL/___experiments1/anchor_pairwise_overlap.py`](data/ALL/___experiments1/anchor_pairwise_overlap.py) — reading-aware pairwise intersection between all 10 anchor datasets. Row = source A (denominator); cell = % of A's top-N that appear in B's top-N.

**Top-5k:**

|                     | CC100 | CEJC  | YOUTUBE_FREQ_V3 | WIKIPEDIA_V2 | NETFLIX | BCCWJ_LUW | BCCWJ_SUW | ANIME_JDRAMA | RSPEER | JPDB  |
| ------------------- | ----- | ----- | --------------- | ------------ | ------- | --------- | --------- | ------------ | ------ | ----- |
| **CC100**           | —     | 63.1% | 75.0%           | 58.3%        | 57.5%   | 68.1%     | 77.3%     | 54.5%        | 65.2%  | 32.5% |
| **CEJC**            | 61.4% | —     | 61.3%           | 47.9%        | 52.9%   | 55.9%     | 66.2%     | 51.0%        | 53.9%  | 34.6% |
| **YOUTUBE_FREQ_V3** | 77.0% | 65.0% | —               | 57.8%        | 62.6%   | 67.9%     | 73.0%     | 60.6%        | 67.3%  | 37.3% |
| **WIKIPEDIA_V2**    | 62.8% | 53.1% | 60.3%           | —            | 54.6%   | 54.4%     | 66.0%     | 52.8%        | 65.4%  | 26.7% |
| **NETFLIX**         | 61.7% | 58.8% | 64.8%           | 54.6%        | —       | 62.6%     | 64.4%     | 79.9%        | 64.4%  | 41.8% |
| **BCCWJ_LUW**       | 64.6% | 54.2% | 62.2%           | 47.9%        | 55.2%   | —         | 70.6%     | 53.0%        | 52.8%  | 29.8% |
| **BCCWJ_SUW**       | 77.9% | 68.0% | 71.2%           | 62.6%        | 60.4%   | 74.4%     | —         | 56.8%        | 64.4%  | 31.4% |
| **ANIME_JDRAMA**    | 58.4% | 56.8% | 62.5%           | 51.8%        | 79.9%   | 60.4%     | 60.8%     | —            | 60.7%  | 42.0% |
| **RSPEER**          | 67.9% | 58.1% | 68.4%           | 63.6%        | 63.3%   | 58.7%     | 66.7%     | 60.0%        | —      | 33.3% |
| **JPDB**            | 26.9% | 30.2% | 29.6%           | 19.5%        | 32.3%   | 26.6%     | 26.3%     | 32.1%        | 26.1%  | —     |

**Top-10k:**

|                     | CC100 | CEJC  | YOUTUBE_FREQ_V3 | WIKIPEDIA_V2 | NETFLIX | BCCWJ_LUW | BCCWJ_SUW | ANIME_JDRAMA | RSPEER | JPDB  |
| ------------------- | ----- | ----- | --------------- | ------------ | ------- | --------- | --------- | ------------ | ------ | ----- |
| **CC100**           | —     | 61.4% | 74.8%           | 60.2%        | 59.6%   | 68.5%     | 75.9%     | 55.1%        | 65.7%  | 35.5% |
| **CEJC**            | 58.9% | —     | 57.2%           | 47.8%        | 49.4%   | 51.7%     | 63.2%     | 48.0%        | 51.8%  | 35.4% |
| **YOUTUBE_FREQ_V3** | 76.4% | 61.7% | —               | 61.0%        | 63.2%   | 65.5%     | 70.3%     | 60.1%        | 67.7%  | 40.4% |
| **WIKIPEDIA_V2**    | 65.1% | 54.3% | 64.2%           | —            | 61.1%   | 56.5%     | 67.9%     | 59.0%        | 70.0%  | 32.9% |
| **NETFLIX**         | 63.0% | 55.3% | 64.9%           | 60.1%        | —       | 61.5%     | 63.5%     | 79.4%        | 66.1%  | 44.4% |
| **BCCWJ_LUW**       | 64.3% | 50.3% | 59.8%           | 48.6%        | 54.1%   | —         | 67.4%     | 51.3%        | 51.8%  | 31.1% |
| **BCCWJ_SUW**       | 76.7% | 66.2% | 69.1%           | 64.1%        | 60.4%   | 72.1%     | —         | 56.5%        | 64.5%  | 34.7% |
| **ANIME_JDRAMA**    | 58.6% | 53.8% | 61.9%           | 57.8%        | 79.6%   | 58.9%     | 59.8%     | —            | 62.2%  | 44.2% |
| **RSPEER**          | 67.8% | 56.8% | 68.7%           | 67.5%        | 65.5%   | 58.1%     | 66.2%     | 61.7%        | —      | 37.1% |
| **JPDB**            | 29.3% | 30.8% | 32.0%           | 24.1%        | 34.0%   | 27.4%     | 29.0%     | 33.2%        | 28.9%  | —     |

**Top-15k:**

|                     | CC100 | CEJC  | YOUTUBE_FREQ_V3 | WIKIPEDIA_V2 | NETFLIX | BCCWJ_LUW | BCCWJ_SUW | ANIME_JDRAMA | RSPEER | JPDB  |
| ------------------- | ----- | ----- | --------------- | ------------ | ------- | --------- | --------- | ------------ | ------ | ----- |
| **CC100**           | —     | 61.0% | 75.0%           | 60.3%        | 61.5%   | 69.1%     | 74.7%     | 56.7%        | 65.4%  | 36.9% |
| **CEJC**            | 57.7% | —     | 55.5%           | 47.6%        | 48.8%   | 49.7%     | 63.3%     | 46.9%        | 50.6%  | 35.7% |
| **YOUTUBE_FREQ_V3** | 76.4% | 60.7% | —               | 61.5%        | 64.3%   | 65.1%     | 68.8%     | 60.9%        | 67.4%  | 41.6% |
| **WIKIPEDIA_V2**    | 65.0% | 54.7% | 64.5%           | —            | 64.0%   | 57.2%     | 67.4%     | 61.4%        | 71.1%  | 35.3% |
| **NETFLIX**         | 64.1% | 54.6% | 65.3%           | 62.4%        | —       | 61.4%     | 63.6%     | 78.8%        | 66.8%  | 45.5% |
| **BCCWJ_LUW**       | 64.1% | 48.5% | 58.6%           | 48.6%        | 53.9%   | —         | 65.7%     | 50.9%        | 51.2%  | 30.9% |
| **BCCWJ_SUW**       | 75.2% | 66.9% | 67.5%           | 63.8%        | 61.2%   | 71.0%     | —         | 56.7%        | 63.9%  | 36.6% |
| **ANIME_JDRAMA**    | 59.6% | 52.9% | 62.1%           | 59.7%        | 79.2%   | 58.7%     | 59.4%     | —            | 62.2%  | 44.4% |
| **RSPEER**          | 67.3% | 56.1% | 68.3%           | 68.7%        | 66.6%   | 57.9%     | 65.5%     | 62.1%        | —      | 38.8% |
| **JPDB**            | 30.5% | 31.3% | 32.7%           | 26.3%        | 35.1%   | 27.3%     | 30.9%     | 33.4%        | 29.9%  | —     |

**Top-25k:**

|                     | CC100 | CEJC  | YOUTUBE_FREQ_V3 | WIKIPEDIA_V2 | NETFLIX | BCCWJ_LUW | BCCWJ_SUW | ANIME_JDRAMA | RSPEER | JPDB  |
| ------------------- | ----- | ----- | --------------- | ------------ | ------- | --------- | --------- | ------------ | ------ | ----- |
| **CC100**           | —     | 61.6% | 75.8%           | 61.7%        | 64.6%   | 69.0%     | 73.8%     | 60.6%        | 65.9%  | 39.8% |
| **CEJC**            | 57.6% | —     | 54.5%           | 48.2%        | 49.1%   | 49.0%     | 64.5%     | 48.0%        | 50.3%  | 36.0% |
| **YOUTUBE_FREQ_V3** | 75.9% | 59.1% | —               | 61.9%        | 65.7%   | 64.2%     | 66.7%     | 63.1%        | 67.2%  | 43.2% |
| **WIKIPEDIA_V2**    | 65.0% | 54.7% | 64.8%           | —            | 65.9%   | 57.9%     | 66.3%     | 64.3%        | 72.4%  | 37.7% |
| **NETFLIX**         | 65.5% | 53.9% | 66.0%           | 63.9%        | —       | 61.9%     | 62.8%     | 79.6%        | 66.7%  | 45.9% |
| **BCCWJ_LUW**       | 62.3% | 46.8% | 57.2%           | 48.9%        | 54.5%   | —         | 61.9%     | 52.0%        | 50.4%  | 31.5% |
| **BCCWJ_SUW**       | 73.2% | 67.9% | 65.5%           | 63.0%        | 61.1%   | 67.7%     | —         | 57.8%        | 62.8%  | 39.5% |
| **ANIME_JDRAMA**    | 61.4% | 52.5% | 63.1%           | 62.0%        | 79.5%   | 59.3%     | 59.4%     | —            | 63.1%  | 44.6% |
| **RSPEER**          | 66.1% | 54.5% | 67.2%           | 69.7%        | 66.5%   | 57.1%     | 63.5%     | 63.2%        | —      | 39.5% |
| **JPDB**            | 33.5% | 32.6% | 35.0%           | 29.6%        | 36.8%   | 28.9%     | 35.1%     | 35.0%        | 31.8%  | —     |

**Key observations:**

- **NETFLIX ↔ ANIME_JDRAMA** is the highest-overlap pair (~79–80% both directions at all tiers) — both are subtitle corpora covering similar spoken registers
- **JPDB rows score 25–45%** across all partners at all tiers, far below every other anchor, because it uses a different vocabulary model (surface forms vs lemmas)
- **YOUTUBE_FREQ_V3 and CC100** show strong mutual coverage (~75–77% / ~66–76%), both capturing broad everyday language across many domains
- **WIKIPEDIA_V2 ↔ RSPEER** is notably high (~70–72% at top-10k and above), consistent with both drawing from written, encyclopedic text
- **CEJC rows are consistently the lowest** among general-purpose anchors (~55–65%), reflecting spoken-only UniDic lemma forms (e.g. 其れ, 為る) that diverge from the surface forms used by written and subtitle sources
- **BCCWJ_SUW scores significantly higher than BCCWJ_LUW** across most partners (~73–78% vs ~62–65% at top-5k) because SUW's fine morphological segmentation produces more particles and grammatical morphemes that appear universally across all corpora; LUW's compound units are more content-word-specific and miss more domain-specific sources
- **The matrix is asymmetric**: BCCWJ_SUW → CC100 is 78% but CC100 → BCCWJ_SUW is 77% at top-5k; ANIME_JDRAMA → NETFLIX is ~79% but NETFLIX → ANIME_JDRAMA is also ~79% — the subtitle pair happens to be nearly symmetric, while written ↔ spoken pairs diverge more
