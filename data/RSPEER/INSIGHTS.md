# Data Insights — wordfreq Japanese Dataset

**Dataset:** `top_25000_japanese.csv` — 25,000 most common Japanese words with `frequency` (0–1) and `zipf_frequency` (0–8), generated via the [rspeer/wordfreq](https://github.com/rspeer/wordfreq) library.

---

## 1. Zipf Distribution

![Zipf Distribution](plot_zipf_distribution.png)

The curve is near-linear on a log-log scale, confirming Zipf's law holds well for Japanese. The slope flattens slightly in the top 10 words (particles and conjunctions dominate), then drops steeply before leveling off again past rank 1,000.

Natural vocabulary tiers visible on the curve:
- **Top 1k:** zipf ≥ ~5.1 — core grammar words and highest-frequency vocabulary
- **1k–5k:** zipf ~4.2–5.1 — common everyday vocabulary
- **5k–10k:** zipf ~3.9–4.2 — fluent-level vocabulary
- **10k–25k:** zipf ~3.2–3.9 — advanced/rare vocabulary

---

## 2. Frequency Coverage Curve

![Coverage Curve](plot_coverage_curve.png)

Returns sharply diminish past the first few thousand words — the curve is extremely steep early on and nearly flat by 20k.

| Coverage | Words needed |
|----------|-------------|
| 80%      | 1,738        |
| 90%      | 5,062        |
| 95%      | 9,690        |
| 98%      | 16,018       |

For learners: mastering ~5k words covers 90% of encountered text. The jump from 90% to 95% requires ~4,600 more words — a significant effort for modest gains.

---

## 3. Word Length by Frequency Tier

![Word Length by Tier](plot_word_length_by_tier.png)

Mean word length increases consistently as frequency decreases — confirming **Zipf's law of abbreviation** for Japanese:

| Tier     | Mean length |
|----------|------------|
| Top 1k   | 1.92 chars |
| 1k–5k    | 2.30 chars |
| 5k–10k   | 2.49 chars |
| 10k–25k  | 2.84 chars |

The top 1k is dominated by 1- and 2-character words (particles, basic verbs, common kanji). By the 10k–25k tier the distribution spreads noticeably toward 3–6 characters, with a longer tail extending to 13 characters.

---

## 4. Script Type Breakdown

![Script Breakdown](plot_script_breakdown.png)

Overall composition of the 25,000-word list:

| Script   | Share  |
|----------|--------|
| Kanji    | 45.8%  |
| Katakana | 18.9%  |
| Mixed    | 18.3%  |
| Hiragana | 10.2%  |
| Other    | 6.8%   |

Key observations from the stacked bar chart:
- **Hiragana dominates the top 1k** (~29% share) — particles, copulas, and grammatical function words sit at the very top of the frequency list.
- **Hiragana share collapses sharply past rank 1k** — dropping to ~10% in the 1k–5k band as lexical vocabulary takes over.
- **Katakana (loanwords) peaks in the 10k–25k tier** (~29%), confirming the hypothesis that loanwords cluster in lower-frequency ranges.
- **Kanji is consistently dominant across all tiers** (40–50%), reflecting how central kanji-based vocabulary is at every level.

---

## 5. Zipf Score Distribution

![Zipf Histogram](plot_zipf_histogram.png)

The distribution is right-skewed and peaks at zipf ~3.25–3.5. All 25,000 words score ≥ 3.0 by construction (they are the top 25k in the list).

| Threshold | Words above | % of list |
|-----------|------------|-----------|
| zipf ≥ 3.0 | 25,000    | 100.0%    |
| zipf ≥ 4.0 | 7,258     | 29.0%     |
| zipf ≥ 5.0 | 922       | 3.7%      |

For building filtered vocabulary lists:
- A **zipf ≥ 4.0** cutoff yields ~7,250 words — a practical "common vocabulary" set.
- A **zipf ≥ 5.0** cutoff yields only ~920 words — a minimal core list.
- The bulk of the 25k list (71%) falls in the zipf 3.0–4.0 range, making that band the "advanced learner" territory.

---

## 6. Cross-Dataset Comparison

![Cross-Dataset Comparison](plot_cross_dataset_comparison.png)

| Comparison      | Overlap |
|-----------------|---------|
| wordfreq ∩ JPDB | 12,258 / ~25k words |
| wordfreq ∩ CEJC | 11,581 / ~25k words |

Only ~49% of wordfreq words appear in JPDB and ~46% in CEJC. The scatter plots show decent correlation along the diagonal for high-frequency words, but large divergence at lower ranks (red/yellow points far from the diagonal).

Top 10 words with largest wordfreq vs JPDB rank divergence:

| Word  | wordfreq rank | JPDB rank | Divergence |
|-------|--------------|-----------|-----------|
| 先    | 287          | 24,201    | 23,914    |
| 一    | 78           | 23,901    | 23,823    |
| 白    | 826          | 24,301    | 23,475    |
| 女    | 234          | 23,501    | 23,267    |
| おき  | 1,209        | 24,384    | 23,175    |
| ガン  | 1,017        | 24,001    | 22,984    |
| 好き  | 135          | 23,101    | 22,966    |
| 起こし | 1,746       | 24,659    | 22,913    |
| 落とし | 2,012       | 24,884    | 22,872    |
| 界    | 1,699        | 24,529    | 22,830    |

These divergences are primarily because JPDB indexes words by **reading** (kana form), so bare kanji like 先, 一, 白 appear with very low reading frequency in JPDB even though they're common in written text. This is a fundamental difference in tokenization philosophy between the two sources.
