#!/usr/bin/env python3
"""
pmw_variance.py — Context-sensitivity analysis.

Words with LOW PMW variance across domains/demographics are "universal" —
they appear at similar rates everywhere. Words with HIGH variance are
"contextual" — they spike in specific situations or for specific speakers.

Output: Markdown tables to stdout.

Usage:
    python3 pmw_variance.py <json_dir>
"""

import sys
import statistics
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[3]))

from loaders import load_cejc_json
from analysis import tier_slice
from utils import markdown_table

# Analyse words within the top N by overall rank
ANALYSIS_TIER = 5000
TOP_N_SHOW    = 25  # rows in each table

DOMAINS = [
    "small_talk", "consultation", "meeting", "class",
    "outdoors", "school", "transportation", "public_commercial",
    "home", "indoors", "workplace",
]

DOMAIN_EN = {
    "small_talk":        "Small Talk",
    "consultation":      "Consultation",
    "meeting":           "Meeting",
    "class":             "Class/Lesson",
    "outdoors":          "Outdoors",
    "school":            "School",
    "transportation":    "Transportation",
    "public_commercial": "Public/Commercial",
    "home":              "Home",
    "indoors":           "Indoors",
    "workplace":         "Workplace",
}

AGE_GROUPS = [
    "0_4", "5_9", "10_14", "15_19", "20_24", "25_29",
    "30_34", "35_39", "40_44", "45_49", "50_54", "55_59",
    "60_64", "65_69", "70_74", "75_79", "80_84", "85_89",
    "90_94", "unknown",
]

GENDER_DEMO = ["m", "f"]
ALL_DEMO    = GENDER_DEMO + AGE_GROUPS


def pmw_values(entry: dict, keys: list[str], field: str) -> list[float]:
    """Extract non-zero PMW values for a list of keys from entry[field]."""
    vals = []
    for k in keys:
        v = entry[field].get(k)
        if v and v[2] > 0:
            vals.append(v[2])
    return vals


def cv(values: list[float]) -> float:
    """Coefficient of variation = stdev / mean. Returns 0 if < 2 values."""
    if len(values) < 2:
        return 0.0
    m = statistics.mean(values)
    return statistics.stdev(values) / m if m > 0 else 0.0


def analyse(data: dict) -> list[dict]:
    """Build per-entry stats for the analysis tier."""
    sliced  = tier_slice(data, ANALYSIS_TIER)
    records = []

    for word, entries in sliced.items():
        for entry in entries:
            overall_pmw = entry["combined"][2]
            if overall_pmw == 0:
                continue

            domain_pmws = pmw_values(entry, DOMAINS, "domains")
            demo_pmws   = pmw_values(entry, ALL_DEMO, "demographics")

            domain_cv   = cv(domain_pmws)
            demo_cv     = cv(demo_pmws)

            # Dominant domain: domain with highest PMW
            dom_pmw_map = {
                k: entry["domains"][k][2]
                for k in DOMAINS
                if entry["domains"][k][2] > 0
            }
            dominant_domain = (
                DOMAIN_EN.get(max(dom_pmw_map, key=dom_pmw_map.get), "—")
                if dom_pmw_map else "—"
            )

            records.append({
                "word":           word,
                "reading":        entry["reading"],
                "pos":            entry["pos"],
                "overall_rank":   entry["combined"][0],
                "overall_pmw":    overall_pmw,
                "domain_cv":      domain_cv,
                "demo_cv":        demo_cv,
                "domain_count":   len(domain_pmws),
                "dominant_domain": dominant_domain,
            })

    return records


def run(json_dir: str) -> None:
    data    = load_cejc_json(json_dir)
    records = analyse(data)

    print("# PMW Variance — Context-Sensitivity Analysis")
    print()
    print("**Source:** CEJC — Corpus of Everyday Japanese Conversation")
    print()
    print(
        "**PMW (per-million-words)** measures how often a word appears per million "
        "words of text. Because different domains and demographic groups have different "
        "total word counts, PMW is the right measure for cross-context comparison.\n"
        "\n"
        "This analysis uses the **coefficient of variation (CV = σ/μ)** across "
        "PMW values to measure context-sensitivity:\n"
        "- **Low CV** → the word appears at roughly the same rate everywhere — "
        "it is *universal*\n"
        "- **High CV** → the word's frequency spikes in certain contexts and is "
        "rare in others — it is *contextual*\n"
        "\n"
        f"Analysis covers the top {ANALYSIS_TIER:,} words by overall rank."
    )
    print()

    # ── Domain variance ────────────────────────────────────────────────────
    print("## Domain Context-Sensitivity")
    print()
    print(
        "How much does a word's frequency vary across the 11 conversation domains "
        "(small talk, meeting, school, workplace, etc.)? "
        "High-variance words are strongly tied to specific settings; "
        "low-variance words are used equally everywhere."
    )
    print()

    # Filter to entries with data in at least 4 domains
    domain_records = [r for r in records if r["domain_count"] >= 4]
    domain_records.sort(key=lambda r: r["domain_cv"], reverse=True)

    print("### Most Contextual Words (highest domain CV — appear unevenly across domains)")
    print()
    print(markdown_table(
        ["Word", "Reading", "POS", "Overall Rank", "Domain CV", "Dominant Domain"],
        [
            [r["word"], r["reading"], r["pos"],
             r["overall_rank"], f"{r['domain_cv']:.2f}", r["dominant_domain"]]
            for r in domain_records[:TOP_N_SHOW]
        ],
    ))
    print()

    domain_records_asc = sorted(
        [r for r in domain_records if r["domain_cv"] > 0],
        key=lambda r: r["domain_cv"],
    )
    print("### Most Universal Words (lowest domain CV — appear evenly across all domains)")
    print()
    print(
        "These words are the true backbone of spoken Japanese — they appear "
        "at similar rates whether you're at work, school, home, or on a train."
    )
    print()
    print(markdown_table(
        ["Word", "Reading", "POS", "Overall Rank", "Domain CV"],
        [
            [r["word"], r["reading"], r["pos"],
             r["overall_rank"], f"{r['domain_cv']:.2f}"]
            for r in domain_records_asc[:TOP_N_SHOW]
        ],
    ))
    print()

    # ── Demographic variance ───────────────────────────────────────────────
    print("## Demographic Context-Sensitivity")
    print()
    print(
        "How much does a word's frequency vary across speaker demographics "
        "(gender + age groups)? High-variance words are strongly associated "
        "with particular speaker profiles."
    )
    print()

    demo_records = [r for r in records if r["demo_cv"] > 0]
    demo_records.sort(key=lambda r: r["demo_cv"], reverse=True)

    print("### Most Demographically Skewed Words (highest demographic CV)")
    print()
    print(markdown_table(
        ["Word", "Reading", "POS", "Overall Rank", "Demo CV"],
        [
            [r["word"], r["reading"], r["pos"],
             r["overall_rank"], f"{r['demo_cv']:.2f}"]
            for r in demo_records[:TOP_N_SHOW]
        ],
    ))
    print()

    demo_universal = sorted(demo_records, key=lambda r: r["demo_cv"])
    print("### Most Demographically Universal Words (lowest demographic CV)")
    print()
    print(
        "These words appear at consistent rates across all age groups and both "
        "genders — they are part of every Japanese speaker's core vocabulary."
    )
    print()
    print(markdown_table(
        ["Word", "Reading", "POS", "Overall Rank", "Demo CV"],
        [
            [r["word"], r["reading"], r["pos"],
             r["overall_rank"], f"{r['demo_cv']:.2f}"]
            for r in demo_universal[:TOP_N_SHOW]
        ],
    ))
    print()

    # ── Combined universality ranking ──────────────────────────────────────
    print("## Most Universal Words Overall (low variance across both domains AND demographics)")
    print()
    print(
        "Words ranked by combined context-sensitivity score (domain CV + demographic CV). "
        "These are the most reliably high-frequency words regardless of *where* or "
        "*by whom* a conversation is taking place. A language learner prioritising "
        "these words will be prepared for virtually any spoken context."
    )
    print()

    combined = [
        r for r in records
        if r["domain_count"] >= 4 and r["demo_cv"] > 0
    ]
    combined.sort(key=lambda r: r["domain_cv"] + r["demo_cv"])

    print(markdown_table(
        ["Word", "Reading", "POS", "Overall Rank", "Overall PMW", "Domain CV", "Demo CV"],
        [
            [r["word"], r["reading"], r["pos"],
             r["overall_rank"], f"{r['overall_pmw']:.1f}",
             f"{r['domain_cv']:.2f}", f"{r['demo_cv']:.2f}"]
            for r in combined[:TOP_N_SHOW]
        ],
    ))
    print()

    # ── Key insights ───────────────────────────────────────────────────────
    print("## Key Insights")
    print()
    top_ctx   = domain_records[:3]
    top_univ  = domain_records_asc[:3]
    print(
        f"- **Most contextual words** (highest domain CV): "
        + ", ".join(f"{r['word']} ({r['dominant_domain']})" for r in top_ctx)
        + ". These words spike in their dominant domain and are rarely used elsewhere."
    )
    print()
    print(
        f"- **Most universal words** (lowest domain CV): "
        + ", ".join(f"{r['word']} ({r['reading']})" for r in top_univ)
        + ". These appear at the same rate regardless of conversational context."
    )
    print()
    print(
        "- **Domain variance tends to be higher than demographic variance** "
        "for most words. This suggests that *what you're talking about* "
        "(domain) has more influence on word choice than *who you are* (gender/age)."
    )
    print()
    print(
        "- **Low-rank (high-frequency) words are generally more universal.** "
        "Function words, auxiliaries, and core verbs appear everywhere. "
        "Content words (especially nouns) are much more context-dependent."
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 pmw_variance.py <json_dir>")
        sys.exit(1)
    run(sys.argv[1])
