# source_insights

Deep analysis scripts examining relationships between the 35 frequency sources: how they agree, where they diverge, and what vocabulary each domain prioritizes.

## Motivation

With 35 sources covering different media types (spoken, anime, literature, web, games), there are natural clusters of agreement and disagreement. These scripts answer questions like:
- Which sources are nearly redundant with each other?
- Which words are universally frequent vs. domain-specific?
- Does spoken Japanese vocabulary look fundamentally different from written?
- What words are distinctive to each media type?

## Note on Paths

These scripts were originally written to run from `data/ALL/` and reference `consolidated.csv` and `categorized.csv` (the CEJC-anchored files). After reorganization, paths in the scripts will need to be updated if run from their new location.

---

## Scripts (`scripts/`)

### `utils.py`
Shared helper library. Provides `markdown_table()` and `ascii_bar_chart()` used by all other scripts.

---

### `variance_analysis.py` → `outputs/variance_analysis.md`

**Methodology:** For each word in `consolidated.csv`, computes:
- **Normalized rank variance**: ranks are normalized per-source to [0,1], then std dev computed across all sources. Low = universally consistent position.
- **Tier variance**: std dev of tier values (1–5) across sources, excluding tier-1 (absent/rare is indistinguishable from missing). High = strong domain-specificity.
- **Basic-tier count**: how many sources assign tier 5 (rank ≤ 1,000).

Reports top-30 words in each category.

**Output interpretation:**
- *Low variance words*: reliable learning targets regardless of your study source (tend to be abstract Sino-Japanese vocabulary: 判断, 原因, 理解)
- *High variance words*: domain-specific or kanji/kana spelling alternates — common in one medium, rare in another (e.g., 其れ is frequent in Aozora literature but rare in modern corpora)
- *Universal core words*: appear as tier-5 "basic" in 20+ sources — the safest high-priority targets

---

### `source_coverage.py` → `outputs/source_coverage.md`

**Methodology:** For each of the 35 sources, counts how many of the 27,988 CEJC words have a valid (non -1) rank. Generates:
- Sorted bar chart of coverage % per source
- Coverage histogram: how many sources cover each word

**Output interpretation:** Coverage % directly indicates how useful a source is for CEJC-anchored study. Low coverage (NIER at ~18%) means most words will have no rank from that source. High coverage (JPDB, ANIME_JDRAMA at 70–80%+) means it's a reliable signal for the majority of frequent words.

---

### `spoken_vs_written.py` → `outputs/spoken_vs_written.md`

**Methodology:** Compares CEJC's spoken `combined_rank` against the average rank across all 35 external (written/media) sources. For each word with 5+ external sources:
- Computes `spoken_rank - external_mean_rank`
- Words with large positive delta are ranked much higher by CEJC than external sources (speech-specific vocabulary)
- Words with large negative delta are ranked much higher by external sources (written/media-specific vocabulary)

Also reports words present only in CEJC (absent from all 35 external sources).

**Output interpretation:** Speech-dominant words tend to be discourse markers, fillers, and conversational grammar. Written/media-dominant words tend to be technical, formal, or narrative vocabulary. Words present only in CEJC may represent spoken contractions or transcription artifacts.

---

### `source_correlations.py` → `outputs/source_correlations.md`

**Methodology:** For all pairs of sources with ≥500 shared words, computes Spearman rank correlation. Reports:
- Top 20 most correlated pairs (near-redundant or same-domain sources)
- Bottom 20 least correlated pairs (most divergent source types)
- Within-group vs. cross-group correlation summary by media type (Written/Wikipedia, Literature/Novels, Anime/Drama, Games/JPDB, Subtitle/Netflix, YouTube)

**Output interpretation:** High correlation = the two sources rank words similarly — one may be partially redundant. Low correlation = the sources capture fundamentally different vocabulary priorities. Cross-group pairs (e.g., Wikipedia vs. Anime) will predictably correlate less than within-group pairs.

---

### `media_profiles.py` → `outputs/media_profiles.md`

**Methodology:** Groups sources into media types (Written/Wikipedia, Literature/Novels, Anime/Drama, Games, Subtitles, YouTube). For each group, finds words that group ranks unusually **high** relative to all other groups combined — the "signature vocabulary" of that media type.

Distinctiveness score = `mean_rank_in_group - mean_rank_outside_group` (lower = more distinctive to that group).

**Output interpretation:** Each group's distinctive words characterize its domain. Anime/Drama will show character speech patterns and onomatopoeia; Literature will show archaic vocabulary and formal grammar; Wikipedia/Web will show technical and encyclopedic terms. Use these profiles to choose which anchor best matches your learning goals.

---

## Outputs (`outputs/`)

Pre-generated markdown reports from the last script run:

| File | Generated by |
|---|---|
| `variance_analysis.md` | `variance_analysis.py` |
| `source_coverage.md` | `source_coverage.py` |
| `spoken_vs_written.md` | `spoken_vs_written.py` |
| `source_correlations.md` | `source_correlations.py` |
| `media_profiles.md` | `media_profiles.py` |

To regenerate, run each script from `data/ALL/` (paths in scripts are relative to that directory):

```
cd data/ALL
python3 experiment/source_insights/scripts/variance_analysis.py > experiment/source_insights/outputs/variance_analysis.md
```
