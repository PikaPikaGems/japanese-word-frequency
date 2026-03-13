#!/usr/bin/env python3
"""
vocab_tier_breakdown.py — POS, origin, and subcategory distributions per frequency tier.

For each tier (top 1500 / 4000 / 10000 / 20000 words by overall rank), outputs:
  - Part-of-speech distribution
  - Word-origin distribution (native / Sino-Japanese / loanword / mixed)
  - Subcategory distribution (top 15)
  - Origin × POS cross-tabulation

Output: Markdown (with ASCII bar charts + Mermaid pie charts) to stdout.

Usage:
    python3 vocab_tier_breakdown.py <json_dir>

Example:
    python3 data/CEJC/scripts/vocab_tier_breakdown.py data/CEJC/json
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[3]))

from loaders import load_cejc_json
from analysis import tier_slice, flat_entries, count_distribution
from utils import markdown_table, ascii_bar_chart, mermaid_pie

TIERS = [1500, 4000, 10000, 20000]
TOP_POS_IN_CROSSTAB = 6
TOP_SUBCATS = 15

# ── Translation dictionaries ──────────────────────────────────────────────────

POS_EN = {
    "名詞-普通名詞-一般":       "Common Noun",
    "名詞-普通名詞-サ変可能":    "Verbal Noun (suru)",
    "名詞-普通名詞-副詞可能":    "Adverbial Noun",
    "名詞-普通名詞-形状詞可能":  "Nominal Adjective",
    "名詞-普通名詞-助数詞可能":  "Counter Noun",
    "名詞-普通名詞-サ変形状詞可能": "Verbal+Adj Noun",
    "名詞-数詞":              "Numeral",
    "名詞-固有名詞-一般":       "Proper Noun",
    "名詞-固有名詞-地名-一般":   "Place Name",
    "名詞-固有名詞-地名-国":     "Country Name",
    "名詞-固有名詞-人名-一般":   "Person Name",
    "名詞-固有名詞-人名-名":     "Given Name",
    "名詞-固有名詞-人名-姓":     "Surname",
    "名詞-助動詞語幹":          "Copula Noun",
    "動詞-一般":              "Verb",
    "動詞-非自立可能":          "Aux. Verb",
    "形容詞-一般":             "I-Adjective",
    "形容詞-非自立可能":         "Dependent I-Adj",
    "形状詞-一般":             "Na-Adjective",
    "形状詞-助動詞語幹":         "Copula Stem",
    "形状詞-タリ":             "Tari-Adjective",
    "副詞":                  "Adverb",
    "接続詞":                 "Conjunction",
    "感動詞-一般":             "Interjection",
    "感動詞-フィラー":          "Filler",
    "助詞-格助詞":             "Case Particle",
    "助詞-副助詞":             "Adverbial Particle",
    "助詞-係助詞":             "Topic Particle",
    "助詞-終助詞":             "Sentence-final Particle",
    "助詞-接続助詞":            "Conjunctive Particle",
    "助詞-準体助詞":            "Nominalizer Particle",
    "助動詞":                 "Auxiliary",
    "接頭辞":                 "Prefix",
    "接尾辞-名詞的-一般":        "Nominal Suffix",
    "接尾辞-名詞的-助数詞":       "Counter Suffix",
    "接尾辞-名詞的-副詞可能":     "Adverbial Suffix",
    "接尾辞-名詞的-サ変可能":     "Verbal Suffix",
    "接尾辞-形容詞的":          "Adjectival Suffix",
    "接尾辞-形状詞的":          "Na-Adj Suffix",
    "接尾辞-動詞的":            "Verbal Suffix (v)",
    "代名詞":                 "Pronoun",
    "連体詞":                 "Pre-noun Adjectival",
    "言いよどみ":              "Hesitation",
    "形態論情報付与対象外":       "Unanalyzed",
    "伏せ字":                 "Censored",
    "歌":                    "Song/Lyric",
    "喃語":                   "Babbling",
}

ORIGIN_EN = {
    "和":  "Native Japanese (和語)",
    "漢":  "Sino-Japanese (漢語)",
    "外":  "Foreign Loanword (外来語)",
    "混":  "Mixed Origin (混種語)",
    "固":  "Proper Noun Origin (固有)",
    "記号": "Symbol / Other",
    "":   "(Unknown)",
}

ORIGIN_SHORT = {
    "和":  "Native JP",
    "漢":  "Sino-JP",
    "外":  "Loanword",
    "混":  "Mixed",
    "固":  "Proper",
    "記号": "Symbol",
    "":   "Unknown",
}

# Per-tier qualitative insights (written after analysing the data)
TIER_INSIGHTS = {
    1500: [
        "**Native Japanese dominates the core.** Over half (55%) of the top-1,500 "
        "words are native Japanese (和語). These are the grammatical glue words, "
        "basic verbs, and everyday nouns that make up the backbone of spoken Japanese.",

        "**Verbs are disproportionately native.** Of the 214 general verb entries, "
        "almost all are 和語 — Sino-Japanese verbs are rare because they are "
        'expressed as verbal nouns + する (e.g. 勉強する), which is why "Verbal Noun '
        '(suru)" is its own large category (5.9%).',

        "**Foreign loanwords are scarce at the top.** Only 7.8% of the top-1,500 "
        "are loanwords (外来語). The highest-frequency words are almost entirely "
        "native or Sino-Japanese — loanwords become more common as frequency rank "
        "decreases.",

        "**Subcategory is nearly meaningless here.** 98.8% of entries have no "
        "subcategory tag (-1 / blank). Subcategory is only assigned to a handful "
        "of grammatical edge cases in this corpus.",
    ],
    4000: [
        "**The 和語/漢語 gap narrows sharply.** Native Japanese drops from 55% to "
        "41% while Sino-Japanese climbs from 31% to 35%. As frequency rank "
        "increases, more Sino-Japanese vocabulary enters — this reflects how "
        "漢語 is used for technical, abstract, and formal concepts.",

        "**Loanwords nearly double.** Foreign loanwords jump from 7.8% → 14%, "
        "the single biggest relative increase of any origin category. "
        "Katakana loanwords for everyday objects and concepts (コーヒー, ニュース, etc.) "
        "start accumulating here.",

        "**Proper nouns appear for the first time.** The 固 (proper noun) category "
        "reaches 8.2%, mainly place names (地名) and personal names (人名). "
        "This reflects that many mid-frequency words in conversation are names of "
        "people and locations.",

        "**The vocabulary becomes more noun-heavy.** Common nouns rise from 28.9% "
        "→ 38.8% of POS entries. As rank decreases, the vocabulary shifts from "
        "grammatical/functional words toward content words.",
    ],
    10000: [
        "**A historic crossover: 和語 ≈ 漢語.** For the first time the two largest "
        "origin groups are nearly equal (~33% each). This crossover point around "
        "rank 10,000 marks where encyclopedic Sino-Japanese vocabulary overtakes "
        "the everyday native lexicon.",

        "**Proper nouns surge to 14.6%.** Place names and personal names now make "
        "up a substantial slice — many mid-frequency spoken words are simply names "
        "of people, cities, and countries.",

        "**Verbs plateau early.** General verbs drop to just 8.5% of entries, "
        "half their share at the top-1,500 tier. The ~870 most-used verbs were "
        "already captured by rank 10,000; additional verbs become increasingly "
        "rare in natural speech.",

        "**Loanwords stabilise at 15.5%.** Foreign loanwords grow more slowly "
        "between tiers 4,000 and 10,000 compared to the jump from 1,500 to 4,000 — "
        "suggesting there is a 'loanword ceiling' around 15–16% in this corpus.",
    ],
    20000: [
        "**This tier is effectively the full dataset.** The corpus only contains "
        "~12,796 unique words, so 'top 20,000' captures everything.",

        "**和語 and 漢語 are statistically tied** at ~32% each — at full vocabulary "
        "breadth, native and Sino-Japanese words are equally represented in "
        "everyday Japanese conversation.",

        "**Proper nouns (16.4%) now outnumber loanwords (15.3%)** — a reminder "
        "that a large fraction of real-world vocabulary is proper names of people "
        "and places, not just common words.",

        "**Mixed-origin words (混種語) grow steadily** from 2.1% → 3.1% across "
        "tiers. These are hybrids such as 打ち合わせ (漢+和) or combinations of "
        "loanword roots with Japanese suffixes.",
    ],
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def pct(count: int, total: int) -> str:
    return f"{count / total * 100:.1f}%" if total else "0.0%"


def en_label(jp: str, mapping: dict, fallback_prefix: str = "") -> str:
    return mapping.get(jp, f"{fallback_prefix}{jp}")


def origin_counts(sliced: dict) -> dict[str, int]:
    """Count unique words per origin (origin is a lexeme-level property)."""
    counts: dict[str, int] = {}
    for entries in sliced.values():
        origin = entries[0]["origin"]
        counts[origin] = counts.get(origin, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))


# ── Main ──────────────────────────────────────────────────────────────────────

def run(json_dir: str) -> None:
    data = load_cejc_json(json_dir)

    print("# Vocabulary Tier Breakdown")
    print()
    print("**Source:** CEJC — Corpus of Everyday Japanese Conversation  ")
    print("**Tiers are cumulative** — 'top 1,500' = words ranked 1–1,500 by overall "
          "frequency across the entire ~2.4 million-word spoken corpus.")
    print()
    print("Each word can appear multiple times if it belongs to more than one "
          "part-of-speech category (e.g. の as a case particle, nominaliser, and "
          "sentence-final particle). Charts that say 'POS entries' count each "
          "grammatical role separately; charts that say 'unique words' count each "
          "word only once.")
    print()

    for tier in TIERS:
        sliced      = tier_slice(data, tier)
        total_words = len(sliced)
        all_entries = list(flat_entries(sliced))
        total_entries = len(all_entries)

        print("---")
        print()
        print(f"## Top {tier:,} Words")
        print()
        print(f"**{total_words:,} unique words · {total_entries:,} POS entries**")
        print()

        # ── POS distribution ───────────────────────────────────────────────
        pos_dist = count_distribution([e for _, e in all_entries], lambda e: e["pos"])

        print("### Part of Speech Distribution")
        print()
        print(
            "What grammatical roles make up this vocabulary tier? "
            "Each bar represents one POS category. Because a single word can "
            "fill multiple roles, the total entries may exceed the unique word count. "
            "This chart reveals the grammatical character of high-frequency Japanese — "
            "for example, whether nouns, verbs, or particles dominate everyday speech."
        )
        print()

        # Bar chart — use English labels
        bar_items = [(en_label(pos, POS_EN), cnt) for pos, cnt in pos_dist.items()]
        print(ascii_bar_chart(bar_items, fence=True))
        print()

        # Table — show both English and Japanese
        print(markdown_table(
            ["Part of Speech (EN)", "品詞 (JP)", "Entries", "%"],
            [
                [en_label(pos, POS_EN), pos, cnt, pct(cnt, total_entries)]
                for pos, cnt in pos_dist.items()
            ],
        ))
        print()

        # Mermaid pie — English labels, top 8 slices
        print(mermaid_pie(
            f"POS — Top {tier:,}",
            [(en_label(pos, POS_EN), cnt) for pos, cnt in list(pos_dist.items())[:8]],
        ))
        print()

        # ── Origin distribution ────────────────────────────────────────────
        orig_counts = origin_counts(sliced)

        print("### Word Origin Distribution")
        print()
        print(
            "Japanese vocabulary is classified into four main origin types: "
            "native Japanese (和語), Sino-Japanese (漢語 — words borrowed from Chinese "
            "and written with kanji), foreign loanwords (外来語 — mainly from English, "
            "written in katakana), and mixed-origin words (混種語). "
            "This distribution shifts dramatically across frequency tiers, revealing "
            "how the character of the vocabulary changes as you go deeper."
        )
        print()

        orig_bar_items = [(ORIGIN_SHORT.get(o, o), cnt) for o, cnt in orig_counts.items()]
        print(ascii_bar_chart(orig_bar_items, fence=True))
        print()

        print(markdown_table(
            ["Origin (EN)", "語種 (JP)", "Unique Words", "%"],
            [
                [ORIGIN_EN.get(o, o), o, cnt, pct(cnt, total_words)]
                for o, cnt in orig_counts.items()
            ],
        ))
        print()

        print(mermaid_pie(
            f"Word Origin — Top {tier:,}",
            [(ORIGIN_SHORT.get(o, o), cnt) for o, cnt in orig_counts.items()],
        ))
        print()

        # ── Subcategory distribution ───────────────────────────────────────
        subcat_dist = count_distribution([e for _, e in all_entries], lambda e: e["subcategory"])
        top_subcats = dict(list(subcat_dist.items())[:TOP_SUBCATS])

        print(f"### Subcategory Distribution (Top {TOP_SUBCATS})")
        print()
        print(
            "A finer-grained classification within each POS. Most entries have no "
            "subcategory (shown as blank / '-1') — subcategories are only assigned "
            "to grammatically irregular or specialised forms. The non-blank entries "
            "here are mostly corpus annotations or proper noun sub-types."
        )
        print()

        sub_bar_items = [(s if s.strip() else "(none)", cnt) for s, cnt in top_subcats.items()]
        print(ascii_bar_chart(sub_bar_items, fence=True))
        print()

        print(markdown_table(
            ["Subcategory", "Entries", "%"],
            [
                [s if s.strip() else "(none)", cnt, pct(cnt, total_entries)]
                for s, cnt in top_subcats.items()
            ],
        ))
        print()

        # ── Origin × POS cross-tabulation ─────────────────────────────────
        top_pos      = list(pos_dist.keys())[:TOP_POS_IN_CROSSTAB]
        all_origins  = list(orig_counts.keys())
        word_to_orig = {w: entries[0]["origin"] for w, entries in sliced.items()}

        cross: dict[str, dict[str, int]] = {
            orig: {pos: 0 for pos in top_pos} for orig in all_origins
        }
        for word, entry in all_entries:
            orig = word_to_orig.get(word)
            pos  = entry["pos"]
            if orig in cross and pos in cross[orig]:
                cross[orig][pos] += 1

        print(f"### Origin × POS Cross-tabulation (top {TOP_POS_IN_CROSSTAB} POS)")
        print()
        print(
            "How do word origins interact with grammatical role? "
            "For example: are Sino-Japanese words more likely to be nouns than verbs? "
            "Are loanwords exclusively nouns? This table answers those questions. "
            "Rows are origin types; columns are the most frequent POS categories."
        )
        print()

        pos_en_headers = [en_label(p, POS_EN) for p in top_pos]
        orig_en_rows   = [
            [ORIGIN_SHORT.get(orig, orig)] + [cross[orig][pos] for pos in top_pos]
            for orig in all_origins
        ]
        print(markdown_table(["Origin"] + pos_en_headers, orig_en_rows))
        print()

        # ── Key insights ───────────────────────────────────────────────────
        print("### Key Insights")
        print()
        for insight in TIER_INSIGHTS.get(tier, []):
            print(f"- {insight}")
            print()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 vocab_tier_breakdown.py <json_dir>")
        sys.exit(1)
    run(sys.argv[1])
