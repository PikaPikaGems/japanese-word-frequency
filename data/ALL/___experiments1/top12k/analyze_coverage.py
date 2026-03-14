"""
Coverage analysis on top-12k slices of each anchor.
Reads from top12k/anchors/*_anchor/, outputs reports to top12k/.

Same EXCLUDE set as experiments1 (10 sources).
"""

import csv
import glob
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from anchor_utils import resolve_anchor_col

csv.field_size_limit(10_000_000)

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "anchors")
BAR_WIDTH = 40

EXCLUDE = {
    "AOZORA_BUNKO",
    "NIER",
    "ILYASEMENOV",
    "DD2_MIGAKU_NOVELS",
    "HERMITDAVE_2016",
    "HERMITDAVE_2018",
    "JPDB",
    "H_FREQ",
    "NAROU",
    "VN_FREQ",
}

RANK_BANDS = [500, 1000, 3000, 5000, 10000, 12000]


def bar(val: int, total: int) -> str:
    filled = round(BAR_WIDTH * val / total) if total else 0
    return "[" + "#" * filled + "-" * (BAR_WIDTH - filled) + "]"


for anchor_dir in sorted(glob.glob(os.path.join(DATA_DIR, "*_anchor"))):
    anchor_name = os.path.basename(anchor_dir).removesuffix("_anchor")
    consol_path = os.path.join(anchor_dir, "consolidated.csv")
    categ_path = os.path.join(anchor_dir, "categorized.csv")
    report_path = os.path.join(BASE, f"coverage_analysis_anchor_{anchor_name}.md")
    zero_path = os.path.join(BASE, f"zero_missing_anchor_{anchor_name}.csv")

    if not os.path.exists(consol_path):
        print(f"Skipping {anchor_name} — no consolidated.csv found")
        continue
    if not os.path.exists(categ_path):
        print(f"Skipping {anchor_name} — no categorized.csv found")
        continue

    with open(consol_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        anchor_col = resolve_anchor_col(anchor_name, header)
        source_cols = [c for c in header if c not in ("word", "hiragana", "katakana") and c != anchor_col]
        check_cols = [c for c in source_cols if c not in EXCLUDE]
        rows = list(reader)

    total = len(rows)

    zero_rows = [r for r in rows if all(r[c] != "-1" for c in check_cols)]
    with open(zero_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(zero_rows)

    with open(categ_path, newline="", encoding="utf-8") as f:
        cat_reader = csv.DictReader(f)
        cat_header = cat_reader.fieldnames
        cat_check = [c for c in cat_header if c not in ("word", "hiragana", "katakana") and c != anchor_col and c not in EXCLUDE]
        rare_rows = [r for r in cat_reader if any(r[c] == "1" for c in cat_check)]

    source_missing = {col: sum(1 for r in rows if r[col] == "-1") for col in source_cols}

    def count_missing(row):
        return sum(1 for c in check_cols if row[c] == "-1")

    missing_counts = [count_missing(r) for r in rows]
    max_m = max(missing_counts) if missing_counts else 0
    dist = [0] * (max_m + 1)
    for c in missing_counts:
        dist[c] += 1

    band_stats = []
    for band in RANK_BANDS:
        band_rows = rows[:band]
        if not band_rows:
            continue
        n = len(band_rows)
        z = sum(1 for r in band_rows if all(r[c] != "-1" for c in check_cols))
        band_stats.append((band, n, z))

    excl_note = ", ".join(sorted(EXCLUDE))
    lines = [
        f"# Coverage Analysis (Top 12k) — Anchor: {anchor_name}",
        f"\nTotal words: {total}  |  Source columns: {len(source_cols)}",
        f"Excluded from quality checks: {excl_note}  ({len(check_cols)} remaining)\n",
        "## Per-Source Missing Rate\n",
        f"{'Source':<35} {'Missing':>7}  {'%':>6}  Bar",
        "-" * 80,
    ]
    for col, miss in sorted(source_missing.items(), key=lambda x: -x[1]):
        pct = 100 * miss / total
        note = " [EXCLUDED]" if col in EXCLUDE else ""
        lines.append(f"{col:<35} {miss:>7}  {pct:>5.1f}%  {bar(miss, total)}{note}")

    lines += [
        f"\n## Zero-Missing by Rank Band",
        f"(Words with zero -1s across all {len(check_cols)} checked sources)\n",
        f"{'Top-N':>8}  {'Total':>7}  {'Zero-missing':>14}  {'%':>6}",
        "-" * 50,
    ]
    for band, n, z in band_stats:
        pct = 100 * z / n
        lines.append(f"{band:>8}  {n:>7}  {z:>14}  {pct:>5.1f}%")

    lines += [
        f"\n## Distribution: How Many Sources Each Word Is Missing From",
        f"({len(check_cols)} columns checked)\n",
        f"{'Missing':>8}  {'Words':>7}  {'%':>6}  Bar",
        "-" * 70,
    ]
    for i, count in enumerate(dist):
        pct = 100 * count / total
        lines.append(f"{i:>8}  {count:>7}  {pct:>5.1f}%  {bar(count, total)}")

    lines.append(f"\nWords with zero -1s: {dist[0]}  ({100*dist[0]/total:.1f}%)")
    lines.append(f"Words with at least one -1: {total - dist[0]}  ({100*(total-dist[0])/total:.1f}%)")
    lines.append(f"Words with at least one RARE category: {len(rare_rows)}  ({100*len(rare_rows)/total:.1f}%)")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[{anchor_name}] {total} words | zero-missing: {dist[0]} ({100*dist[0]/total:.1f}%) | -> {os.path.basename(report_path)}")

print("\nAll anchors analyzed.")
