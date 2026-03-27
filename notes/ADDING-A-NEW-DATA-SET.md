# Adding a New Dataset

This document describes the steps to add a new frequency source to the consolidated rankings.

---

## Overview

Raw source files live in `data/RAW/<AUTHOR_OR_GROUP>/`. Each source must be converted into a standardized `DATA.csv` (columns: `WORD`, `FREQUENCY_RANKING`, top 25,000 entries) under `data/RAW/___FILTERED/<SOURCE_NAME>/`. The consolidation scripts automatically pick up every `___FILTERED/*/DATA.csv` when they are run.

---

## Step 1 — Place the raw data

Put the raw source files in `data/RAW/<AUTHOR_OR_GROUP>/<dataset_name>/`. Do not modify the originals.

Example:

```
data/RAW/KUUUUBE/jmdict_freq/
    index.json
    term_meta_bank_1.json
```

---

## Step 2 — Create the filtered source folder

Create a new subdirectory under `data/RAW/___FILTERED/` named after the source (use `ALLCAPS_UNDERSCORES`):

```
data/RAW/___FILTERED/<SOURCE_NAME>/
    README.md
    SCRIPT.py
```

Choose a name that is:

- Descriptive and unique
- Alphabetically placed correctly (the consolidation scripts sort sources alphabetically — the name determines column order in all consolidated CSVs)

---

## Step 3 — Write README.md

Describe the source. Template:

```markdown
# <SOURCE_NAME> — <Short title>

## Source

- **GitHub / URL:** <link>

## Description

<What corpus or resource this is, who created it, data type, coverage.>

**Author:** <author>
**Data type:** <books / subtitles / newspaper / web text / etc.>
**Coverage:** <time period, size, etc.>

## Format (<format name>)

<Describe the raw file format — TSV, JSON, etc. — and what fields it contains.>

## DATA.csv

Top 25,000 words by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
```

---

## Step 4 — Write SCRIPT.py

Rules:

- **No pandas** — use the stdlib `csv` and `json` modules only
- Input path: relative to `__file__`, pointing into `../../<AUTHOR>/...`
- Output path: `os.path.join(os.path.dirname(__file__), "DATA.csv")`
- Top 25,000 entries maximum
- Deduplicate on word surface form — keep the lowest (most frequent) rank
- Output columns: `WORD`, `FREQUENCY_RANKING` (reassigned sequentially starting from 1)

Minimal template:

```python
import csv
import json
import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), "../../AUTHOR/dataset/file.json")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "DATA.csv")
TOP_N = 25000


def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        entries = json.load(f)

    best_rank: dict[str, int] = {}
    for entry in entries:
        word = entry[0]
        rank = entry[2].get("value")  # adjust to match actual format
        if rank is not None and (word not in best_rank or rank < best_rank[word]):
            best_rank[word] = rank

    rows = sorted(best_rank.items(), key=lambda x: x[1])[:TOP_N]

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["WORD", "FREQUENCY_RANKING"])
        for new_rank, (word, _) in enumerate(rows, start=1):
            writer.writerow([word, new_rank])

    print(f"Written {len(rows)} rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
```

See existing `SCRIPT.py` files in other `___FILTERED/` subfolders for more examples (e.g., `BCCWJ_SUW/SCRIPT.py` for multi-file Yomitan JSON, `ADNO/SCRIPT.py` for TSV input).

---

## Step 5 — Run SCRIPT.py to generate DATA.csv

```bash
python data/RAW/___FILTERED/<SOURCE_NAME>/SCRIPT.py
```

Verify the output:

- File exists: `data/RAW/___FILTERED/<SOURCE_NAME>/DATA.csv`
- First row is the header `WORD,FREQUENCY_RANKING`
- Row count ≤ 25,000
- Ranks are sequential integers starting from 1

---

## Step 6 — Check for duplicate columns

Run the duplicate-column check **before** running the full consolidation. This does a quick consolidation pass to verify the new source is not identical to an existing one:

```bash
# First, run only the CEJC consolidation so the new column exists
python data/ALL/___data_generation/SCRIPT.py

# Then check for duplicates
python data/ALL/___experiments1/check_duplicate_rank_columns.py
```

The script exits with code 1 and prints any duplicate pairs if found. **If duplicates are detected, stop here** — the new source is redundant. Either remove it or document why it is kept before proceeding.

---

## Step 7 — Run the remaining consolidation scripts

Once the duplicate check passes, run the remaining scripts to regenerate all anchor variants. They automatically include every `___FILTERED/*/DATA.csv` (sorted alphabetically), so the new source will be picked up without any code changes.

```bash
# JPDB, YOUTUBE_FREQ_V3, ANIME_JDRAMA, NETFLIX anchors
python data/ALL/___data_generation/make_anchored.py

# BCCWJ_LUW, BCCWJ_SUW, CC100, RSPEER, WIKIPEDIA_V2 anchors
python data/ALL/___data_generation/make_more_anchors.py
```

After running, verify the new column appears in a consolidated CSV:

```bash
head -1 data/ALL/CEJC_anchor/consolidated.csv | tr ',' '\n' | grep -n <SOURCE_NAME>
```

---

## Step 8 — Update CONSOLIDATED_CSV_REFERENCEV1.md

Edit [CONSOLIDATED_CSV_REFERENCEV1.md](CONSOLIDATED_CSV_REFERENCEV1.md):

1. **`## SAMPLE DATA`** — add the new column name to the header row (in alphabetical position), and insert the corresponding rank value into each of the three sample data rows.

2. **`## Column Reference`** — add a row to the appropriate table describing what the column means and summarizing the source. Choose the section that best fits the source type:
   - Written corpus columns (books, web, Wikipedia, newspaper)
   - Spoken Japanese columns (CSJ)
   - Fiction and literary columns (novels, VNs, web novels)
   - Subtitle and media columns (anime, drama, Netflix, YouTube)
   - Specialized columns (niche or single-domain sources)

---

## Step 9 — Update notes/dataset-directory-tree.md

Add a row to the table in the `RAW/___FILTERED — 60+ Source Datasets + RSPEER` section of [notes/dataset-directory-tree.md](notes/dataset-directory-tree.md). Insert alphabetically by source name:

```markdown
| <SOURCE_NAME> | <Short description> |
```

## Step 10 — Update notes/dataset-catalog.md

Add a row to [notes/dataset-catalog.md](dataset-catalog.md) describing the new source. Insert it into the section that best fits the source type (Academic / Research Corpora, Written Corpora, Subtitle / Media, etc.). If the source is particularly high-quality or widely useful, also add it to the **⭐ Highlighted (Shortlisted)** table at the top.

Row format:

```markdown
| `SOURCE_NAME` | <Author / Project> | <One-sentence description: corpus type, size, date, notable properties.> |
```

Insert alphabetically within the section, or in rough quality/relevance order for the Highlighted table.
