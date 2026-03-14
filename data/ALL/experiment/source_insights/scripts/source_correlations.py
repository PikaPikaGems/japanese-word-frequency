#!/usr/bin/env python3
"""
source_correlations.py — Pairwise Spearman rank correlations between sources.

For all pairs of sources with ≥5,000 shared words:
  - Top 20 most correlated pairs (near-duplicates or same-domain sources)
  - Bottom 20 least correlated pairs (most divergent source types)
  - Within-group vs cross-group correlation summary by media type

Output: Markdown to stdout.

Usage:
    python3 source_correlations.py
"""

import sys
import csv
import math
from pathlib import Path
from itertools import combinations

sys.path.insert(0, str(Path(__file__).parent))
from utils import markdown_table, ascii_bar_chart

DATA_DIR = Path(__file__).parents[3]
CONSOLIDATED = DATA_DIR / "CEJC_anchor" / "consolidated.csv"

MIN_SHARED = 500  # minimum shared words to compute correlation

MEDIA_GROUPS = {
    "Written/Wikipedia": ["ADNO", "ILYASEMENOV", "WIKIPEDIA_V2", "CC100"],
    "Literature/Novels": [
        "AOZORA_BUNKO", "INNOCENT_RANKED", "NOVELS",
        "DD2_MORPHMAN_NOVELS", "DD2_YOMICHAN_NOVELS", "DD2_MIGAKU_NOVELS", "NAROU",
    ],
    "Anime/Drama": [
        "ANIME_JDRAMA", "DAVE_DOEBRICK", "CHRISKEMPSON",
        "DD2_MORPHMAN_SHONEN", "DD2_YOMICHAN_SHONEN", "DD2_YOMICHAN_SHONEN_STARS",
        "JITEN_ANIME",
    ],
    "Netflix": ["NETFLIX", "DD2_MIGAKU_NETFLIX", "DD2_MORPHMAN_NETFLIX"],
    "Slice of Life Anime": ["DD2_MORPHMAN_SOL", "DD2_YOMICHAN_SOL"],
    "Visual Novels": ["VN_FREQ", "DD2_YOMICHAN_VN"],
    "YouTube": ["YOUTUBE_FREQ", "YOUTUBE_FREQ_V3"],
    "Dictionary/Balanced": ["KOKUGOJITEN", "MONODICTS", "H_FREQ", "BCCWJ"],
    "Other": ["JPDB", "NIER", "HERMITDAVE_2016", "HERMITDAVE_2018"],
}


def spearman_r(xs, ys):
    """Compute Spearman correlation from paired lists of ranks."""
    n = len(xs)
    if n < 3:
        return float("nan")
    # Rank xs and ys
    def rank_list(vals):
        indexed = sorted(enumerate(vals), key=lambda iv: iv[1])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j < n - 1 and indexed[j + 1][1] == indexed[j][1]:
                j += 1
            avg_rank = (i + j) / 2 + 1
            for k in range(i, j + 1):
                ranks[indexed[k][0]] = avg_rank
            i = j + 1
        return ranks
    rx = rank_list(xs)
    ry = rank_list(ys)
    mean_rx = sum(rx) / n
    mean_ry = sum(ry) / n
    num = sum((rx[i] - mean_rx) * (ry[i] - mean_ry) for i in range(n))
    den = math.sqrt(
        sum((rx[i] - mean_rx) ** 2 for i in range(n)) *
        sum((ry[i] - mean_ry) ** 2 for i in range(n))
    )
    return num / den if den else float("nan")


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    return rows, fieldnames


def source_to_group(col):
    for group, members in MEDIA_GROUPS.items():
        if col in members:
            return group
    return "Other"


def main():
    rows, fieldnames = load(CONSOLIDATED)
    source_cols = fieldnames[15:]

    # Only sources with sufficient coverage
    good_sources = [
        col for col in source_cols
        if sum(1 for r in rows if r[col] not in ("-1", "")) >= 5000
    ]

    # Build value arrays per source (None for missing)
    data = {}
    for col in good_sources:
        data[col] = [
            int(r[col]) if r[col] not in ("-1", "") else None
            for r in rows
        ]

    # Pairwise correlations
    results = []
    for a, b in combinations(good_sources, 2):
        pairs = [
            (data[a][i], data[b][i])
            for i in range(len(rows))
            if data[a][i] is not None and data[b][i] is not None
        ]
        if len(pairs) < MIN_SHARED:
            continue
        xs, ys = zip(*pairs)
        r = spearman_r(list(xs), list(ys))
        results.append((r, a, b, len(pairs)))

    results.sort(key=lambda x: x[0], reverse=True)

    lines = []
    lines.append("# Source Correlation Analysis")
    lines.append("")
    lines.append(
        "Pairwise Spearman rank correlations between all sources with ≥5,000 words in common. "
        "A correlation near 1.0 means the two sources rank words nearly identically; "
        "near 0 means their rankings are essentially unrelated."
    )
    lines.append("")
    lines.append(f"**Sources analyzed:** {len(good_sources)} (≥5,000 words coverage)")
    lines.append(f"**Pairs computed:** {len(results):,}")
    lines.append("")

    lines.append("## Top 20 Most Correlated Pairs (most similar sources)")
    lines.append("")
    lines.append(
        "High correlation often indicates near-duplicate sources (same underlying data "
        "in different formats) or sources from the same domain."
    )
    lines.append("")
    top_rows = [
        (f"{r:.3f}", a, b, f"{n:,}")
        for r, a, b, n in results[:20]
    ]
    lines.append(markdown_table(["r", "Source A", "Source B", "Shared words"], top_rows))
    lines.append("")

    lines.append("## Bottom 20 Least Correlated Pairs (most divergent sources)")
    lines.append("")
    lines.append(
        "Low correlation indicates sources from very different domains — "
        "e.g. media transcriptions vs. dictionary headwords."
    )
    lines.append("")
    bot_rows = [
        (f"{r:.3f}", a, b, f"{n:,}")
        for r, a, b, n in results[-20:]
    ]
    lines.append(markdown_table(["r", "Source A", "Source B", "Shared words"], bot_rows))
    lines.append("")

    # Within-group vs cross-group averages
    lines.append("## Within-Group vs Cross-Group Correlation")
    lines.append("")
    lines.append(
        "Average Spearman r for pairs within the same media-type group vs. across groups. "
        "High within-group r confirms sources of the same type agree with each other."
    )
    lines.append("")

    group_of = {col: source_to_group(col) for col in good_sources}
    within_pairs = [(r, a, b) for r, a, b, _ in results if group_of.get(a) == group_of.get(b)]
    cross_pairs = [(r, a, b) for r, a, b, _ in results if group_of.get(a) != group_of.get(b)]

    def avg(lst):
        return sum(lst) / len(lst) if lst else float("nan")

    within_r = [r for r, _, _ in within_pairs]
    cross_r = [r for r, _, _ in cross_pairs]

    lines.append(f"- **Within-group average r:** {avg(within_r):.3f} ({len(within_r)} pairs)")
    lines.append(f"- **Cross-group average r:** {avg(cross_r):.3f} ({len(cross_r)} pairs)")
    lines.append("")

    # Per-group within average
    group_rows = []
    for group in MEDIA_GROUPS:
        group_members = [c for c in good_sources if group_of.get(c) == group]
        if len(group_members) < 2:
            continue
        gp_rs = [
            r for r, a, b, _ in results
            if group_of.get(a) == group and group_of.get(b) == group
        ]
        if gp_rs:
            group_rows.append((group, f"{avg(gp_rs):.3f}", str(len(group_members))))

    if group_rows:
        lines.append(markdown_table(["Group", "Avg within-group r", "Sources"], group_rows))
        lines.append("")

    # Notable observations
    lines.append("## Notable Observations")
    lines.append("")

    # Near-duplicates (r > 0.95)
    near_dupes = [(r, a, b, n) for r, a, b, n in results if r >= 0.95]
    if near_dupes:
        lines.append("### Near-duplicate sources (r ≥ 0.95)")
        lines.append("")
        lines.append(
            "These pairs are almost certainly the same underlying data published in different formats. "
            "Including both in a weighted average would double-count that source's signal."
        )
        lines.append("")
        for r, a, b, n in near_dupes:
            lines.append(f"- **{a} ↔ {b}**: r={r:.3f} ({n:,} shared words)")
        lines.append("")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
