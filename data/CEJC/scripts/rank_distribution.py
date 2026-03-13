#!/usr/bin/env python3
"""
rank_distribution.py — Analysis of the competition-ranking structure in CEJC.

The dataset uses standard competition ranking (1224): words with identical
corpus frequency share the same rank, and the next rank skips accordingly.
This creates enormous tie-groups at lower frequency levels.

Output: Markdown with ASCII charts and tables to stdout.

Usage:
    python3 scripts/rank_distribution.py <tsv_path>

Example:
    python3 scripts/rank_distribution.py 2_cejc_frequencylist_suw_token.tsv
"""

import csv
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from utils import markdown_table, ascii_bar_chart

BAR_WIDTH = 50


def run(tsv_path: str) -> None:
    rank_counts: Counter = Counter()
    word_freq: dict[int, int] = {}  # rank → corpus frequency

    with open(tsv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            rank = int(row["rank"])
            rank_counts[rank] += 1
            word_freq[rank] = int(row["frequency"])

    total_rows   = sum(rank_counts.values())
    unique_ranks = len(rank_counts)
    max_rank     = max(rank_counts)
    singleton_ranks = sum(1 for c in rank_counts.values() if c == 1)
    tied_ranks      = unique_ranks - singleton_ranks
    tied_rows       = sum(c for c in rank_counts.values() if c > 1)

    print("# Rank Distribution Analysis")
    print()
    print("**Source:** CEJC — Corpus of Everyday Japanese Conversation")
    print()
    print(
        "The CEJC dataset uses **standard competition ranking (1224-ranking)**: "
        "words with the same corpus frequency share the same rank, and the next rank "
        "skips accordingly. This contrasts with dense ranking (1223), where the next "
        "rank would be +1 regardless of ties.\n"
        "\n"
        "The consequence: while the highest rank value is **{max_rank:,}**, there are "
        "only **{unique_ranks:,} distinct frequency levels** across all **{total_rows:,} entries**. "
        "At the bottom of the frequency spectrum, thousands of rare words all appear "
        "the same number of times — and all share one enormous rank tier.".format(
            max_rank=max_rank,
            unique_ranks=unique_ranks,
            total_rows=total_rows,
        )
    )
    print()

    # ── Dataset overview ───────────────────────────────────────────────────────
    print("## Dataset Overview")
    print()
    print(markdown_table(
        ["Metric", "Value"],
        [
            ["Total entries (rows)",         f"{total_rows:,}"],
            ["Unique rank values",           f"{unique_ranks:,}"],
            ["Highest rank value",           f"{max_rank:,}"],
            ["Ranks with exactly 1 entry",   f"{singleton_ranks:,}"],
            ["Ranks with 2+ entries (ties)", f"{tied_ranks:,}"],
            ["Entries caught in tie-groups", f"{tied_rows:,}"],
        ]
    ))
    print()

    # ── Top tie-groups ─────────────────────────────────────────────────────────
    print("## Largest Tie-Groups")
    print()
    print(
        "The following ranks have the most entries sharing the same rank value. "
        "Each group represents words that appeared an identical number of times "
        "in the corpus. The enormous size of the bottom tier — where thousands of "
        "words all appeared just once or twice — is the defining feature of this dataset."
    )
    print()

    top_ties = sorted(rank_counts.items(), key=lambda x: -x[1])[:15]
    rows = []
    cumulative = 0
    for rank, count in top_ties:
        cumulative += count
        freq = word_freq.get(rank, 0)
        rows.append([
            f"{rank:,}",
            f"{count:,}",
            f"{freq:,}",
            f"{count / total_rows * 100:.1f}%",
            f"{cumulative / total_rows * 100:.1f}%",
        ])

    print(markdown_table(
        ["Rank", "Entries sharing this rank", "Corpus freq (each)", "% of dataset", "Cumulative %"],
        rows,
    ))
    print()

    # Bar chart of top tie-groups
    bar_items = [(f"rank {r:>6,}", c) for r, c in top_ties]
    print(ascii_bar_chart(bar_items, fence=True, max_bar=BAR_WIDTH))
    print()

    # ── Singleton vs tie summary ────────────────────────────────────────────────
    print("## Singleton vs Tie-Group Entries")
    print()
    print(
        "Words at the top of the frequency spectrum are unique enough to have their "
        "own rank (singletons). Words at the bottom share ranks with hundreds or "
        "thousands of others that appeared equally rarely."
    )
    print()

    singleton_entry_count = sum(c for c in rank_counts.values() if c == 1)
    print(markdown_table(
        ["Category", "Distinct ranks", "Total entries", "% of entries"],
        [
            ["Singleton ranks (no ties)", f"{singleton_ranks:,}", f"{singleton_entry_count:,}",
             f"{singleton_entry_count / total_rows * 100:.1f}%"],
            ["Tie-group ranks (2+ entries)", f"{tied_ranks:,}", f"{tied_rows:,}",
             f"{tied_rows / total_rows * 100:.1f}%"],
        ]
    ))
    print()

    # ── Tie-group size distribution ─────────────────────────────────────────────
    print("## Tie-Group Size Distribution")
    print()
    print(
        "How many tie-groups exist of each size? "
        "Most tie-groups are small (2–10 entries), but a handful of massive groups "
        "at the bottom of the frequency list dominate the dataset."
    )
    print()

    # group_size → how many rank tiers have that group size
    size_dist: Counter = Counter(c for c in rank_counts.values() if c > 1)

    ranges = [
        ("2–5",       lambda k: 2 <= k <= 5),
        ("6–20",      lambda k: 6 <= k <= 20),
        ("21–100",    lambda k: 21 <= k <= 100),
        ("101–500",   lambda k: 101 <= k <= 500),
        ("501–2000",  lambda k: 501 <= k <= 2000),
        ("2001–5000", lambda k: 2001 <= k <= 5000),
        ("5000+",     lambda k: k > 5000),
    ]

    table_rows = []
    for label, pred in ranges:
        n_tiers   = sum(v for k, v in size_dist.items() if pred(k))
        n_entries = sum(k * v for k, v in size_dist.items() if pred(k))
        table_rows.append([label, f"{n_tiers:,}", f"{n_entries:,}"])

    print(markdown_table(
        ["Group size", "# of rank tiers", "Total entries in these tiers"],
        table_rows,
    ))
    print()

    # ── Key insights ────────────────────────────────────────────────────────────
    biggest_rank, biggest_count = top_ties[0]
    biggest_freq = word_freq.get(biggest_rank, 0)
    top_singleton = sorted(
        ((r, c) for r, c in rank_counts.items() if c == 1),
        key=lambda x: x[0]
    )[-1]

    print("## Key Insights")
    print()
    print(
        f"- **The dataset uses standard competition (1224) ranking, not dense ranking.** "
        f"There are {unique_ranks:,} distinct frequency levels but the highest rank value "
        f"is {max_rank:,} — a gap of {max_rank - unique_ranks:,} — caused entirely by "
        f"tie-induced rank jumps."
    )
    print()
    print(
        f"- **The largest tie-group (rank {biggest_rank:,}) contains {biggest_count:,} entries** "
        f"— {biggest_count / total_rows * 100:.1f}% of the entire dataset. "
        f"Every word in this group appeared exactly {biggest_freq:,} time(s) in the corpus. "
        f"This is the long tail of rare vocabulary in action."
    )
    print()
    print(
        f"- **Only {singleton_ranks:,} words have a frequency unique enough to earn their own rank.** "
        f"These are the high-frequency words where even small differences in usage count "
        f"result in distinct rankings."
    )
    print()
    print(
        f"- **The last singleton rank is {top_singleton[0]:,}**, meaning words ranked "
        f"{top_singleton[0] + 1:,} and below all share their rank with at least one other word. "
        f"Past this point, the corpus can no longer distinguish relative frequency."
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 rank_distribution.py <tsv_path>")
        sys.exit(1)
    run(sys.argv[1])
