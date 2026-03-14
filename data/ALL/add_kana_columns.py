"""
Add 'hiragana' and 'katakana' columns (after 'word') to every
categorized.csv and consolidated.csv under data/ALL/*/

Reading sources (in priority order):
  1. data/JPDBV2/jpdb_v2.2_freq_list_2024-10-13.csv  — tab-separated,
     columns: term, reading, frequency, kana_frequency
     'reading' is already hiragana.
  2. data/CEJC/2_cejc_frequencylist_suw_token.tsv    — tab-separated,
     columns: rank, 語彙素読み, 語彙素, ...
     '語彙素読み' is katakana; '語彙素' is the vocabulary lemma (word).

Usage:
    python data/ALL/add_kana_columns.py
"""

import csv
import sys
from pathlib import Path

# ── load kana.py directly to avoid triggering utils/__init__.py ───────────────
ROOT = Path(__file__).parents[2]

import importlib.util as _ilu
_spec = _ilu.spec_from_file_location("kana", ROOT / "utils" / "kana.py")
_mod  = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
hiragana_to_katakana = _mod.hiragana_to_katakana
katakana_to_hiragana = _mod.katakana_to_hiragana

# ── source file paths ─────────────────────────────────────────────────────────
JPDB_SRC = ROOT / "data" / "JPDBV2" / "jpdb_v2.2_freq_list_2024-10-13.csv"
CEJC_SRC = ROOT / "data" / "CEJC" / "2_cejc_frequencylist_suw_token.tsv"
ALL_DIR  = ROOT / "data" / "ALL"


# ── build reading lookup: word -> (hiragana, katakana) ────────────────────────

def _build_lookup() -> dict[str, tuple[str, str]]:
    lookup: dict[str, tuple[str, str]] = {}

    # 1. JPDB — reading column is hiragana
    with open(JPDB_SRC, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            word = row.get("term", "").strip()
            reading = row.get("reading", "").strip()
            if word and reading:
                hira = reading
                kata = hiragana_to_katakana(reading)
                lookup[word] = (hira, kata)

    # 2. CEJC — 語彙素読み column is katakana; 語彙素 is the word
    with open(CEJC_SRC, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            word = row.get("語彙素", "").strip()
            reading = row.get("語彙素読み", "").strip()
            if word and reading and word not in lookup:
                kata = reading
                hira = katakana_to_hiragana(reading)
                lookup[word] = (hira, kata)

    return lookup


# ── patch a single CSV file ───────────────────────────────────────────────────

def _patch_csv(path: Path, lookup: dict[str, tuple[str, str]]) -> None:
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        return

    header = rows[0]
    if "hiragana" in header and "katakana" in header:
        return  # already patched

    try:
        word_idx = header.index("word")
    except ValueError:
        print(f"  [skip] no 'word' column: {path}")
        return

    insert_at = word_idx + 1
    new_header = header[:insert_at] + ["hiragana", "katakana"] + header[insert_at:]

    new_rows = [new_header]
    for row in rows[1:]:
        word = row[word_idx] if word_idx < len(row) else ""
        hira, kata = lookup.get(word, ("", ""))
        new_row = row[:insert_at] + [hira, kata] + row[insert_at:]
        new_rows.append(new_row)

    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(new_rows)

    print(f"  patched: {path.relative_to(ROOT)}")


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    print("Building reading lookup...")
    lookup = _build_lookup()
    print(f"  {len(lookup):,} entries loaded")

    targets = sorted(ALL_DIR.glob("*/categorized.csv")) + sorted(ALL_DIR.glob("*/consolidated.csv"))
    print(f"Patching {len(targets)} files...")
    for path in targets:
        _patch_csv(path, lookup)

    print("Done.")


if __name__ == "__main__":
    main()
