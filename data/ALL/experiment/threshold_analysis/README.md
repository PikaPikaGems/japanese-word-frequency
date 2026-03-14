# threshold_analysis

Identifies "high-frequency" words that appear robustly across most sources, using a missing-source threshold to filter out poorly-covered words.

## Motivation

Not every word in an anchor list is equally trustworthy. A word ranked #500 in one source but absent from 30 others could be an artifact of that corpus. This experiment defines a threshold N: a word is considered "high-frequency" only if it is missing from **at most N sources**. Lower N = stricter filter, higher confidence subset.

This answers: *"Which words have strong cross-corpus evidence for being frequent?"*

---

## Methodology

For each anchor (CEJC, JPDB, YOUTUBE_FREQ_V3, ANIME_JDRAMA, NETFLIX):

1. Count how many of the 35 sources have a missing rank (`-1`) for each word.
2. Keep only words where `missing_count ≤ N`.
3. Output the filtered word list with all source ranks.

Two thresholds are analyzed:
- **N=2**: Very strict — word must be present in 33+ of 35 sources
- **N=3**: Moderate — word must be present in 32+ of 35 sources

---

## Files

### Analysis Reports (Markdown)

#### `threshold_analysis_N2.md`
Summary for threshold N=2 across all anchors:
- How many words pass the threshold per anchor
- Per-source: % of high-frequency words that are **absent** from that source (reveals which sources have the most gaps even among high-confidence words)

#### `threshold_analysis_N3.md`
Same analysis for threshold N=3 (more inclusive, larger passing set).

**How to interpret:** A source with 0% absent among high-frequency words (e.g., DD2_YOMICHAN_SHONEN_STARS) covers all the most common words well. A source with 60%+ absent (e.g., ILYASEMENOV) is very sparse even for core vocabulary.

---

### Filtered Word Lists (CSV)

#### `threshold_[2|3]_anchor_[ANCHOR].csv`
The words passing the threshold for each anchor, with all 35 source ranks preserved.

| File pattern | Description |
|---|---|
| `threshold_2_anchor_CEJC.csv` | CEJC words present in 33+ sources |
| `threshold_3_anchor_CEJC.csv` | CEJC words present in 32+ sources |
| `threshold_2_anchor_JPDB.csv` | JPDB top-25k words present in 33+ sources |
| `threshold_3_anchor_JPDB.csv` | JPDB top-25k words present in 32+ sources |
| *(same for ANIME_JDRAMA, NETFLIX, YOUTUBE_FREQ_V3)* | |

**How to interpret:** Use these filtered CSVs as high-confidence word lists for study deck generation. The smaller N=2 sets are more conservative; the N=3 sets include more words with only slightly lower confidence. Compare sizes across anchors: a smaller passing set for an anchor means its vocabulary skews more niche/domain-specific.

---

## Example Results (ANIME_JDRAMA, N=3)

- Total anchor words: 25,000
- Passing threshold: ~7,721 (30.9%)
- Best-covered source: DD2_YOMICHAN_SHONEN_STARS (0.0% absent among passing words)
- Worst-covered source: ILYASEMENOV (63.5% absent among passing words)
