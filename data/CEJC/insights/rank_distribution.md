# Rank Distribution Analysis

**Source:** CEJC — Corpus of Everyday Japanese Conversation

The CEJC dataset uses **standard competition ranking (1224-ranking)**: words with the same corpus frequency share the same rank, and the next rank skips accordingly. This contrasts with dense ranking (1223), where the next rank would be +1 regardless of ties.

The consequence: while the highest rank value is **20,704**, there are only **719 distinct frequency levels** across all **29,534 entries**. At the bottom of the frequency spectrum, thousands of rare words all appear the same number of times — and all share one enormous rank tier.

## Dataset Overview

| Metric                       | Value  |
| ---------------------------- | ------ |
| Total entries (rows)         | 29,534 |
| Unique rank values           | 719    |
| Highest rank value           | 20,704 |
| Ranks with exactly 1 entry   | 430    |
| Ranks with 2+ entries (ties) | 289    |
| Entries caught in tie-groups | 29,104 |

## Largest Tie-Groups

The following ranks have the most entries sharing the same rank value. Each group represents words that appeared an identical number of times in the corpus. The enormous size of the bottom tier — where thousands of words all appeared just once or twice — is the defining feature of this dataset.

| Rank   | Entries sharing this rank | Corpus freq (each) | % of dataset | Cumulative % |
| ------ | ------------------------- | ------------------ | ------------ | ------------ |
| 20,704 | 8,831                     | 1                  | 29.9%        | 29.9%        |
| 16,266 | 4,438                     | 2                  | 15.0%        | 44.9%        |
| 13,446 | 2,820                     | 3                  | 9.5%         | 54.5%        |
| 11,455 | 1,991                     | 4                  | 6.7%         | 61.2%        |
| 10,047 | 1,408                     | 5                  | 4.8%         | 66.0%        |
| 8,967  | 1,080                     | 6                  | 3.7%         | 69.6%        |
| 8,120  | 847                       | 7                  | 2.9%         | 72.5%        |
| 7,460  | 660                       | 8                  | 2.2%         | 74.7%        |
| 6,881  | 579                       | 9                  | 2.0%         | 76.7%        |
| 6,453  | 428                       | 10                 | 1.4%         | 78.2%        |
| 6,059  | 394                       | 11                 | 1.3%         | 79.5%        |
| 5,687  | 372                       | 12                 | 1.3%         | 80.7%        |
| 5,383  | 304                       | 13                 | 1.0%         | 81.8%        |
| 5,116  | 267                       | 14                 | 0.9%         | 82.7%        |
| 4,880  | 236                       | 15                 | 0.8%         | 83.5%        |

```
rank 20,704  ██████████████████████████████████████████████████  8831.0  (35.8%)
rank 16,266  █████████████████████████                           4438.0  (18.0%)
rank 13,446  ████████████████                                    2820.0  (11.4%)
rank 11,455  ███████████                                         1991.0  (8.1%)
rank 10,047  ████████                                            1408.0  (5.7%)
rank  8,967  ██████                                              1080.0  (4.4%)
rank  8,120  █████                                                847.0  (3.4%)
rank  7,460  ████                                                 660.0  (2.7%)
rank  6,881  ███                                                  579.0  (2.3%)
rank  6,453  ██                                                   428.0  (1.7%)
rank  6,059  ██                                                   394.0  (1.6%)
rank  5,687  ██                                                   372.0  (1.5%)
rank  5,383  ██                                                   304.0  (1.2%)
rank  5,116  ██                                                   267.0  (1.1%)
rank  4,880  █                                                    236.0  (1.0%)
```

## Singleton vs Tie-Group Entries

Words at the top of the frequency spectrum are unique enough to have their own rank (singletons). Words at the bottom share ranks with hundreds or thousands of others that appeared equally rarely.

| Category                     | Distinct ranks | Total entries | % of entries |
| ---------------------------- | -------------- | ------------- | ------------ |
| Singleton ranks (no ties)    | 430            | 430           | 1.5%         |
| Tie-group ranks (2+ entries) | 289            | 29,104        | 98.5%        |

## Tie-Group Size Distribution

How many tie-groups exist of each size? Most tie-groups are small (2–10 entries), but a handful of massive groups at the bottom of the frequency list dominate the dataset.

| Group size | # of rank tiers | Total entries in these tiers |
| ---------- | --------------- | ---------------------------- |
| 2–5        | 152             | 426                          |
| 6–20       | 72              | 752                          |
| 21–100     | 41              | 1,883                        |
| 101–500    | 15              | 3,389                        |
| 501–2000   | 6               | 6,565                        |
| 2001–5000  | 2               | 7,258                        |
| 5000+      | 1               | 8,831                        |

## Key Insights

- **The dataset uses standard competition (1224) ranking, not dense ranking.** There are 719 distinct frequency levels but the highest rank value is 20,704 — a gap of 19,985 — caused entirely by tie-induced rank jumps.

- **The largest tie-group (rank 20,704) contains 8,831 entries** — 29.9% of the entire dataset. Every word in this group appeared exactly 1 time(s) in the corpus. This is the long tail of rare vocabulary in action.

- **Only 430 words have a frequency unique enough to earn their own rank.** These are the high-frequency words where even small differences in usage count result in distinct rankings.

- **The last singleton rank is 862**, meaning words ranked 863 and below all share their rank with at least one other word. Past this point, the corpus can no longer distinguish relative frequency.
