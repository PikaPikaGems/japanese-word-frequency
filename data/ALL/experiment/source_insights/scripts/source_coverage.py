#!/usr/bin/env python3
"""
source_coverage.py — Per-source word coverage analysis.

For each of the 35 external sources:
  - Number and % of the 27,988 words that have a valid rank
  - Bar chart sorted by coverage

Also reports how many sources cover each word (coverage histogram).

Output: Markdown to stdout.

Usage:
    python3 source_coverage.py
"""

import sys
import csv
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import markdown_table, ascii_bar_chart

DATA_DIR = Path(__file__).parents[3]
CONSOLIDATED = DATA_DIR / "consolidated_anchor_CEJC.csv"

MISSING = -1


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    return rows, fieldnames


def main():
    rows, fieldnames = load(CONSOLIDATED)
    source_cols = fieldnames[15:]  # columns after the 14 CEJC rank columns
    total = len(rows)

    # Per-source coverage
    coverage = {}
    for col in source_cols:
        valid = sum(1 for r in rows if r[col] != str(MISSING) and r[col] != "")
        coverage[col] = valid

    sorted_by_cov = sorted(coverage.items(), key=lambda x: x[1], reverse=True)

    lines = []
    lines.append("# Source Coverage Analysis")
    lines.append("")
    lines.append(f"**Total words in consolidated.csv:** {total:,}")
    lines.append(f"**Total external sources:** {len(source_cols)}")
    lines.append("")
    lines.append(
        "Each source covers only a subset of the 27,988 words — the rest receive rank -1 "
        "(not present in that source's top-25k list). This affects how much weight each "
        "source contributes to cross-source comparisons."
    )
    lines.append("")

    # Summary table
    lines.append("## Coverage per Source")
    lines.append("")
    table_rows = [
        (col, f"{cnt:,}", f"{cnt / total * 100:.1f}%")
        for col, cnt in sorted_by_cov
    ]
    lines.append(markdown_table(["Source", "Words covered", "% of total"], table_rows))
    lines.append("")

    # Bar chart
    lines.append("## Coverage Bar Chart (sorted by coverage)")
    lines.append("")
    bar_items = [(col, cnt / total * 100) for col, cnt in sorted_by_cov]
    lines.append(ascii_bar_chart(bar_items, fence=True, max_bar=40))
    lines.append("")

    # Coverage histogram: how many sources cover each word
    lines.append("## Word Coverage Distribution")
    lines.append("")
    lines.append(
        "How many of the 35 sources assign a valid rank to each word. "
        "Words covered by more sources have more cross-source signal."
    )
    lines.append("")

    source_count_per_word = []
    for row in rows:
        n = sum(1 for col in source_cols if row[col] != str(MISSING) and row[col] != "")
        source_count_per_word.append(n)

    thresholds = [35, 30, 25, 20, 15, 10, 5, 2, 1, 0]
    hist_rows = []
    for t in thresholds:
        if t == 0:
            cnt = sum(1 for n in source_count_per_word if n == 0)
            label = "0 sources (CEJC-only)"
        elif t == 1:
            cnt = sum(1 for n in source_count_per_word if n == 1)
            label = "exactly 1 source"
        else:
            cnt = sum(1 for n in source_count_per_word if n >= t)
            label = f"{t}+ sources"
        hist_rows.append((label, f"{cnt:,}", f"{cnt / total * 100:.1f}%"))

    lines.append(markdown_table(["Coverage", "Words", "% of total"], hist_rows))
    lines.append("")

    # Notable observations
    lines.append("## Notable Observations")
    lines.append("")

    # Flag anomalously low coverage
    low_coverage = [(col, cnt) for col, cnt in coverage.items() if cnt < 1000]
    if low_coverage:
        lines.append("### Sources with anomalously low coverage (<1,000 words)")
        lines.append("")
        for col, cnt in sorted(low_coverage, key=lambda x: x[1]):
            lines.append(f"- **{col}**: {cnt:,} words ({cnt / total * 100:.1f}%) — likely incomplete or misprocessed source")
        lines.append("")

    cejc_only = sum(1 for n in source_count_per_word if n == 0)
    lines.append(f"### CEJC-exclusive words")
    lines.append("")
    lines.append(
        f"**{cejc_only:,} words** ({cejc_only / total * 100:.1f}%) appear in CEJC but in none of the 35 external sources. "
        "These are likely proper nouns, very rare terms, or spoken-only vocabulary not captured by any written/media corpus."
    )
    lines.append("")

    high_cov = [(col, cnt) for col, cnt in coverage.items() if cnt / total >= 0.50]
    if high_cov:
        lines.append("### Sources with broadest coverage (≥50% of words)")
        lines.append("")
        for col, cnt in sorted(high_cov, key=lambda x: x[1], reverse=True):
            lines.append(f"- **{col}**: {cnt:,} words ({cnt / total * 100:.1f}%)")
        lines.append("")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
