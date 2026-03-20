"""
bucket_category_tables.py — Generate category tier breakdown tables using the Bucket Count Algorithm.

Algorithm:
  For each word:
    1. Collect valid (non -1) ranks from all shortlisted sources.
    2. Require at least N sources (threshold). If fewer → UNRANKED.
    3. Count how many valid ranks fall into each tier bucket
       (BASIC / COMMON / FLUENT / ADVANCED).
    4. Assign the tier with the highest count.
       Ties broken by preferring the higher tier (BASIC > COMMON > FLUENT > ADVANCED).

Contrast with the Single Rank (minimum) algorithm in SINGLE_RANK.md:
  - Minimum: a word gets a good tier if *any* source ranks it highly.
  - Bucket: a word gets a good tier if *most* sources rank it in that tier.

Reads data/ALL/RIRIKKU_CONSOLIDATED.csv and prints markdown tables for:
  - Type A tier ranges (BASIC 1–1,800 / COMMON 1,801–5,000 / FLUENT 5,001–12,000 / ADVANCED 12,001–25,000)
  - Type B tier ranges (BASIC 1–1,000 / COMMON 1,001–4,000 / FLUENT 4,001–10,000 / ADVANCED 10,001–25,000)

For each type, shows word counts at thresholds >=2, >=3, >=4.

Run from the repo root:
    python data/ALL/___experiments3/bucket_category_tables.py
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


def load_source_ranks():
    """Return list of valid-rank lists per word (non -1 values only)."""
    rows = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sources = [int(row[c]) for c in SHORTLISTED if int(row[c]) != -1]
            rows.append(sources)
    return rows


def assign_bucket_tier(valid_ranks, tiers):
    """
    Count how many ranks fall in each tier bucket, return the winning tier name.
    Ties are broken by preferring higher tiers (earlier in the tiers list).
    Returns None if no rank falls in any bucket (shouldn't happen with 1–25k data).
    """
    counts = {name: 0 for name, _, _ in tiers}
    for r in valid_ranks:
        for name, lo, hi in tiers:
            if lo <= r <= hi:
                counts[name] += 1
                break
    # Find tier with max count; prefer earlier (higher) tier on tie
    best_name = None
    best_count = -1
    for name, _, _ in tiers:
        if counts[name] > best_count:
            best_count = counts[name]
            best_name = name
    return best_name if best_count > 0 else None


def compute_stats(rows, threshold, tiers):
    tier_names = [name for name, _, _ in tiers]
    counts = {name: 0 for name in tier_names}
    ranked = 0
    unranked = 0
    for valid_ranks in rows:
        if len(valid_ranks) >= threshold:
            ranked += 1
            tier = assign_bucket_tier(valid_ranks, tiers)
            if tier is not None:
                counts[tier] += 1
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
        ranked_str = f"**{fmt(ranked)}**" if threshold == 3 else fmt(ranked)
        unranked_str = f"**{fmt(unranked)}**" if threshold == 3 else fmt(unranked)
        print(f"| {t_str} | {ranked_str} | {tier_vals} | {unranked_str} |")


def print_tier_ranges(tiers, label):
    print(f"\n### Category Rank Ranges ({label})\n")
    rows = load_source_ranks()
    _, _, _, counts_3 = compute_stats(rows, 3, tiers)
    print("| Tier     | Rank range    | Word count ≥3 |")
    print("| -------- | ------------- | ------------- |")
    for name, lo, hi in tiers:
        lo_s = f"{lo:,}"
        hi_s = f"{hi:,}"
        print(f"| {name:<8} | {lo_s}–{hi_s:<5}       | {counts_3[name]:,}         |")


if __name__ == "__main__":
    rows = load_source_ranks()
    total_words = len(rows)
    print(f"Total words in RIRIKKU_CONSOLIDATED.csv: {total_words:,}\n")
    print("Algorithm: Bucket Count")
    print("  Each word's tier = the tier bucket containing the most of its valid source ranks.")
    print("  Ties broken by preferring higher tier (BASIC > COMMON > FLUENT > ADVANCED).\n")

    print_tier_ranges(TYPE_A, "Type A")
    print_table(rows, TYPE_A, "Threshold Comparison — Type A (Bucket Count)")

    print_tier_ranges(TYPE_B, "Type B")
    print_table(rows, TYPE_B, "Threshold Comparison — Type B (Bucket Count)")
