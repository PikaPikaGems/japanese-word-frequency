"""
running-scripts.py — Reference guide for running the data generation and validation scripts.

This file is not executed directly. It documents which scripts to run, in what order,
and what each script does.

=== DATA GENERATION ===

After adding a new source to data/RAW/___FILTERED/<SOURCE_NAME>/, run the scripts below
to regenerate all consolidated.csv and categorized.csv files across all anchor variants.
Run these from the repository root.

    # 1. Generate CEJC-anchored consolidated output
    python data/ALL/___data_generation/SCRIPT.py

    # 2. Generate JPDB, YOUTUBE_FREQ_V3, ANIME_JDRAMA, NETFLIX anchors
    python data/ALL/___data_generation/make_anchored.py

    # 3. Generate BCCWJ_LUW, BCCWJ_SUW, CC100, RSPEER, WIKIPEDIA_V2 anchors
    python data/ALL/___data_generation/make_more_anchors.py

Each script scans data/RAW/___FILTERED/*/DATA.csv automatically (sorted alphabetically),
so new sources are picked up without any code changes.

=== VALIDATION ===

After regenerating, run the validation scripts to confirm the output is clean.

--- check_missing_reading.py ---
Checks that every word in every consolidated.csv has both hiragana and katakana readings.
Exits with code 0 if all readings are present; code 1 if any are missing.

    python data/ALL/___data_generation/check_missing_reading.py

--- check_duplicate_rank_columns.py ---
Checks that no two frequency rank columns in any consolidated.csv are exact duplicates
(identical values across all rows). This catches cases where the same source was
accidentally added twice, or where two sources are redundant.
Exits with code 0 if all columns are unique; code 1 if any duplicates are found.

    python data/ALL/___data_generation/check_duplicate_rank_columns.py

=== FULL PIPELINE (one-liner) ===

    python data/ALL/___data_generation/SCRIPT.py && \\
    python data/ALL/___data_generation/make_anchored.py && \\
    python data/ALL/___data_generation/make_more_anchors.py && \\
    python data/ALL/___data_generation/check_missing_reading.py && \\
    python data/ALL/___data_generation/check_duplicate_rank_columns.py
"""
