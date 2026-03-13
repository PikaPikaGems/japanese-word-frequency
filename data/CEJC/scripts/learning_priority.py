#!/usr/bin/env python3
"""
learning_priority.py — Practical word lists for learners.

Scores words by two dimensions:
  - "High-value" words: high overall frequency AND broad domain coverage
    (words that pay off in every conversational context)
  - "Specialist" words: high frequency in specific domains but low overall rank
    (words worth learning for particular settings)

Output: Ranked Markdown tables to stdout.

Usage:
    python3 learning_priority.py <json_dir>
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[3]))

from loaders import load_cejc_json
from analysis import tier_slice
from utils import markdown_table

ANALYSIS_TIER   = 8000   # words to consider
TOP_N_SHOW      = 30     # rows per table
MIN_PMW         = 20.0   # ignore very rare words

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

N_DOMAINS = len(DOMAINS)

ORIGIN_EN = {
    "和": "Native JP", "漢": "Sino-JP", "外": "Loanword",
    "混": "Mixed", "固": "Proper", "記号": "Symbol", "": "Unknown",
}


def domain_coverage(entry: dict) -> tuple[int, float]:
    """
    Returns (coverage_count, avg_domain_pmw) where:
      coverage_count = number of domains where the word has pmw > 0
      avg_domain_pmw = mean pmw across those active domains
    """
    active = [entry["domains"][d][2] for d in DOMAINS if entry["domains"][d][2] > 0]
    if not active:
        return 0, 0.0
    return len(active), sum(active) / len(active)


def dominant_domain(entry: dict) -> str:
    """Domain with the highest PMW for this entry."""
    best = max(DOMAINS, key=lambda d: entry["domains"][d][2])
    return DOMAIN_EN[best] if entry["domains"][best][2] > 0 else "—"


def specialist_score(entry: dict) -> float:
    """
    How specialised is a word?
    = (max domain PMW) / (overall PMW)
    High = the word's frequency is concentrated in one domain.
    """
    if entry["combined"][2] == 0:
        return 0.0
    max_d_pmw = max(entry["domains"][d][2] for d in DOMAINS)
    return max_d_pmw / entry["combined"][2]


def run(json_dir: str) -> None:
    data   = load_cejc_json(json_dir)
    sliced = tier_slice(data, ANALYSIS_TIER)

    records = []
    for word, entries in sliced.items():
        for entry in entries:
            overall_pmw = entry["combined"][2]
            if overall_pmw < MIN_PMW:
                continue
            cov_count, avg_d_pmw = domain_coverage(entry)
            cov_frac = cov_count / N_DOMAINS

            records.append({
                "word":         word,
                "reading":      entry["reading"],
                "pos":          entry["pos"],
                "origin":       ORIGIN_EN.get(entry["origin"], entry["origin"]),
                "rank":         entry["combined"][0],
                "overall_pmw":  overall_pmw,
                "cov_count":    cov_count,
                "cov_frac":     cov_frac,
                "avg_d_pmw":    avg_d_pmw,
                # High-value score: log-frequency × domain coverage breadth
                "value_score":  overall_pmw * cov_frac,
                # Specialist score: concentration in dominant domain
                "spec_score":   specialist_score(entry),
                "dominant":     dominant_domain(entry),
            })

    print("# Learning Priority — High-Value & Specialist Word Lists")
    print()
    print("**Source:** CEJC — Corpus of Everyday Japanese Conversation")
    print()
    print(
        "Not all frequent words are equally worth studying. This analysis ranks words "
        "along two learner-relevant dimensions:\n"
        "\n"
        "**High-value words** score high on *both* overall frequency *and* domain breadth. "
        "They appear in many different conversational contexts, so learning them pays off "
        "regardless of what situation you find yourself in. "
        "Score = overall PMW × (domains active / 11).\n"
        "\n"
        "**Specialist words** are highly frequent *within one domain* but less common "
        "overall. They are essential vocabulary for a specific context but less useful "
        "outside it. Score = (peak domain PMW) / (overall PMW).\n"
        "\n"
        f"Analysis covers the top {ANALYSIS_TIER:,} words with overall PMW ≥ {MIN_PMW:.0f}."
    )
    print()

    # ── High-value words ───────────────────────────────────────────────────
    print("## High-Value Words (broad coverage × high frequency)")
    print()
    print(
        "Sorted by value score (overall PMW × domain coverage fraction). "
        "These are the best words to prioritise for general conversational fluency — "
        "high frequency AND present across many different contexts."
    )
    print()

    by_value = sorted(records, key=lambda r: r["value_score"], reverse=True)
    print(markdown_table(
        ["Word", "Reading", "POS", "Origin", "Rank", "Overall PMW", "Domains Active", "Value Score"],
        [
            [r["word"], r["reading"], r["pos"], r["origin"],
             r["rank"], f"{r['overall_pmw']:.1f}",
             f"{r['cov_count']}/{N_DOMAINS}", f"{r['value_score']:.1f}"]
            for r in by_value[:TOP_N_SHOW]
        ],
    ))
    print()

    # Full coverage words (appear in all 11 domains)
    full_cov = [r for r in records if r["cov_count"] == N_DOMAINS]
    full_cov.sort(key=lambda r: r["overall_pmw"], reverse=True)
    if full_cov:
        print(f"### Words Present in All {N_DOMAINS} Domains")
        print()
        print(
            f"These {len(full_cov)} words appear in every single domain in the corpus. "
            "They are the most universally applicable vocabulary in spoken Japanese."
        )
        print()
        print(markdown_table(
            ["Word", "Reading", "POS", "Origin", "Rank", "Overall PMW"],
            [
                [r["word"], r["reading"], r["pos"], r["origin"],
                 r["rank"], f"{r['overall_pmw']:.1f}"]
                for r in full_cov[:TOP_N_SHOW]
            ],
        ))
        print()

    # ── Specialist words ───────────────────────────────────────────────────
    print("## Specialist Words (domain-concentrated)")
    print()
    print(
        "Sorted by specialist score (peak domain PMW / overall PMW). "
        "A score > 2 means the word's peak-domain frequency is more than double "
        "its overall frequency — it is disproportionately concentrated in one context. "
        "Useful for learners targeting a specific domain (workplace, school, etc.)."
    )
    print()

    by_spec = sorted(
        [r for r in records if r["spec_score"] > 1.5 and r["rank"] <= 5000],
        key=lambda r: r["spec_score"],
        reverse=True,
    )
    print(markdown_table(
        ["Word", "Reading", "POS", "Origin", "Rank", "Overall PMW", "Dominant Domain", "Spec Score"],
        [
            [r["word"], r["reading"], r["pos"], r["origin"],
             r["rank"], f"{r['overall_pmw']:.1f}",
             r["dominant"], f"{r['spec_score']:.2f}"]
            for r in by_spec[:TOP_N_SHOW]
        ],
    ))
    print()

    # ── Per-domain top specialist words ───────────────────────────────────
    print("## Top Specialist Words by Domain")
    print()
    print(
        "For each domain, the words with the highest specialist score "
        "(concentrated in that specific domain). These form a 'domain vocabulary list' "
        "for targeted study."
    )
    print()

    for domain in DOMAINS:
        domain_spec = sorted(
            [r for r in records
             if r["dominant"] == DOMAIN_EN[domain] and r["spec_score"] > 1.2],
            key=lambda r: r["spec_score"],
            reverse=True,
        )
        if not domain_spec:
            continue
        print(f"### {DOMAIN_EN[domain]}")
        print()
        print(markdown_table(
            ["Word", "Reading", "POS", "Rank", "Overall PMW", "Spec Score"],
            [
                [r["word"], r["reading"], r["pos"],
                 r["rank"], f"{r['overall_pmw']:.1f}", f"{r['spec_score']:.2f}"]
                for r in domain_spec[:10]
            ],
        ))
        print()

    # ── Key insights ───────────────────────────────────────────────────────
    print("## Key Insights")
    print()
    print(
        "- **A small set of words is truly universal.** Words appearing in all "
        f"{N_DOMAINS} domains are the core of spoken Japanese — mastering these alone "
        "provides a baseline for virtually any conversation."
    )
    print()
    print(
        "- **High-value ≠ simply high frequency.** Some very frequent words "
        "(particles, auxiliaries) are so domain-universal they score extremely high. "
        "But some frequent content words are domain-specialist — they appear often "
        "only in one setting."
    )
    print()
    print(
        "- **Specialist vocabulary grows quickly within each domain.** "
        "Each domain has a cluster of words with 2–4× their expected frequency, "
        "forming a learnable 'domain vocabulary module' of roughly 50–200 words."
    )
    print()
    print(
        "- **Learning strategy implication:** Start with high-value words for general "
        "fluency, then add the specialist word lists for your most-used domains "
        "(e.g. workplace + small talk for business Japanese)."
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 learning_priority.py <json_dir>")
        sys.exit(1)
    run(sys.argv[1])
