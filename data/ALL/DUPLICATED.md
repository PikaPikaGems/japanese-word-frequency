# Duplicate Column Check Scripts

Two scripts exist for checking duplicate frequency rank columns in `consolidated.csv` files.

---

## `data/ALL/___experiments0/duplicate_detection/check_duplicates.py`

- Operates on a **single hardcoded** `consolidated.csv` in its own directory.
- Skips `word` and any column ending in `_rank` — meaning all CEJC sub-columns are excluded from the check.
- Does **not** skip `hiragana` or `katakana` (they would be checked as if they were rank columns).
- **Destructive**: when duplicates are found, prompts the user to delete the duplicate columns from `consolidated.csv` and remove their corresponding `___FILTERED` directories.
- Includes logic to prefer keeping non-`DD2_` columns when deciding which duplicate to drop.

## `check_duplicate_rank_columns.py` (project root)

- Recursively finds and checks **all** `consolidated.csv` files under the project root.
- Skips only `word`, `hiragana`, and `katakana` — all rank columns including CEJC sub-columns are checked.
- **Read-only**: reports duplicates but makes no changes.
- Exits with code 1 if any duplicates are detected, suitable for use in CI or pre-build checks.

---

## Summary of differences

| | `check_duplicates.py` | `check_duplicate_rank_columns.py` |
| ------------------------- | ------------------------------------- | --------------------------------- |
| Files checked             | One hardcoded file                    | All `consolidated.csv` recursively |
| Columns skipped           | `word` + anything ending in `_rank`   | `word`, `hiragana`, `katakana`    |
| CEJC columns checked?     | No (excluded by `_rank` suffix)       | Yes                               |
| `hiragana`/`katakana` checked? | Yes (not excluded)               | No                                |
| Destructive?              | Yes — can delete columns and dirs     | No — report only                  |
| Exit code on duplicates   | No                                    | Yes (exit 1)                      |
