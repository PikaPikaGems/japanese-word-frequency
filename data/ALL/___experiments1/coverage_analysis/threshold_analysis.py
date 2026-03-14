"""
For each anchor, filters words at threshold <= N missing sources (default N=3).
Reports what % of those high-frequency words are absent in each source.
Writes filtered CSVs: threshold_N_anchor_{NAME}.csv
Writes consolidated report: threshold_analysis_N{N}.md

Updated EXCLUDE set (vs experiments0): adds H_FREQ, NAROU, VN_FREQ per §12 recommendation.
Runs on all *_anchor/ directories — picks up new anchors automatically.
"""

import csv
import glob
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from anchor_utils import resolve_anchor_col

csv.field_size_limit(10_000_000)

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "..", "..")
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

THRESHOLD = 3  # words missing from <= THRESHOLD sources are "high frequency"


def bar(val: int, total: int) -> str:
    filled = round(BAR_WIDTH * val / total) if total else 0
    return "[" + "#" * filled + "-" * (BAR_WIDTH - filled) + "]"


all_anchor_results = {}

for anchor_dir in sorted(glob.glob(os.path.join(DATA_DIR, "*_anchor"))):
    anchor_name = os.path.basename(anchor_dir).removesuffix("_anchor")
    consol_path = os.path.join(anchor_dir, "consolidated.csv")
    if not os.path.exists(consol_path):
        print(f"Skipping {anchor_name} — no consolidated.csv found")
        continue

    with open(consol_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        anchor_col = resolve_anchor_col(anchor_name, header)
        all_source_cols = [c for c in header if c not in ("word", "hiragana", "katakana") and c != anchor_col]
        check_cols = [c for c in all_source_cols if c not in EXCLUDE]
        rows = list(reader)

    total = len(rows)

    def missing_count(row):
        return sum(1 for c in check_cols if row[c] == "-1")

    hf_rows = [r for r in rows if missing_count(r) <= THRESHOLD]
    n_hf = len(hf_rows)

    source_absent = {}
    for col in all_source_cols:
        absent = sum(1 for r in hf_rows if r[col] == "-1")
        source_absent[col] = absent

    all_anchor_results[anchor_name] = {
        "total": total,
        "hf_rows": hf_rows,
        "n_hf": n_hf,
        "check_cols": check_cols,
        "all_source_cols": all_source_cols,
        "source_absent": source_absent,
        "header": header,
    }

    out_path = os.path.join(BASE, f"threshold_{THRESHOLD}_anchor_{anchor_name}.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(hf_rows)

    print(
        f"[{anchor_name}] total={total}  high-freq (≤{THRESHOLD} missing)={n_hf} ({100*n_hf/total:.1f}%)"
        f"  -> {os.path.basename(out_path)}"
    )


# ── Write consolidated report ─────────────────────────────────────────────────
report_path = os.path.join(BASE, f"threshold_analysis_N{THRESHOLD}.md")
excl_note = ", ".join(sorted(EXCLUDE))

lines = [
    f"# Threshold Analysis — High-Frequency Words (Missing from ≤{THRESHOLD} Sources)",
    f"\n**Definition:** A word is \"high frequency\" if it is absent from at most {THRESHOLD} of the checked sources.",
    f"**Excluded from checks:** {excl_note}",
    f"\nFor each anchor, this shows:",
    f"- How many words pass the threshold",
    f"- For every source, what % of those high-frequency words are absent in that source",
    f"\n---",
]

for anchor_name, data in all_anchor_results.items():
    total = data["total"]
    n_hf = data["n_hf"]
    check_cols = data["check_cols"]
    all_source_cols = data["all_source_cols"]
    source_absent = data["source_absent"]

    lines += [
        f"\n## Anchor: {anchor_name}",
        f"\nTotal words: {total}  |  Checked sources: {len(check_cols)}  |  High-frequency (≤{THRESHOLD} missing): {n_hf} ({100*n_hf/total:.1f}%)\n",
        f"{'Source':<35} {'Absent':>7}  {'%':>6}  Bar  Note",
        "-" * 90,
    ]

    for col in sorted(all_source_cols, key=lambda c: -source_absent[c]):
        absent = source_absent[col]
        pct = 100 * absent / n_hf if n_hf else 0
        excl_tag = " [EXCLUDED]" if col in EXCLUDE else ""
        lines.append(
            f"{col:<35} {absent:>7}  {pct:>5.1f}%  {bar(absent, n_hf)}{excl_tag}"
        )

with open(report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\nReport -> {os.path.basename(report_path)}")
