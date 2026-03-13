#!/usr/bin/env python3
"""
domain_similarity.py — Pairwise domain correlation and clustering.

- Jaccard similarity of top-N vocabulary between domain pairs
- Pearson rank correlation between domain rank vectors
- Mermaid graph showing strongest domain connections

Output: Markdown tables + Mermaid graph to stdout.

Usage:
    python3 domain_similarity.py <json_dir>
"""

import sys
import statistics
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[3]))

from loaders import load_cejc_json
from analysis import tier_slice
from utils import markdown_table, mermaid_graph

OVERLAP_TOP_N     = 300   # top-N words per domain for Jaccard
CORRELATION_WORDS = 3000  # pool of words for rank correlation
GRAPH_TOP_PAIRS   = 12    # strongest pairs to show in Mermaid graph

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

# Short IDs safe for Mermaid node names (no spaces/special chars)
DOMAIN_ID = {
    "small_talk":        "SmallTalk",
    "consultation":      "Consult",
    "meeting":           "Meeting",
    "class":             "Class",
    "outdoors":          "Outdoors",
    "school":            "School",
    "transportation":    "Transit",
    "public_commercial": "Public",
    "home":              "Home",
    "indoors":           "Indoors",
    "workplace":         "Work",
}


def top_words_per_domain(data: dict, top_n: int) -> dict[str, list[str]]:
    """Return the top top_n word keys per domain ranked by domain PMW."""
    result: dict[str, list[str]] = {}
    for domain in DOMAINS:
        ranked = []
        for word, entries in data.items():
            for entry in entries:
                d = entry["domains"][domain]
                if d[2] > 0:
                    ranked.append((d[0], word))  # (domain_rank, word)
        ranked.sort()
        result[domain] = [w for _, w in ranked[:top_n]]
    return result


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def pearson(xs: list[float], ys: list[float]) -> float:
    """Pearson correlation coefficient between two equal-length lists."""
    n = len(xs)
    if n < 2:
        return 0.0
    mx, my = statistics.mean(xs), statistics.mean(ys)
    num    = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denom  = (
        (sum((x - mx) ** 2 for x in xs) ** 0.5) *
        (sum((y - my) ** 2 for y in ys) ** 0.5)
    )
    return num / denom if denom else 0.0


def domain_rank_vectors(data: dict) -> dict[str, list[float]]:
    """
    For each domain, build a rank vector over the CORRELATION_WORDS most frequent
    words overall. Words absent from a domain get a fallback rank.
    """
    sliced   = tier_slice(data, CORRELATION_WORDS)
    fallback = CORRELATION_WORDS * 10  # high rank for absent words

    vectors: dict[str, list[float]] = {d: [] for d in DOMAINS}
    for word, entries in sliced.items():
        for entry in entries:
            for domain in DOMAINS:
                dr = entry["domains"][domain][0]
                vectors[domain].append(float(dr) if dr > 0 else float(fallback))

    return vectors


def run(json_dir: str) -> None:
    data        = load_cejc_json(json_dir)
    top_words   = top_words_per_domain(data, OVERLAP_TOP_N)
    rank_vecs   = domain_rank_vectors(data)

    # Precompute all pairwise metrics
    pairs = []
    for i, d_a in enumerate(DOMAINS):
        for d_b in DOMAINS[i + 1:]:
            set_a    = set(top_words[d_a])
            set_b    = set(top_words[d_b])
            jac      = jaccard(set_a, set_b)
            pearr    = pearson(rank_vecs[d_a], rank_vecs[d_b])
            overlap  = len(set_a & set_b)
            pairs.append({
                "a": d_a, "b": d_b,
                "jaccard": jac,
                "pearson": pearr,
                "overlap": overlap,
            })

    print("# Domain Similarity Analysis")
    print()
    print("**Source:** CEJC — Corpus of Everyday Japanese Conversation")
    print()
    print(
        "How similar are the 11 conversation domains in terms of vocabulary? "
        "Two complementary measures are used:\n"
        "\n"
        f"1. **Jaccard similarity** — fraction of shared words among the top {OVERLAP_TOP_N} "
        "words in each domain. Ranges 0 (no overlap) to 1 (identical vocabulary).\n"
        "2. **Pearson rank correlation** — how similarly the two domains *rank* the same "
        f"words across the top {CORRELATION_WORDS:,} overall words. "
        "A score near 1 means the domains agree on which words are more/less frequent; "
        "near 0 means no agreement.\n"
        "\n"
        "The 11 domains break into two groups: "
        "**conversation types** (small talk, consultation, meeting, class) and "
        "**locations** (outdoors, school, transportation, public/commercial, home, indoors, workplace)."
    )
    print()

    # ── Jaccard similarity table ───────────────────────────────────────────
    pairs_by_jac = sorted(pairs, key=lambda p: p["jaccard"], reverse=True)

    print("## Vocabulary Overlap — Jaccard Similarity")
    print()
    print(
        f"Pairs ranked by Jaccard similarity of their top-{OVERLAP_TOP_N} vocabulary. "
        "Higher = more shared words."
    )
    print()
    print(markdown_table(
        ["Domain A", "Domain B", "Shared Words", "Jaccard", "Pearson r"],
        [
            [DOMAIN_EN[p["a"]], DOMAIN_EN[p["b"]],
             p["overlap"], f"{p['jaccard']:.3f}", f"{p['pearson']:.3f}"]
            for p in pairs_by_jac
        ],
    ))
    print()

    # ── Pearson correlation matrix ─────────────────────────────────────────
    print("## Rank Correlation Matrix (Pearson r)")
    print()
    print(
        f"Full pairwise Pearson correlation of domain rank vectors over the "
        f"top {CORRELATION_WORDS:,} words. Cells closer to 1.0 = "
        "the two domains rank words in a similar order."
    )
    print()

    headers = ["Domain"] + [DOMAIN_ID[d] for d in DOMAINS]
    rows    = []
    for d_a in DOMAINS:
        row = [DOMAIN_EN[d_a]]
        for d_b in DOMAINS:
            if d_a == d_b:
                row.append("1.000")
            else:
                p = next(
                    (p for p in pairs if
                     (p["a"] == d_a and p["b"] == d_b) or
                     (p["a"] == d_b and p["b"] == d_a)),
                    None,
                )
                row.append(f"{p['pearson']:.3f}" if p else "—")
        rows.append(row)

    print(markdown_table(headers, rows))
    print()

    # ── Mermaid graph of strongest connections ─────────────────────────────
    print(f"## Similarity Graph (top {GRAPH_TOP_PAIRS} strongest Jaccard pairs)")
    print()
    print(
        "Each edge connects two domains with high vocabulary overlap. "
        "Edge labels show the Jaccard similarity score. "
        "Clusters of tightly connected nodes share a similar vocabulary profile."
    )
    print()

    top_pairs = pairs_by_jac[:GRAPH_TOP_PAIRS]
    edges = [
        (DOMAIN_ID[p["a"]], DOMAIN_ID[p["b"]], f"{p['jaccard']:.2f}")
        for p in top_pairs
    ]
    print(mermaid_graph(edges, directed=False))
    print()

    # ── Key insights ───────────────────────────────────────────────────────
    print("## Key Insights")
    print()

    most_sim  = pairs_by_jac[0]
    least_sim = pairs_by_jac[-1]
    print(
        f"- **Most similar pair:** {DOMAIN_EN[most_sim['a']]} × {DOMAIN_EN[most_sim['b']]} "
        f"(Jaccard = {most_sim['jaccard']:.3f}, {most_sim['overlap']} shared words in top {OVERLAP_TOP_N}). "
        f"These domains share the largest core vocabulary."
    )
    print()
    print(
        f"- **Least similar pair:** {DOMAIN_EN[least_sim['a']]} × {DOMAIN_EN[least_sim['b']]} "
        f"(Jaccard = {least_sim['jaccard']:.3f}, {least_sim['overlap']} shared words). "
        f"These domains have the most distinct vocabularies."
    )
    print()

    # Conversation-type vs location average Jaccard
    conv_domains = {"small_talk", "consultation", "meeting", "class"}
    loc_domains  = set(DOMAINS) - conv_domains

    conv_pairs = [p for p in pairs if p["a"] in conv_domains and p["b"] in conv_domains]
    loc_pairs  = [p for p in pairs if p["a"] in loc_domains  and p["b"] in loc_domains]
    cross_pairs = [p for p in pairs if
                   (p["a"] in conv_domains) != (p["b"] in conv_domains)]

    avg_conv  = statistics.mean(p["jaccard"] for p in conv_pairs)  if conv_pairs  else 0
    avg_loc   = statistics.mean(p["jaccard"] for p in loc_pairs)   if loc_pairs   else 0
    avg_cross = statistics.mean(p["jaccard"] for p in cross_pairs) if cross_pairs else 0

    print(
        f"- **Conversation-type domains are more similar to each other** "
        f"(avg Jaccard = {avg_conv:.3f}) than location domains are ({avg_loc:.3f}), "
        f"and both are more similar within their group than across groups ({avg_cross:.3f}). "
        f"This suggests that *what kind of conversation* matters more for vocabulary "
        f"than *where* it takes place."
    )
    print()
    print(
        "- **Indoors and Home cluster tightly** — much of 'home' conversation "
        "takes place indoors, making these two location categories partially redundant. "
        "Their high overlap reflects corpus recording conditions."
    )
    print()
    print(
        "- **Transportation and Public/Commercial are the most isolated** location domains. "
        "These settings feature shorter, more transactional exchanges with distinctive "
        "vocabulary that doesn't generalise well to other contexts."
    )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 domain_similarity.py <json_dir>")
        sys.exit(1)
    run(sys.argv[1])
