# Source Correlation Analysis

Pairwise Spearman rank correlations between all sources with ≥5,000 words in common. A correlation near 1.0 means the two sources rank words nearly identically; near 0 means their rankings are essentially unrelated.

**Sources analyzed:** 35 (≥5,000 words coverage)
**Pairs computed:** 595

## Top 20 Most Correlated Pairs (most similar sources)

High correlation often indicates near-duplicate sources (same underlying data in different formats) or sources from the same domain.

| r     | Source A             | Source B                  | Shared words |
| ----- | -------------------- | ------------------------- | ------------ |
| 0.995 | DD2_YOMICHAN_SHONEN  | DD2_YOMICHAN_SHONEN_STARS | 11,740       |
| 0.984 | DAVE_DOEBRICK        | NETFLIX                   | 11,529       |
| 0.981 | HERMITDAVE_2016      | HERMITDAVE_2018           | 9,818        |
| 0.945 | DD2_MIGAKU_NETFLIX   | DD2_MORPHMAN_NETFLIX      | 10,490       |
| 0.931 | DD2_MORPHMAN_SHONEN  | DD2_YOMICHAN_SHONEN       | 9,906        |
| 0.922 | DD2_MORPHMAN_SHONEN  | DD2_YOMICHAN_SHONEN_STARS | 9,959        |
| 0.910 | DD2_MORPHMAN_SOL     | DD2_YOMICHAN_SOL          | 10,049       |
| 0.906 | DAVE_DOEBRICK        | DD2_MIGAKU_NETFLIX        | 11,057       |
| 0.898 | KOKUGOJITEN          | MONODICTS                 | 9,570        |
| 0.896 | DD2_MIGAKU_NETFLIX   | NETFLIX                   | 10,975       |
| 0.891 | DD2_MORPHMAN_NOVELS  | INNOCENT_RANKED           | 9,505        |
| 0.885 | DD2_MORPHMAN_NOVELS  | DD2_YOMICHAN_NOVELS       | 10,609       |
| 0.875 | DAVE_DOEBRICK        | DD2_MORPHMAN_NETFLIX      | 8,833        |
| 0.874 | DD2_MORPHMAN_NOVELS  | NOVELS                    | 10,589       |
| 0.869 | DD2_MORPHMAN_NETFLIX | NETFLIX                   | 8,779        |
| 0.869 | ADNO                 | WIKIPEDIA_V2              | 10,141       |
| 0.852 | DD2_YOMICHAN_NOVELS  | NOVELS                    | 11,144       |
| 0.850 | DD2_YOMICHAN_NOVELS  | INNOCENT_RANKED           | 9,567        |
| 0.837 | DD2_YOMICHAN_VN      | VN_FREQ                   | 10,562       |
| 0.828 | NAROU                | VN_FREQ                   | 13,272       |

## Bottom 20 Least Correlated Pairs (most divergent sources)

Low correlation indicates sources from very different domains — e.g. media transcriptions vs. dictionary headwords.

| r     | Source A                  | Source B        | Shared words |
| ----- | ------------------------- | --------------- | ------------ |
| 0.137 | BCCWJ                     | ILYASEMENOV     | 3,801        |
| 0.136 | DD2_MORPHMAN_SOL          | ILYASEMENOV     | 2,584        |
| 0.134 | DD2_MIGAKU_NOVELS         | ILYASEMENOV     | 852          |
| 0.132 | ANIME_JDRAMA              | ILYASEMENOV     | 4,016        |
| 0.126 | ILYASEMENOV               | MONODICTS       | 3,528        |
| 0.114 | DD2_MORPHMAN_SHONEN       | ILYASEMENOV     | 2,593        |
| 0.106 | ILYASEMENOV               | KOKUGOJITEN     | 3,556        |
| 0.102 | ILYASEMENOV               | NOVELS          | 4,168        |
| 0.099 | DD2_MORPHMAN_NOVELS       | ILYASEMENOV     | 3,877        |
| 0.097 | CHRISKEMPSON              | ILYASEMENOV     | 3,559        |
| 0.094 | DD2_YOMICHAN_SHONEN       | ILYASEMENOV     | 3,765        |
| 0.092 | DD2_YOMICHAN_SHONEN_STARS | ILYASEMENOV     | 3,866        |
| 0.090 | ILYASEMENOV               | INNOCENT_RANKED | 3,524        |
| 0.085 | ILYASEMENOV               | JITEN_ANIME     | 3,600        |
| 0.083 | ILYASEMENOV               | NIER            | 2,046        |
| 0.083 | ILYASEMENOV               | VN_FREQ         | 3,712        |
| 0.080 | ILYASEMENOV               | NAROU           | 3,738        |
| 0.077 | DD2_YOMICHAN_NOVELS       | ILYASEMENOV     | 4,091        |
| 0.058 | H_FREQ                    | ILYASEMENOV     | 2,657        |
| 0.045 | DD2_YOMICHAN_VN           | ILYASEMENOV     | 3,476        |

## Within-Group vs Cross-Group Correlation

Average Spearman r for pairs within the same media-type group vs. across groups. High within-group r confirms sources of the same type agree with each other.

- **Within-group average r:** 0.690 (66 pairs)
- **Cross-group average r:** 0.520 (529 pairs)

| Group               | Avg within-group r | Sources |
| ------------------- | ------------------ | ------- |
| Written/Wikipedia   | 0.467              | 4       |
| Literature/Novels   | 0.730              | 7       |
| Anime/Drama         | 0.779              | 7       |
| Netflix             | 0.904              | 3       |
| Slice of Life Anime | 0.910              | 2       |
| Visual Novels       | 0.837              | 2       |
| YouTube             | 0.777              | 2       |
| Dictionary/Balanced | 0.519              | 4       |
| Other               | 0.449              | 4       |

## Notable Observations

### Near-duplicate sources (r ≥ 0.95)

These pairs are almost certainly the same underlying data published in different formats. Including both in a weighted average would double-count that source's signal.

- **DD2_YOMICHAN_SHONEN ↔ DD2_YOMICHAN_SHONEN_STARS**: r=0.995 (11,740 shared words)
- **DAVE_DOEBRICK ↔ NETFLIX**: r=0.984 (11,529 shared words)
- **HERMITDAVE_2016 ↔ HERMITDAVE_2018**: r=0.981 (9,818 shared words)

