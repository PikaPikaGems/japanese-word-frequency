# Source Correlation Analysis

Pairwise Spearman rank correlations between all sources with ≥5,000 words in common. A correlation near 1.0 means the two sources rank words nearly identically; near 0 means their rankings are essentially unrelated.

**Sources analyzed:** 31 (≥5,000 words coverage)
**Pairs computed:** 465

## Top 20 Most Correlated Pairs (most similar sources)

High correlation often indicates near-duplicate sources (same underlying data in different formats) or sources from the same domain.

| r     | Source A            | Source B                  | Shared words |
| ----- | ------------------- | ------------------------- | ------------ |
| 0.991 | DAVE_DOEBRICK       | NETFLIX                   | 10,767       |
| 0.927 | KOKUGOJITEN         | MONODICTS                 | 8,755        |
| 0.925 | DD2_YOMICHAN_SHONEN | DD2_YOMICHAN_SHONEN_STARS | 10,976       |
| 0.924 | DD2_MORPHMAN_NOVELS | DD2_YOMICHAN_NOVELS       | 9,570        |
| 0.916 | DD2_MORPHMAN_NOVELS | INNOCENT_RANKED           | 8,926        |
| 0.899 | DD2_MORPHMAN_NOVELS | NOVELS                    | 10,127       |
| 0.890 | DAVE_DOEBRICK       | DD2_MIGAKU_NETFLIX        | 10,311       |
| 0.889 | DD2_YOMICHAN_NOVELS | NOVELS                    | 10,141       |
| 0.882 | ADNO                | WIKIPEDIA_V2              | 9,827        |
| 0.875 | DD2_MIGAKU_NETFLIX  | NETFLIX                   | 10,238       |
| 0.873 | DD2_YOMICHAN_NOVELS | INNOCENT_RANKED           | 8,635        |
| 0.844 | INNOCENT_RANKED     | NOVELS                    | 8,943        |
| 0.843 | ANIME_JDRAMA        | DAVE_DOEBRICK             | 9,368        |
| 0.838 | ANIME_JDRAMA        | NETFLIX                   | 9,356        |
| 0.830 | YOUTUBE_FREQ        | YOUTUBE_FREQ_V3           | 11,216       |
| 0.827 | ANIME_JDRAMA        | CHRISKEMPSON              | 8,224        |
| 0.808 | ANIME_JDRAMA        | JITEN_ANIME               | 8,655        |
| 0.804 | AOZORA_BUNKO        | DD2_YOMICHAN_NOVELS       | 6,349        |
| 0.803 | ANIME_JDRAMA        | DD2_YOMICHAN_SHONEN_STARS | 9,051        |
| 0.800 | NAROU               | VN_FREQ                   | 13,247       |

## Bottom 20 Least Correlated Pairs (most divergent sources)

Low correlation indicates sources from very different domains — e.g. media transcriptions vs. dictionary headwords.

| r     | Source A             | Source B             | Shared words |
| ----- | -------------------- | -------------------- | ------------ |
| 0.250 | DD2_MORPHMAN_NETFLIX | WIKIPEDIA_V2         | 7,291        |
| 0.249 | AOZORA_BUNKO         | DD2_MIGAKU_NOVELS    | 848          |
| 0.248 | AOZORA_BUNKO         | DD2_MORPHMAN_SOL     | 5,133        |
| 0.242 | VN_FREQ              | WIKIPEDIA_V2         | 8,567        |
| 0.239 | ADNO                 | DD2_YOMICHAN_VN      | 7,080        |
| 0.229 | DD2_MORPHMAN_SOL     | WIKIPEDIA_V2         | 6,653        |
| 0.221 | DD2_MORPHMAN_NETFLIX | INNOCENT_RANKED      | 7,375        |
| 0.220 | ADNO                 | VN_FREQ              | 8,177        |
| 0.212 | ADNO                 | DD2_MORPHMAN_SOL     | 6,119        |
| 0.208 | DD2_MORPHMAN_NETFLIX | DD2_YOMICHAN_VN      | 8,201        |
| 0.207 | DD2_MORPHMAN_SHONEN  | MONODICTS            | 6,745        |
| 0.204 | ADNO                 | H_FREQ               | 6,134        |
| 0.177 | DD2_MORPHMAN_SHONEN  | KOKUGOJITEN          | 6,552        |
| 0.173 | DD2_MORPHMAN_SOL     | MONODICTS            | 6,614        |
| 0.170 | DD2_MORPHMAN_NETFLIX | H_FREQ               | 7,677        |
| 0.163 | AOZORA_BUNKO         | DD2_MORPHMAN_NETFLIX | 5,772        |
| 0.162 | ADNO                 | DD2_MIGAKU_NOVELS    | 1,678        |
| 0.151 | DD2_MORPHMAN_NETFLIX | MONODICTS            | 7,272        |
| 0.128 | DD2_MORPHMAN_SOL     | KOKUGOJITEN          | 6,447        |
| 0.100 | DD2_MORPHMAN_NETFLIX | KOKUGOJITEN          | 6,991        |

## Within-Group vs Cross-Group Correlation

Average Spearman r for pairs within the same media-type group vs. across groups. High within-group r confirms sources of the same type agree with each other.

- **Within-group average r:** 0.673 (57 pairs)
- **Cross-group average r:** 0.503 (408 pairs)

| Group               | Avg within-group r | Sources |
| ------------------- | ------------------ | ------- |
| Written/Wikipedia   | 0.630              | 3       |
| Literature/Novels   | 0.711              | 7       |
| Anime/Drama         | 0.682              | 7       |
| Netflix             | 0.644              | 3       |
| Slice of Life Anime | 0.672              | 2       |
| Visual Novels       | 0.770              | 2       |
| YouTube             | 0.830              | 2       |
| Dictionary/Balanced | 0.498              | 4       |

## Notable Observations

### Near-duplicate sources (r ≥ 0.95)

These pairs are almost certainly the same underlying data published in different formats. Including both in a weighted average would double-count that source's signal.

- **DAVE_DOEBRICK ↔ NETFLIX**: r=0.991 (10,767 shared words)

