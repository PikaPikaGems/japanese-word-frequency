"""
Generates the "N≤3 missing sources by rank band" summary table.

For each anchor (top-12k slice), and each rank band, reports the percentage
of words missing from at most 3 of the ~38 checked sources.

Run from repo root:
    python data/ALL/___experiments1/top12k/n_leq3_by_rank_band.py
"""

import csv
import glob
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from anchor_utils import get_anchor_family_cols

csv.field_size_limit(10_000_000)

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "anchors")

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

RANK_BANDS = [500, 1000, 3000, 5000, 12000]
THRESHOLD = 3


def pct(n, total):
    return 100 * n / total if total else 0.0


results = []  # list of (anchor_name, {band: pct})

for anchor_dir in sorted(glob.glob(os.path.join(DATA_DIR, "*_anchor"))):
    anchor_name = os.path.basename(anchor_dir).removesuffix("_anchor")
    consol_path = os.path.join(anchor_dir, "consolidated.csv")

    if not os.path.exists(consol_path):
        print(f"Skipping {anchor_name} — no consolidated.csv found")
        continue

    with open(consol_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        anchor_family = get_anchor_family_cols(anchor_name, header)
        source_cols = [c for c in header if c not in ("word", "hiragana", "katakana") and c not in anchor_family]
        check_cols = [c for c in source_cols if c not in EXCLUDE]
        rows = list(reader)

    band_pcts = {}
    for band in RANK_BANDS:
        band_rows = rows[:band]
        n = len(band_rows)
        if n == 0:
            band_pcts[band] = None
            continue
        count = sum(
            1 for r in band_rows
            if sum(1 for c in check_cols if r[c] == "-1") <= THRESHOLD
        )
        band_pcts[band] = pct(count, n)

    results.append((anchor_name, band_pcts))
    print(f"[{anchor_name}] {len(rows)} words | checked sources: {len(check_cols)}")

# ── Print markdown table ───────────────────────────────────────────────────────
col_w = 16
band_labels = {500: "Top-500", 1000: "Top-1k", 3000: "Top-3k", 5000: "Top-5k", 12000: "Top-12k"}

header_cells = ["Anchor"] + [band_labels[b] for b in RANK_BANDS]
sep_cells = ["-" * (col_w - 1)] + ["-------"] * len(RANK_BANDS)

def fmt_row(cells):
    return "| " + " | ".join(c.ljust(col_w - 1) if i == 0 else c.rjust(7) for i, c in enumerate(cells)) + " |"

print()
print(f"**N≤{THRESHOLD} missing sources by rank band** (top-12k slices):\n")
print(fmt_row(header_cells))
print(fmt_row(sep_cells))
for anchor_name, band_pcts in results:
    cells = [anchor_name] + [
        f"{band_pcts[b]:.1f}%" if band_pcts[b] is not None else "—"
        for b in RANK_BANDS
    ]
    print(fmt_row(cells))
