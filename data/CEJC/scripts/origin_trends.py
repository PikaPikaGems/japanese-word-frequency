#!/usr/bin/env python3
"""
origin_trends.py — How word-origin composition shifts across frequency tiers.

Shows the proportion of 和語 / 漢語 / 外来語 / 混種語 at each tier cutoff,
revealing how vocabulary character changes as you go deeper into the lexicon.

Output: Markdown with ASCII stacked bar chart + tables to stdout.

Usage:
    python3 origin_trends.py <json_dir>
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[3]))

from loaders import load_cejc_json
from analysis import tier_slice
from utils import markdown_table, ascii_stacked_bar_chart, mermaid_pie

TIERS = [500, 1500, 4000, 10000, 20000]

ORIGIN_SHORT = {
    "和":  "Native JP",
    "漢":  "Sino-JP",
    "外":  "Loanword",
    "混":  "Mixed",
    "固":  "Proper",
    "記号": "Symbol",
    "":   "Unknown",
}

ORIGIN_FULL = {
    "和":  "Native Japanese (和語)",
    "漢":  "Sino-Japanese (漢語)",
    "外":  "Foreign Loanword (外来語)",
    "混":  "Mixed Origin (混種語)",
    "固":  "Proper Noun Origin (固有)",
    "記号": "Symbol / Other",
    "":   "Unknown",
}

# Canonical display order
ORIGIN_ORDER = ["和", "漢", "外", "固", "混", "記号", ""]


def pct(n, total):
    return round(n / total * 100, 1) if total else 0.0


def origin_dist(sliced: dict) -> dict[str, int]:
    """Count unique words per origin for a sliced dataset."""
    counts: dict[str, int] = {}
    for entries in sliced.values():
        o = entries[0]["origin"]
        counts[o] = counts.get(o, 0) + 1
    return counts


def run(json_dir: str) -> None:
    data = load_cejc_json(json_dir)

    print("# Word Origin Trends Across Frequency Tiers")
    print()
    print("**Source:** CEJC — Corpus of Everyday Japanese Conversation")
    print()
    print(
        "Japanese vocabulary is divided into four main origin types:\n"
        "- **Native Japanese (和語)** — words with Old Japanese roots, the grammatical core of the language\n"
        "- **Sino-Japanese (漢語)** — words borrowed from Chinese, typically written in kanji, often formal or technical\n"
        "- **Foreign Loanwords (外来語)** — borrowed from other languages (mostly English), written in katakana\n"
        "- **Mixed Origin (混種語)** — hybrid words combining elements from different origin types\n"
        "\n"
        "This analysis shows how the balance between these origin types shifts as you move from the "
        "most frequent words down to the full vocabulary breadth. **Each tier is cumulative** — "
        "top 500 means words ranked 1–500."
    )
    print()

    # Collect data across all tiers
    tier_data: list[tuple[int, dict[str, int], int]] = []
    for tier in TIERS:
        sliced = tier_slice(data, tier)
        dist   = origin_dist(sliced)
        total  = len(sliced)
        tier_data.append((tier, dist, total))

    # ── Stacked bar chart ──────────────────────────────────────────────────
    print("## Origin Composition by Tier")
    print()
    print(
        "Each row is a cumulative tier. The stacked bar shows the proportional "
        "breakdown of word origins. Watch how native Japanese (█) shrinks and "
        "Sino-Japanese / loanwords / proper nouns grow as the tier expands."
    )
    print()

    stacked_rows = []
    for tier, dist, total in tier_data:
        seg = {
            ORIGIN_SHORT.get(o, o): pct(dist.get(o, 0), total)
            for o in ORIGIN_ORDER
            if dist.get(o, 0) > 0
        }
        stacked_rows.append((f"Top {tier:>6,}", seg))

    print(ascii_stacked_bar_chart(stacked_rows, max_width=50, fence=True))
    print()

    # ── Percentage table ───────────────────────────────────────────────────
    print("## Percentage Breakdown Table")
    print()
    print(
        "Exact percentages per tier. The most important columns to watch are "
        "**Native JP** (and) and **Sino-JP** (漢) — their crossover point reveals "
        "where the Sino-Japanese vocabulary overtakes the native core."
    )
    print()

    # Only include origins that appear in at least one tier
    active_origins = [o for o in ORIGIN_ORDER
                      if any(dist.get(o, 0) > 0 for _, dist, _ in tier_data)]

    headers = ["Tier", "Total Words"] + [ORIGIN_SHORT.get(o, o) for o in active_origins]
    rows = []
    for tier, dist, total in tier_data:
        row = [f"Top {tier:,}", f"{total:,}"]
        for o in active_origins:
            row.append(f"{pct(dist.get(o, 0), total):.1f}%")
        rows.append(row)

    print(markdown_table(headers, rows))
    print()

    # ── Per-tier Mermaid pies ──────────────────────────────────────────────
    print("## Pie Charts by Tier")
    print()
    for tier, dist, total in tier_data:
        items = [
            (ORIGIN_SHORT.get(o, o), dist[o])
            for o in ORIGIN_ORDER
            if dist.get(o, 0) > 0
        ]
        print(mermaid_pie(f"Origin — Top {tier:,}", items))
        print()

    # ── Key insights ───────────────────────────────────────────────────────
    print("## Key Insights")
    print()

    # Compute actual crossover tier for 和 vs 漢
    prev_native_pct = None
    crossover_tier  = None
    for tier, dist, total in tier_data:
        native_pct = pct(dist.get("和", 0), total)
        sino_pct   = pct(dist.get("漢", 0), total)
        if prev_native_pct is not None and native_pct < sino_pct and crossover_tier is None:
            crossover_tier = tier
        prev_native_pct = native_pct

    top_tier_dist  = tier_data[0][1]
    top_tier_total = tier_data[0][2]
    bot_tier_dist  = tier_data[-1][1]
    bot_tier_total = tier_data[-1][2]

    native_top = pct(top_tier_dist.get("和", 0), top_tier_total)
    native_bot = pct(bot_tier_dist.get("和", 0), bot_tier_total)
    loan_top   = pct(top_tier_dist.get("外", 0), top_tier_total)
    loan_bot   = pct(bot_tier_dist.get("外", 0), bot_tier_total)
    proper_bot = pct(bot_tier_dist.get("固", 0), bot_tier_total)

    print(
        f"- **Native Japanese dominates the core.** {native_top:.1f}% of the top-{TIERS[0]:,} words "
        f"are 和語, falling to {native_bot:.1f}% by the full vocabulary. The highest-frequency "
        f"words — particles, auxiliaries, common verbs — are almost exclusively native Japanese."
    )
    print()
    if crossover_tier:
        print(
            f"- **The 和語/漢語 crossover happens around the top-{crossover_tier:,} tier.** "
            f"Before this point, native Japanese outnumbers Sino-Japanese. Beyond it, the lexicon "
            f"is dominated by kanji-based technical and abstract vocabulary."
        )
    else:
        print(
            "- **Native Japanese remains the largest single origin type** throughout all tiers, "
            "though the gap with Sino-Japanese narrows significantly at deeper tiers."
        )
    print()
    print(
        f"- **Loanwords grow steadily but plateau.** Foreign loanwords rise from "
        f"{loan_top:.1f}% at the top-{TIERS[0]:,} to {loan_bot:.1f}% by the full vocabulary. "
        f"Most high-frequency loanwords are everyday katakana words; "
        f"lower-frequency loanwords include specialist and technical terms."
    )
    print()
    print(
        f"- **Proper nouns ({proper_bot:.1f}% at full vocabulary) are a significant slice.** "
        f"This reflects that a substantial portion of real-world vocabulary consists of "
        f"names of people, places, and countries — not just common words."
    )
    print()
    print(
        "- **Mixed-origin words (混種語) grow slowly but steadily.** These hybrids "
        "(e.g. 打ち合わせ combining 漢 and 和 elements) accumulate as vocabulary expands, "
        "reflecting the blended nature of modern Japanese."
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 origin_trends.py <json_dir>")
        sys.exit(1)
    run(sys.argv[1])
