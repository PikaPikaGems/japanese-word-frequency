# duplicate_detection

Audit and removal of redundant (duplicate) source columns in the consolidated data.

## Motivation

Some word frequency lists in `data/RAW/___FILTERED/` are derived from the same underlying data or preprocessing pipeline, producing rank vectors that are byte-for-byte identical across all words. Including duplicates inflates source counts and distorts coverage and variance statistics. This experiment detects and eliminates them.

## Script

### `check_duplicates.py`

**Methodology:**

1. Loads `consolidated.csv` (CEJC-anchored).
2. Identifies all source-rank columns (excluding `word` and CEJC domain/gender columns).
3. For each source column, computes a tuple of all rank values as a signature.
4. Groups columns by identical signature — any group with 2+ columns is a duplicate set.
5. Within each duplicate group, prefers to keep a non-DD2 source (original datasets over derived variants); falls back to alphabetical order.
6. Prompts for confirmation before writing changes.
7. On confirmation: removes duplicate columns from `consolidated.csv` and deletes their `___FILTERED` directories.

**Usage:**
```
python3 check_duplicates.py
```

The script is interactive — it prints which columns would be removed and asks `[y/N]` before making any changes.

## Output

### `DUPLICATES.md`

Audit log of all duplicate detection runs. Records:
- Which duplicate groups were found
- Which column was kept and which were removed (and why)
- Current status (no further duplicates as of last run)

## Results

Three duplicate groups were identified and removed:

| Removed source           | Kept source       | Reason                         |
|--------------------------|-------------------|-------------------------------|
| `DD2_YOMICHAN_NETFLIX`   | `NETFLIX`         | NETFLIX is the original source |
| `DD2_MIGAKU_SOL`         | `DD2_YOMICHAN_SOL`| Alphabetical among DD2 group   |
| `DD2_MIGAKU_SHONEN`      | `DD2_YOMICHAN_SHONEN` | Alphabetical among DD2 group |

After removal, 35 unique sources remain. No further duplicates have been found.
