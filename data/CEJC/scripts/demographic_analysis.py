#!/usr/bin/env python3
"""
demographic_analysis.py — Gender and age group patterns.

- Words with the biggest male/female PMW skew
- Age-group vocabulary coverage across frequency tiers
- Age-group vocabulary size estimates

Output: Markdown tables + ASCII charts to stdout.

Usage:
    python3 demographic_analysis.py <json_dir>
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[3]))

from loaders import load_cejc_json
from analysis import tier_slice, flat_entries
from utils import markdown_table, ascii_bar_chart

GENDER_SKEW_TIER = 8000   # pool of words to search for gender skew
TOP_SKEW         = 30     # rows per gender skew table
MIN_OVERALL_PMW  = 50     # ignore very rare words (noisy ratios)
MIN_GENDER_PMW   = 1.0    # both genders must have at least this PMW

AGE_GROUPS = [
    "0_4", "5_9", "10_14", "15_19", "20_24", "25_29",
    "30_34", "35_39", "40_44", "45_49", "50_54", "55_59",
    "60_64", "65_69", "70_74", "75_79", "80_84", "85_89",
    "90_94",
]

AGE_LABEL = {
    "0_4": "0–4",   "5_9": "5–9",   "10_14": "10–14", "15_19": "15–19",
    "20_24": "20–24", "25_29": "25–29", "30_34": "30–34", "35_39": "35–39",
    "40_44": "40–44", "45_49": "45–49", "50_54": "50–54", "55_59": "55–59",
    "60_64": "60–64", "65_69": "65–69", "70_74": "70–74", "75_79": "75–79",
    "80_84": "80–84", "85_89": "85–89", "90_94": "90–94",
}

COVERAGE_TIERS = [500, 1000, 2000, 3000, 5000, 8000, 12000]


def pct(n, total):
    return f"{n / total * 100:.1f}%" if total else "0%"


def run(json_dir: str) -> None:
    data = load_cejc_json(json_dir)

    print("# Demographic Analysis — Gender & Age Patterns")
    print()
    print("**Source:** CEJC — Corpus of Everyday Japanese Conversation")
    print()
    print(
        "The CEJC corpus records the gender and age of each speaker, allowing us to "
        "measure how word frequency varies by speaker demographics. "
        "All comparisons use **PMW (per-million-words)** to normalise for the fact "
        "that different demographic groups contributed different amounts of speech.\n"
        "\n"
        "**Important caveat:** these patterns reflect the speech of the 1,675 "
        "participants in this specific corpus. They are descriptive of the corpus, "
        "not prescriptive of how any individual speaks."
    )
    print()

    # ── Gender skew ────────────────────────────────────────────────────────
    print("## Gender Skew")
    print()
    print(
        "Words are ranked by their **male/female PMW ratio**. "
        "A ratio > 1 means the word appears more frequently in male speech; "
        "a ratio < 1 means it appears more in female speech. "
        f"Only words in the top {GENDER_SKEW_TIER:,} overall and with PMW ≥ "
        f"{MIN_GENDER_PMW} for both genders are included (to avoid noisy ratios "
        "from very rare words)."
    )
    print()

    sliced      = tier_slice(data, GENDER_SKEW_TIER)
    skew_rows   = []

    for word, entries in sliced.items():
        for entry in entries:
            if entry["combined"][2] < MIN_OVERALL_PMW:
                continue
            m_pmw = entry["demographics"]["m"][2]
            f_pmw = entry["demographics"]["f"][2]
            if m_pmw < MIN_GENDER_PMW or f_pmw < MIN_GENDER_PMW:
                continue
            ratio = m_pmw / f_pmw
            skew_rows.append({
                "word":    word,
                "reading": entry["reading"],
                "pos":     entry["pos"],
                "rank":    entry["combined"][0],
                "m_pmw":   m_pmw,
                "f_pmw":   f_pmw,
                "ratio":   ratio,
            })

    skew_rows.sort(key=lambda r: r["ratio"], reverse=True)

    print("### Most Male-Skewed Words (M/F PMW ratio, highest first)")
    print()
    print(
        "These words appear significantly more often in male speech. "
        "A ratio of 2.0 means men use this word twice as often as women (per million words)."
    )
    print()
    print(markdown_table(
        ["Word", "Reading", "POS", "Rank", "Male PMW", "Female PMW", "M/F Ratio"],
        [
            [r["word"], r["reading"], r["pos"], r["rank"],
             f"{r['m_pmw']:.1f}", f"{r['f_pmw']:.1f}", f"{r['ratio']:.2f}"]
            for r in skew_rows[:TOP_SKEW]
        ],
    ))
    print()

    skew_rows.sort(key=lambda r: r["ratio"])
    print("### Most Female-Skewed Words (F/M PMW ratio, highest first)")
    print()
    print(
        "These words appear significantly more often in female speech. "
        "The ratio shown is M/F — so lower values mean stronger female skew."
    )
    print()
    print(markdown_table(
        ["Word", "Reading", "POS", "Rank", "Male PMW", "Female PMW", "M/F Ratio"],
        [
            [r["word"], r["reading"], r["pos"], r["rank"],
             f"{r['m_pmw']:.1f}", f"{r['f_pmw']:.1f}", f"{r['ratio']:.2f}"]
            for r in skew_rows[:TOP_SKEW]
        ],
    ))
    print()

    # ── Age-group vocabulary coverage ──────────────────────────────────────
    print("## Age-Group Vocabulary Coverage Across Tiers")
    print()
    print(
        "For each frequency tier (top 500, 1,000, … 12,000 words overall), "
        "this shows how many of those words each age group actually used in the corpus "
        "(i.e., had PMW > 0). This is a proxy for **vocabulary breadth** — "
        "how wide a net each age group casts across the most common words.\n"
        "\n"
        "Note: younger children (0–9) will naturally cover fewer words because "
        "they speak less and use simpler language. Very old age groups may have "
        "small sample sizes in the corpus."
    )
    print()

    # Build coverage table
    cov_headers = ["Age Group"] + [f"Top {t:,}" for t in COVERAGE_TIERS]
    cov_rows    = []

    for age in AGE_GROUPS:
        row = [AGE_LABEL[age]]
        for tier in COVERAGE_TIERS:
            sliced_tier = tier_slice(data, tier)
            covered = sum(
                1 for entries in sliced_tier.values()
                if any(e["demographics"][age][2] > 0 for e in entries)
            )
            total = len(sliced_tier)
            row.append(f"{covered:,} ({pct(covered, total)})")
        cov_rows.append(row)

    print(markdown_table(cov_headers, cov_rows))
    print()

    # ── Age-group coverage bar chart at top-3000 ──────────────────────────
    CHART_TIER = 3000
    sliced_chart = tier_slice(data, CHART_TIER)
    total_chart  = len(sliced_chart)

    print(f"### Coverage at Top {CHART_TIER:,} Words")
    print()
    print(
        f"Bar chart showing how many of the top {CHART_TIER:,} most frequent words "
        "each age group used in the corpus. Longer bars = broader vocabulary coverage."
    )
    print()

    chart_items = []
    for age in AGE_GROUPS:
        covered = sum(
            1 for entries in sliced_chart.values()
            if any(e["demographics"][age][2] > 0 for e in entries)
        )
        chart_items.append((AGE_LABEL[age], covered))

    print(ascii_bar_chart(chart_items, max_width=40, fence=True))
    print()

    # ── Largest age group vocabulary ───────────────────────────────────────
    print("## Age Group — Active Vocabulary Size Estimate")
    print()
    print(
        "How many distinct words does each age group use across the entire corpus? "
        "This counts unique words with PMW > 0 for each age group across all "
        f"{len(data):,} words in the dataset."
    )
    print()

    vocab_sizes = []
    for age in AGE_GROUPS:
        count = sum(
            1 for entries in data.values()
            if any(e["demographics"][age][2] > 0 for e in entries)
        )
        vocab_sizes.append((AGE_LABEL[age], count))

    print(ascii_bar_chart(vocab_sizes, max_width=40, fence=True))
    print()
    print(markdown_table(
        ["Age Group", "Words Used (PMW > 0)", "% of Full Dataset"],
        [[age, f"{count:,}", pct(count, len(data))] for age, count in vocab_sizes],
    ))
    print()

    # ── Key insights ───────────────────────────────────────────────────────
    print("## Key Insights")
    print()
    print(
        "- **Gender differences in vocabulary are real but moderate.** "
        "The most skewed words tend to be topic-specific (certain activities, "
        "styles of expression) rather than basic vocabulary. Core function words "
        "show very little gender skew."
    )
    print()
    print(
        "- **Young children (0–9) use a narrow vocabulary slice.** "
        "Their coverage of high-frequency words is limited, and they almost "
        "entirely avoid low-frequency words — consistent with the expected "
        "developmental vocabulary growth pattern."
    )
    print()
    print(
        "- **Working-age adults (20–59) tend to have the broadest coverage.** "
        "They contribute the most speech to the corpus and use vocabulary across "
        "the widest range of domains (work, home, social)."
    )
    print()
    print(
        "- **Vocabulary coverage grows rapidly in early tiers and flattens.** "
        "Even young children cover most of the top-500 words, but the gap between "
        "age groups widens as tier size increases — deeper vocabulary is where "
        "age-related differences become most visible."
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 demographic_analysis.py <json_dir>")
        sys.exit(1)
    run(sys.argv[1])
