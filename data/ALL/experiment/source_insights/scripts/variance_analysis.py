#!/usr/bin/env python3
"""
variance_analysis.py — Cross-source rank variance analysis.

Identifies:
  - Words with the lowest normalized-rank variance (universally consistent)
  - Words with the highest tier variance (most contested across sources)
  - Universal core words: ranked 'basic' by the most sources

Output: Markdown to stdout.

Usage:
    python3 variance_analysis.py
"""

import sys
import csv
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import markdown_table

DATA_DIR = Path(__file__).parents[3]
CONSOLIDATED = DATA_DIR / "CEJC_anchor" / "consolidated.csv"
CATEGORIZED = DATA_DIR / "CEJC_anchor" / "categorized.csv"

# categorized.csv encoding: 5=basic, 4=common, 3=fluent, 2=advanced, 1=rare/absent
BASIC = 5
ABSENT = 1  # also used for "not in source" — indistinguishable

MIN_SOURCES_FOR_VARIANCE = 10
TOP_N = 30


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    return rows, fieldnames


def safe_int(v, missing=-1):
    try:
        i = int(v)
        return None if i == missing else i
    except (ValueError, TypeError):
        return None


def mean(vals):
    v = [x for x in vals if x is not None]
    return sum(v) / len(v) if v else None


def std(vals):
    v = [x for x in vals if x is not None]
    if len(v) < 2:
        return None
    m = sum(v) / len(v)
    return math.sqrt(sum((x - m) ** 2 for x in v) / len(v))


def main():
    rows, fieldnames = load_csv(CONSOLIDATED)
    cat_rows, _ = load_csv(CATEGORIZED)
    source_cols = fieldnames[15:]
    total = len(rows)

    # Per-source min/max for normalization
    col_vals = {}
    for col in source_cols:
        vals = [safe_int(r[col]) for r in rows]
        valid = [v for v in vals if v is not None]
        col_vals[col] = (min(valid), max(valid)) if valid else (None, None)

    def normalize(raw, col):
        lo, hi = col_vals[col]
        if lo is None or hi == lo:
            return None
        return (raw - lo) / (hi - lo)

    # Per-word: normalized rank values across sources, tier values
    word_data = []
    for i, row in enumerate(rows):
        word = row["word"]
        overall_rank = safe_int(row["combined_rank"], missing=-9999)

        norm_vals = []
        for col in source_cols:
            v = safe_int(row[col])
            if v is not None:
                n = normalize(v, col)
                if n is not None:
                    norm_vals.append(n)

        # Tier values from categorized: exclude ABSENT (1) as indistinguishable from missing
        tier_vals = []
        for col in source_cols:
            t = safe_int(cat_rows[i][col], missing=-1)
            if t is not None and t != ABSENT:
                tier_vals.append(t)

        word_data.append({
            "word": word,
            "overall_rank": overall_rank,
            "norm_vals": norm_vals,
            "n_sources": len(norm_vals),
            "norm_std": std(norm_vals),
            "tier_vals": tier_vals,
            "n_present": len(tier_vals),
            "tier_std": std(tier_vals),
            "tier_min": min(tier_vals) if tier_vals else None,
            "tier_max": max(tier_vals) if tier_vals else None,
            "basic_count": sum(1 for t in tier_vals if t == BASIC),
        })

    lines = []
    lines.append("# Cross-Source Rank Variance Analysis")
    lines.append("")
    lines.append(
        "How consistently do the 35 sources agree on a word's frequency? "
        "Low variance = all sources agree; high variance = sources strongly disagree."
    )
    lines.append("")

    # --- Universal core words ---
    lines.append("## Universal Core Words (basic tier in most sources)")
    lines.append("")
    lines.append(
        f"Words ranked in the top ~1,000 (tier 5 = basic) by the largest number of sources, "
        f"excluding tier 1 (rare/absent) as indistinguishable from 'not in source'. "
        f"These words have the strongest cross-corpus consensus for being high-priority vocabulary."
    )
    lines.append("")

    thresholds = [25, 20, 15, 10]
    for t in thresholds:
        cnt = sum(1 for d in word_data if d["basic_count"] >= t)
        lines.append(f"- Basic in **{t}+** sources: **{cnt}** words")
    lines.append("")

    core = sorted(
        [d for d in word_data if d["basic_count"] >= 20],
        key=lambda d: -d["basic_count"]
    )[:TOP_N]
    core_rows = [
        (d["word"], str(d["overall_rank"]), str(d["basic_count"]), str(d["n_present"]))
        for d in core
    ]
    lines.append(markdown_table(
        ["Word", "Overall rank", "Basic in N sources", "Present in N sources"],
        core_rows
    ))
    lines.append("")

    # --- Lowest normalized-rank variance ---
    lines.append("## Lowest Rank Variance (universally consistent words)")
    lines.append("")
    lines.append(
        f"Words present in {MIN_SOURCES_FOR_VARIANCE}+ sources where normalized ranks agree most closely. "
        "These words have nearly the same position across every corpus type — "
        "a reliable signal regardless of which source you use."
    )
    lines.append("")

    low_var = sorted(
        [d for d in word_data if d["n_sources"] >= MIN_SOURCES_FOR_VARIANCE and d["norm_std"] is not None],
        key=lambda d: d["norm_std"]
    )[:TOP_N]
    low_rows = [
        (d["word"], str(d["overall_rank"]), f"{d['norm_std']:.4f}", str(d["n_sources"]))
        for d in low_var
    ]
    lines.append(markdown_table(
        ["Word", "Overall rank", "Normalized std", "N sources"],
        low_rows
    ))
    lines.append("")

    # --- Highest tier variance ---
    lines.append("## Highest Tier Variance (most contested words)")
    lines.append("")
    lines.append(
        f"Words present in {MIN_SOURCES_FOR_VARIANCE}+ sources where tier assignments disagree most. "
        "A word ranked 'basic' in some corpora but 'advanced' in others suggests "
        "strong domain-specificity: highly frequent in one medium but rare in another."
    )
    lines.append("")

    high_var = sorted(
        [d for d in word_data if d["n_present"] >= MIN_SOURCES_FOR_VARIANCE and d["tier_std"] is not None],
        key=lambda d: -d["tier_std"]
    )[:TOP_N]

    TIER_NAMES = {5: "basic", 4: "common", 3: "fluent", 2: "advanced"}

    high_rows = [
        (
            d["word"],
            str(d["overall_rank"]),
            f"{d['tier_std']:.2f}",
            TIER_NAMES.get(d["tier_max"], str(d["tier_max"])) if d["tier_max"] else "—",
            TIER_NAMES.get(d["tier_min"], str(d["tier_min"])) if d["tier_min"] else "—",
            str(d["n_present"]),
        )
        for d in high_var
    ]
    lines.append(markdown_table(
        ["Word", "Overall rank", "Tier std", "Best tier", "Worst tier", "N sources"],
        high_rows
    ))
    lines.append("")

    # --- Notable patterns ---
    lines.append("## Notable Patterns")
    lines.append("")

    lines.append("### Consistently ranked words are abstract 漢語 (Sino-Japanese)")
    lines.append("")
    lines.append(
        "The words with lowest variance tend to be general-purpose Sino-Japanese vocabulary: "
        "判断 (judgment), 原因 (cause), 理解 (understanding), 可能 (possible), 重要 (important), 影響 (influence). "
        "These terms appear at similar frequencies in speech, literature, media, and web text — "
        "making them reliable learning targets regardless of which frequency list you use."
    )
    lines.append("")

    lines.append("### High-variance words are often kanji/kana spelling alternates")
    lines.append("")
    lines.append(
        "Many highly contested words are archaic or literary kanji spellings of common words: "
        "其れ (それ), 此れ (これ), 此の (この), 矢張り (やはり), 為る (する). "
        "Literary corpora (AOZORA, NOVELS) rank these as frequent; "
        "modern web/subtitle corpora rarely see them, assigning rare or advanced tiers. "
        "The underlying word is common, but its kanji spelling is domain-specific."
    )
    lines.append("")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
