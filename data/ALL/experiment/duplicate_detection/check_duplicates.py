"""
Checks consolidated.csv for duplicate source columns — columns with exactly the same
FREQUENCY_RANKING value for every row (treating -1 as missing). Reports duplicates
and removes them from both consolidated.csv and the corresponding ___FILTERED directories.
"""

import csv
import glob
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
CONSOLIDATED = os.path.join(BASE, "consolidated.csv")
FILTERED_DIR = os.path.join(ROOT, "data", "RAW", "___FILTERED")

# Columns that are NOT source rank columns (skip these in duplicate check)
CEJC_PREFIX = {"word", "combined_rank", "small_talk_rank", "medical_consultation_rank",
                "workplace_rank", "school_rank", "family_rank", "outing_rank",
                "male_rank", "female_rank"}


def load_consolidated():
    rows = []
    with open(CONSOLIDATED, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames[:]
        for row in reader:
            rows.append(row)
    return fieldnames, rows


def get_source_columns(fieldnames):
    """Return column names that are source rank columns (not word or CEJC)."""
    source_cols = []
    for col in fieldnames:
        if col == "word":
            continue
        # CEJC columns end with _rank or are named combined_rank
        if col.endswith("_rank"):
            continue
        source_cols.append(col)
    return source_cols


def col_values(rows, col):
    return tuple(row[col] for row in rows)


def find_duplicates(fieldnames, rows):
    source_cols = get_source_columns(fieldnames)
    print(f"Checking {len(source_cols)} source columns for duplicates...\n")

    # Map column signature -> list of column names with that signature
    sig_to_cols = {}
    for col in source_cols:
        sig = col_values(rows, col)
        sig_to_cols.setdefault(sig, []).append(col)

    duplicates = {sig: cols for sig, cols in sig_to_cols.items() if len(cols) > 1}
    return duplicates, source_cols


def remove_duplicates(fieldnames, rows, to_remove):
    """Remove columns from fieldnames/rows and delete their ___FILTERED directories."""
    new_fieldnames = [f for f in fieldnames if f not in to_remove]
    new_rows = []
    for row in rows:
        new_row = {k: v for k, v in row.items() if k not in to_remove}
        new_rows.append(new_row)

    # Write updated consolidated.csv
    with open(CONSOLIDATED, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=new_fieldnames)
        writer.writeheader()
        writer.writerows(new_rows)
    print(f"\nUpdated {CONSOLIDATED}")
    print(f"Removed columns: {sorted(to_remove)}")

    # Delete corresponding ___FILTERED directories
    for name in to_remove:
        dir_path = os.path.join(FILTERED_DIR, name)
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)
            print(f"Deleted directory: {dir_path}")
        else:
            print(f"WARNING: Directory not found: {dir_path}")


def main():
    fieldnames, rows = load_consolidated()
    duplicates, source_cols = find_duplicates(fieldnames, rows)

    if not duplicates:
        print("No duplicate columns found.")
        return

    print(f"Found {len(duplicates)} duplicate group(s):\n")
    to_remove = set()

    for i, (sig, cols) in enumerate(duplicates.items(), 1):
        print(f"  Group {i}: {cols}")
        # Prefer non-DD2 columns (existing datasets); then alphabetical
        non_dd2 = [c for c in cols if not c.startswith("DD2_")]
        if non_dd2:
            kept = sorted(non_dd2)[0]
        else:
            kept = sorted(cols)[0]
        removed = [c for c in sorted(cols) if c != kept]
        print(f"    -> Keep: {kept}")
        print(f"    -> Remove: {removed}")
        to_remove.update(removed)

    print(f"\nTotal columns to remove: {len(to_remove)}")

    confirm = input("\nProceed with removal? [y/N] ").strip().lower()
    if confirm == "y":
        remove_duplicates(fieldnames, rows, to_remove)
        print("\nDone.")
    else:
        print("Aborted. No changes made.")


if __name__ == "__main__":
    main()
