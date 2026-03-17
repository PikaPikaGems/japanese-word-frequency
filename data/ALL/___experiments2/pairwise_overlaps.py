"""
Pairwise reading-aware overlap between selected source datasets, grouped by theme.

For each pair (A, B) at top-N, counts the fraction of A's top-N words that
appear in B's top-N using reading-aware matching:
  A word matches if its surface form OR its hiragana reading equals
  B's surface form or hiragana reading.

Sources are loaded from data/RAW/___FILTERED/*/DATA.csv (WORD, FREQUENCY_RANKING).
Hiragana readings are sourced from consolidated anchor CSVs.

Run from repo root:
  python data/ALL/___experiments2/pairwise_overlaps.py
"""

import csv
import os

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
RAW_DIR = os.path.join(REPO_ROOT, "data", "RAW", "___FILTERED")
ALL_DIR = os.path.join(REPO_ROOT, "data", "ALL")
OUT_MD = os.path.join(os.path.dirname(__file__), "PAIRWISE_OVERLAPS.md")

NS = [2000, 5000, 10000]

TABLES = [
    {
        "title": "Table 1 — Japanese Web",
        "sources": ["MALTESAA_NWJC", "CC100"],
    },
    {
        "title": "Table 2 — Wikipedia",
        "sources": ["ADNO", "ILYASEMENOV", "WIKIPEDIA_V2"],
    },
    {
        "title": "Table 4 — YouTube",
        "sources": ["YOUTUBE_FREQ", "YOUTUBE_FREQ_V3"],
    },
    {
        "title": "Table 5 — Netflix and Dramas",
        "sources": [
            "ANIME_JDRAMA",
            "NETFLIX",
            "DAVE_DOEBRICK",
            "DD2_MIGAKU_NETFLIX",
            "DD2_MORPHMAN_NETFLIX",
            "CHRISKEMPSON",
            "JITEN_DRAMA",
        ],
    },
    {
        "title": "Table 6 — Slice of Life",
        "sources": ["DD2_MORPHMAN_SOL", "DD2_YOMICHAN_SOL"],
    },
    {
        "title": "Table 7 — Anime",
        "sources": [
            "JLAB",
            "DD2_YOMICHAN_SHONEN",
            "DD2_YOMICHAN_SHONEN_STARS",
            "JITEN_ANIME",
            "JITEN_ANIME_V2",
        ],
    },
]

ANCHOR_DIRS = [
    d for d in os.listdir(ALL_DIR)
    if d.endswith("_anchor") and os.path.isfile(os.path.join(ALL_DIR, d, "consolidated.csv"))
]


def build_global_hiragana_lookup():
    """Scan all consolidated anchor CSVs to build word -> hiragana mapping."""
    lookup = {}
    for anchor_dir in ANCHOR_DIRS:
        path = os.path.join(ALL_DIR, anchor_dir, "consolidated.csv")
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                w = row.get("word", "")
                h = row.get("hiragana", "")
                if w and w not in lookup and h and h != "-":
                    lookup[w] = h
    return lookup


def load_source(name, hira_lookup):
    """Load DATA.csv for a source, returning list of (word, hiragana) sorted by rank."""
    path = os.path.join(RAW_DIR, name, "DATA.csv")
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            w = row.get("WORD", "").strip()
            try:
                rank = int(row["FREQUENCY_RANKING"])
            except (ValueError, KeyError):
                continue
            if rank < 1 or not w:
                continue
            h = hira_lookup.get(w, "-")
            rows.append((rank, w, h))
    rows.sort(key=lambda x: x[0])
    return [(w, h) for _, w, h in rows]


def build_lookup(word_hira_list, n):
    s = set()
    for w, h in word_hira_list[:n]:
        s.add(w)
        if h and h != "-":
            s.add(h)
    return s


def overlap_pct(a_list, b_lookup, n):
    top_a = a_list[:n]
    actual_n = len(top_a)
    if actual_n == 0:
        return 0.0
    count = sum(
        1 for w, h in top_a
        if w in b_lookup or (h and h != "-" and h in b_lookup)
    )
    return count / actual_n * 100


def fmt_pct(v):
    return f"{v:.1f}%"


def make_md_table(sources, data, n):
    """Return markdown table string for a given N."""
    col_names = sources
    header = "| " + " " * 28 + " | " + " | ".join(f"{s:<28}" for s in col_names) + " |"
    sep = "| " + "-" * 28 + " | " + " | ".join("-" * 28 for _ in col_names) + " |"
    lines = [header, sep]
    lookups = {s: build_lookup(data[s], n) for s in sources}
    for a in sources:
        cells = []
        for b in sources:
            if a == b:
                cells.append(f"{'—':<28}")
            else:
                pct = overlap_pct(data[a], lookups[b], n)
                cells.append(f"{fmt_pct(pct):<28}")
        lines.append("| " + f"**{a}**".ljust(28) + " | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def print_table(sources, data, n):
    col_w = 28
    num_w = 8
    header = f"{'':>{col_w}}" + "".join(f"{s:>{num_w}}" for s in sources)
    sep = "-" * len(header)
    lookups = {s: build_lookup(data[s], n) for s in sources}
    print(f"  Top {n:,}")
    print(header)
    print(sep)
    for a in sources:
        row = f"{a:>{col_w}}"
        for b in sources:
            if a == b:
                row += f"{'—':>{num_w}}"
            else:
                pct = overlap_pct(data[a], lookups[b], n)
                row += f"{pct:>{num_w - 1}.1f}%"
        print(row)
    print()


# ── Main ──────────────────────────────────────────────────────────────────────

print("Building global hiragana lookup from anchor CSVs...")
hira_lookup = build_global_hiragana_lookup()
print(f"  {len(hira_lookup):,} word→hiragana mappings loaded")
print()

# Collect all unique source names
all_sources = set()
for table in TABLES:
    all_sources.update(table["sources"])

print("Loading source DATA.csv files...")
source_data = {}
for name in sorted(all_sources):
    path = os.path.join(RAW_DIR, name, "DATA.csv")
    if not os.path.isfile(path):
        print(f"  WARNING: {name} not found at {path}")
        source_data[name] = []
    else:
        source_data[name] = load_source(name, hira_lookup)
        print(f"  {name}: {len(source_data[name])} words")
print()

# ── Console output + MD collection ────────────────────────────────────────────
md_sections = [
    "# Pairwise Overlap — Cross-Dataset Agreement",
    "",
    "Reading-aware pairwise intersection between source datasets.",
    "Row = source A (denominator); cell = % of A's top-N that appear in B's top-N.",
    "",
    "> **Reading-aware match**: a word in A counts as matching B if its surface form",
    "> or hiragana reading equals B's surface form or reading.",
    "",
]

for table in TABLES:
    title = table["title"]
    sources = table["sources"]
    # filter out any missing
    sources = [s for s in sources if source_data.get(s)]

    print(f"=== {title} ===")
    md_sections.append(f"## {title}")
    md_sections.append("")

    for n in NS:
        print_table(sources, source_data, n)
        md_sections.append(f"### Top {n:,}")
        md_sections.append("")
        md_sections.append(make_md_table(sources, source_data, n))
        md_sections.append("")

md_content = "\n".join(md_sections)
with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write(md_content)

print(f"Wrote {OUT_MD}")
