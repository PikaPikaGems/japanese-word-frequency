# data_generation

Scripts that build the primary consolidated and categorized CSV files from raw sources.

## Scripts

### `SCRIPT.py`

**Methodology:** Generates `consolidated_anchor_CEJC.csv` using CEJC as the word backbone.

1. Loads JPDB v2 to build a `kanji → kana` fallback table (for cross-script lookups).
2. Reads `data/CEJC/CONSOLIDATED_UNIQUE.csv` to establish word order and CEJC domain/gender rank columns.
3. Loads every `data/RAW/___FILTERED/*/DATA.csv` source (35 sources total).
4. For each CEJC word, looks up its rank in every source — using the kana fallback if the kanji form is absent.
5. Writes one row per CEJC word: all CEJC columns + one rank column per source.

**Output:** `../../consolidated_anchor_CEJC.csv`
- ~27,988 rows (one per CEJC word)
- Columns: `word`, 13 CEJC domain/gender rank columns, then 35 source rank columns
- Missing rank = `-1`

---

### `CATEGORIZED.py`

**Methodology:** Converts rank values in `consolidated_anchor_CEJC.csv` to a 5-tier vocabulary category.

Tier mapping applied to every rank column:

| Tier | Label    | Rank range       |
|------|----------|------------------|
| 5    | basic    | 1 – 1,000        |
| 4    | common   | 1,001 – 4,000    |
| 3    | fluent   | 4,001 – 10,000   |
| 2    | advanced | 10,001 – 25,000  |
| 1    | rare     | 25,001+ or absent|

**Output:** `../../categorized_anchor_CEJC.csv`
- Same structure as `consolidated_anchor_CEJC.csv` but all rank values replaced with tier numbers (1–5)
- Useful for categorical comparison and learning prioritization

---

### `make_anchored.py`

**Methodology:** Generates consolidated + categorized files for four non-CEJC anchors: `JPDB`, `YOUTUBE_FREQ_V3`, `ANIME_JDRAMA`, `NETFLIX`.

Unlike SCRIPT.py (which anchors on CEJC word order), each run here takes one source's top-N words and looks up every other source for each word. Uses **bidirectional** kana/kanji lookup:
- Kanji anchor words → try their kana reading in kana-keyed sources
- Kana anchor words → try any kanji form that maps to that kana in CEJC

Anchors and word limits:

| Anchor          | Top-N words |
|-----------------|-------------|
| JPDB            | 25,000      |
| YOUTUBE_FREQ_V3 | 30,000      |
| ANIME_JDRAMA    | 25,000      |
| NETFLIX         | 25,000      |

**Outputs** (written to `../../`):
- `consolidated_anchor_[ANCHOR].csv` — raw ranks; columns: `word`, `[ANCHOR]_rank`, `CEJC_rank`, then all other sources
- `categorized_anchor_[ANCHOR].csv` — same structure with rank values replaced by tier numbers (1–5)

## How to interpret the outputs

- **`consolidated_anchor_*.csv`**: Use to compare raw frequency rankings across sources. A value of `-1` means the word was not found in that source.
- **`categorized_anchor_*.csv`**: Use for learning prioritization. A word with tier 5 in most columns is a high-confidence high-frequency target. Tier 1 means rare or absent — when most columns show tier 1, treat that word with lower priority.
- The **choice of anchor** determines which words appear (and in what order). Pick the anchor that best matches your learning context: JPDB for games/anime, YouTube for conversational, ANIME_JDRAMA for subtitle-based study, NETFLIX for modern media.
