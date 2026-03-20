"""
category_tables.py — Generate category tier breakdown tables for SINGLE_RANK.md.

Reads data/ALL/RIRIKKU_CONSOLIDATED.csv and prints markdown tables for:
  - Type A tier ranges (BASIC 1–1,800 / COMMON 1,801–5,000 / FLUENT 5,001–12,000 / ADVANCED 12,001–25,000)
  - Type B tier ranges (BASIC 1–1,000 / COMMON 1,001–4,000 / FLUENT 4,001–10,000 / ADVANCED 10,001–25,000)

For each type, shows word counts at thresholds >=2, >=3, >=4.

Run from the repo root:
    python data/ALL/___experiments3/category_tables.py
"""

import csv
import os

csv.field_size_limit(10_000_000)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CSV_PATH = os.path.join(ROOT, "data", "ALL", "RIRIKKU_CONSOLIDATED.csv")

SHORTLISTED = [
    "RSPEER",
    "cejc_combined_rank",
    "cejc_small_talk_rank",
    "BCCWJ_LUW",
    "BCCWJ_SUW",
    "CC100",
    "MALTESAA_NWJC",
    "JITEN_GLOBAL",
    "JITEN_DRAMA",
    "ANIME_JDRAMA",
    "YOUTUBE_FREQ_V3",
    "NETFLIX",
    "DD2_MORPHMAN_NETFLIX",
    "WIKIPEDIA_V2",
    "ADNO",
    "DD2_MORPHMAN_SOL",
]

TYPE_A = [
    ("BASIC",    1,     1_800),
    ("COMMON",   1_801, 5_000),
    ("FLUENT",   5_001, 12_000),
    ("ADVANCED", 12_001, 25_000),
]

TYPE_B = [
    ("BASIC",    1,     1_000),
    ("COMMON",   1_001, 4_000),
    ("FLUENT",   4_001, 10_000),
    ("ADVANCED", 10_001, 25_000),
]


def load_source_counts():
    """Return list of (source_count_list) per word — only the valid (non -1) source counts."""
    rows = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sources = [int(row[c]) for c in SHORTLISTED if int(row[c]) != -1]
            rows.append(sources)
    return rows


def compute_stats(rows, threshold, tiers):
    counts = {name: 0 for name, _, _ in tiers}
    ranked = 0
    unranked = 0
    for sources in rows:
        if len(sources) >= threshold:
            r = min(sources)
            ranked += 1
            for name, lo, hi in tiers:
                if lo <= r <= hi:
                    counts[name] += 1
                    break
        else:
            unranked += 1
    total = ranked + unranked
    return total, ranked, unranked, counts


def fmt(n):
    return f"{n:,}"


def print_table(rows, tiers, label):
    tier_names = [name for name, _, _ in tiers]
    header = "| Threshold | TOTAL | " + " | ".join(tier_names) + " | Unranked |"
    sep    = "| --------- | ----- | " + " | ".join(["------"] * len(tier_names)) + " | -------- |"
    print(f"\n### {label}\n")
    print(header)
    print(sep)
    for threshold in [2, 3, 4]:
        total, ranked, unranked, counts = compute_stats(rows, threshold, tiers)
        mark = " ✅" if threshold == 3 else ""
        t_str = f"**≥{threshold}**{mark}" if threshold == 3 else f"≥{threshold}"
        tier_vals = " | ".join(f"**{fmt(counts[n])}**" if threshold == 3 else fmt(counts[n]) for n in tier_names)
        # TOTAL = ranked count (words that pass the threshold), Unranked = words that don't
        ranked_str = f"**{fmt(ranked)}**" if threshold == 3 else fmt(ranked)
        unranked_str = f"**{fmt(unranked)}**" if threshold == 3 else fmt(unranked)
        print(f"| {t_str} | {ranked_str} | {tier_vals} | {unranked_str} |")


def print_tier_ranges(tiers, label):
    print(f"\n### Category Rank Ranges ({label})\n")
    _, _, _, counts_3 = compute_stats(load_source_counts(), 3, tiers)
    print("| Tier     | Rank range    | Word count ≥3 |")
    print("| -------- | ------------- | ------------- |")
    for name, lo, hi in tiers:
        lo_s = f"{lo:,}"
        hi_s = f"{hi:,}"
        print(f"| {name:<8} | {lo_s}–{hi_s:<5}       | {counts_3[name]:,}         |")


if __name__ == "__main__":
    rows = load_source_counts()
    total_words = len(rows)
    print(f"Total words in RIRIKKU_CONSOLIDATED.csv: {total_words:,}\n")

    print_tier_ranges(TYPE_A, "Type A")
    print_table(rows, TYPE_A, "Threshold Comparison — Type A")

    print_tier_ranges(TYPE_B, "Type B")
    print_table(rows, TYPE_B, "Threshold Comparison — Type B")
