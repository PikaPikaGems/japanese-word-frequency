# Experiments 4 — Dataset Selection: Netflix and Wikipedia

**Goal:** Decide between `NETFLIX` vs `DD2_MORPHMAN_NETFLIX`, and `WIKIPEDIA_V2` vs `ADNO`.

**Scripts:**
- `analyze_netflix.py` → `NETFLIX_ANALYSIS.md`
- `analyze_wikipedia.py` → `WIKIPEDIA_ANALYSIS.md`

Run from repo root:
```
python data/ALL/___experiments4/analyze_netflix.py
python data/ALL/___experiments4/analyze_wikipedia.py
```

---

## Netflix: `NETFLIX` vs `DD2_MORPHMAN_NETFLIX`

**Anchor used:** `ANIME_JDRAMA_anchor/consolidated.csv`
**Reference:** `ANIME_JDRAMA_rank` (widely cited, well-regarded subtitle corpus)

### Spearman Correlation

| Dataset | Valid pairs with ANIME_JDRAMA | ρ vs ANIME_JDRAMA |
|---|---|---|
| `NETFLIX` | 19,513 | **0.7247** |
| `DD2_MORPHMAN_NETFLIX` | 12,004 | 0.6929 |

ρ between NETFLIX and DD2_MORPHMAN_NETFLIX (shared 11,205 words): **0.7958**

### Top-N Jaccard Overlap

| Top-N | NETFLIX ∩ ANIME_JDRAMA | DD2 ∩ ANIME_JDRAMA | NETFLIX ∩ DD2 |
|---|---|---|---|
| 100 | 0.636 | 0.400 | 0.506 |
| 500 | 0.640 | 0.413 | 0.513 |
| 1,000 | 0.635 | 0.422 | 0.534 |
| 5,000 | 0.608 | 0.425 | 0.508 |

### Key Finding: DD2's "Proper Name Filter" Removes Common Words

DD2_MORPHMAN_NETFLIX was expected to differ from NETFLIX mainly by excluding proper names (character names, person names). The analysis checks words that NETFLIX ranks in its top 300 but DD2 either filters out entirely or ranks above 2,000.

**71 such words exist.** Reviewing them reveals the filter is not just removing proper names — it is removing large numbers of common conversational words:

| NETFLIX rank | Word | Reading | DD2 rank |
|---|---|---|---|
| 9 | する | する | 10,746 |
| 17 | ん | ん | absent |
| 31 | いい | いい | 16,719 |
| 33 | なる | なる | 17,060 |
| 55 | お前 | おまえ | absent |
| 57 | けど | けど | absent |
| 68 | 僕 | ぼく | 10,587 |
| 148 | 帰る | かえる | absent |
| 150 | だから | だから | absent |
| 176 | 本当に | ほんとうに | absent |
| 200 | 信じる | しんじる | absent |
| 211 | 私たち | わたしたち | absent |
| 212 | お願い | おねがい | absent |
| 278 | パパ | パパ | absent |

Words like する (rank 9), いい, なる, けど, だから, 本当に, お願い are core everyday vocabulary, not proper names. Their near-absence in DD2 suggests the Morphman/UniDic lemmatization pipeline is **merging these into parent entries or failing to match them** across the source files — not filtering them as names. The result is significant gaps in conversational vocabulary coverage.

### Conclusion: **Recommend `NETFLIX`**

- Higher Spearman correlation with ANIME_JDRAMA (0.7247 vs 0.6929)
- Far better coverage: 19,513 valid pairs vs 12,004 — 63% more
- Consistently higher Jaccard overlap with ANIME_JDRAMA at every threshold
- The 71 missing/demoted words in DD2 are primarily common speech — not noise

`DD2_MORPHMAN_NETFLIX` has a coverage problem that outweighs its lemmatization advantage.

---

## Wikipedia: `WIKIPEDIA_V2` vs `ADNO`

**Anchor used:** `BCCWJ_LUW_anchor/consolidated.csv`
**Primary reference:** `BCCWJ_LUW_rank` (authoritative written Japanese, NINJAL)
**Secondary reference:** `RSPEER` (multi-source aggregate)

### Spearman Correlation

| Dataset | n vs BCCWJ_LUW | ρ vs BCCWJ_LUW | n vs RSPEER | ρ vs RSPEER |
|---|---|---|---|---|
| `WIKIPEDIA_V2` | 11,640 | **0.4108** | 10,368 | **0.6761** |
| `ADNO` | 10,364 | 0.3954 | 9,486 | 0.6728 |

ρ between WIKIPEDIA_V2 and ADNO (shared 9,830 words): **0.8745**

The two datasets strongly agree with each other (ρ=0.875), so the choice between them is largely about coverage margin and what each uniquely captures.

### Top-N Jaccard Overlap

| Top-N | WIKIPEDIA_V2 ∩ BCCWJ_LUW | ADNO ∩ BCCWJ_LUW | WIKIPEDIA_V2 ∩ ADNO |
|---|---|---|---|
| 100 | 0.210 | 0.200 | 0.470 |
| 500 | 0.201 | 0.174 | 0.623 |
| 1,000 | 0.227 | 0.187 | 0.640 |
| 5,000 | 0.319 | 0.289 | 0.711 |

Note: low Jaccard against BCCWJ_LUW (~0.21) is expected and normal — Wikipedia vocabulary is topic-specific and encyclopedic, quite different from the balanced written corpus. Both datasets show the same pattern.

### Discrepancy Analysis (Top 500)

**In WIKIPEDIA_V2 top 500, absent from ADNO (19 words):**

Notable examples: として (#24), という (#47), により (#69), による (#76), によって (#87), について (#138), において (#143), における (#226), に対して (#370), とともに (#453)

These are compound postpositional phrases (複合助詞) that appear heavily in formal written Japanese and Wikipedia prose — *because of X*, *regarding X*, *in the context of X*. WIKIPEDIA_V2 captures this grammar layer; ADNO does not.

Also present: 株式会社 (#178), 小学校 (#195), 中学校 (#302), 所在地 (#339), アメリカ合衆国 (#496) — classic high-frequency Wikipedia article vocabulary (companies, schools, locations, countries).

**In ADNO top 500, absent from WIKIPEDIA_V2 (3 words):**

なっ (#26), 関する (#375), 本作 (#477)

なっ is a morpheme fragment (て-form of なる) — its presence as a top-26 entry in ADNO is arguably noise from imperfect tokenization. 関する and 本作 are legitimate words (ADNO includes them; WIKIPEDIA_V2 likely merges them elsewhere).

### Conclusion: **Recommend `WIKIPEDIA_V2`**

- Marginally higher Spearman correlations on both references
- Better coverage: 11,640 valid pairs vs 10,364 vs BCCWJ_LUW (12% more); 10,368 vs 9,486 vs RSPEER (9% more)
- Captures compound postpositions central to formal written/encyclopedic Japanese (として, という, により, etc.) — ADNO misses all of these in its top 500
- ADNO's unique top-500 entries are 3 words, one of which (なっ) appears to be a tokenization artifact
- Larger source coverage (~850k entries vs unstated for ADNO)

ADNO is a solid dataset and fully compatible with WIKIPEDIA_V2 (ρ=0.875), but WIKIPEDIA_V2 strictly dominates on every measured dimension.
