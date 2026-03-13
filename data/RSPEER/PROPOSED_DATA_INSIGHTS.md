# Proposed Data Insights & Graphs for wordfreq Japanese Dataset

## Dataset
`top_25000_japanese.csv` — 25,000 most common Japanese words with `frequency` (0–1) and `zipf_frequency` (0–8).

---

## 1. Zipf Distribution Plot
**Script:** `plot_zipf_distribution.py`

Plot rank (x) vs. zipf_frequency (y) for the top 25,000 words.

- Shows how steeply frequency falls off with rank — expected to follow Zipf's law (roughly linear on a log-log scale).
- Helps identify natural "tiers" of vocabulary (e.g. core 1k, 5k, 10k words).

---

## 2. Frequency Coverage Curve
**Script:** `plot_coverage_curve.py`

Cumulative frequency sum vs. number of words known (x = 1 to 25,000).

- Answers: "If I know the top N words, what % of real text do I cover?"
- Highlight key thresholds: 80%, 90%, 95%, 98% coverage.
- Extremely useful for language learners deciding how many words to study.

---

## 3. Word Length Distribution by Frequency Tier
**Script:** `plot_word_length_by_tier.py`

Histogram of word lengths (in characters) split across frequency tiers (e.g. top 1k, 1k–5k, 5k–10k, 10k–25k).

- Do common words tend to be shorter? Tests a well-known linguistic principle (Zipf's law of abbreviation).
- Reveals structural differences between high- and low-frequency vocabulary.

---

## 4. Script Type Breakdown (Hiragana / Katakana / Kanji / Mixed)
**Script:** `plot_script_breakdown.py`

Classify each word by its writing system and plot:
- Pie chart of script type counts overall.
- Stacked bar chart of script type share across frequency tiers.

- Shows how Kanji-heavy vocabulary is at different frequency levels.
- Katakana loanwords tend to cluster in mid-to-low frequency ranges — this would confirm or challenge that.

---

## 5. Zipf Score Distribution Histogram
**Script:** `plot_zipf_histogram.py`

Histogram of zipf_frequency values across all 25,000 words.

- Shows the density of words at each "difficulty" level.
- Useful for deciding cut-off points for vocabulary lists (e.g. "only include words with zipf ≥ 3.0").

---

## 6. Comparison with Other Datasets (if available)
**Script:** `plot_cross_dataset_comparison.py`

Compare wordfreq rank/frequency against JPDB, CEJC, or other frequency lists already in this repo for overlapping vocabulary.

- Highlights words that are common in one source but rare in another (domain-specific vocabulary).
- Useful for building a robust, source-averaged frequency ranking.
