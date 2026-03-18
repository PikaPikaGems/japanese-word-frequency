"""
Compare WIKIPEDIA_V2 vs ADNO using BCCWJ_LUW as the primary reference
and RSPEER as a secondary reference.

Metrics:
  1. Spearman rank correlation of each against BCCWJ_LUW_rank and RSPEER
  2. Spearman rank correlation between WIKIPEDIA_V2 and ADNO directly
  3. Top-N Jaccard overlap at multiple thresholds
  4. Discrepancy words: in one dataset's top 500 but absent from the other

Anchor used: BCCWJ_LUW_anchor/consolidated.csv
Primary reference column: BCCWJ_LUW_rank

Run from repo root:
  python data/ALL/___experiments4/analyze_wikipedia.py
"""

import csv
import os

csv.field_size_limit(10_000_000)

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ALL_DIR = os.path.join(REPO_ROOT, "data", "ALL")
ANCHOR_CSV = os.path.join(ALL_DIR, "BCCWJ_LUW_anchor", "consolidated.csv")
OUT_MD = os.path.join(os.path.dirname(__file__), "WIKIPEDIA_ANALYSIS.md")

REF_PRIMARY = "BCCWJ_LUW_rank"
REF_SECONDARY = "RSPEER"
COL_A = "WIKIPEDIA_V2"
COL_B = "ADNO"


# ── Stats helpers ──────────────────────────────────────────────────────────────

def assign_ranks(values):
    n = len(values)
    order = sorted(range(n), key=lambda i: values[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        j = i
        while j + 1 < n and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def spearman(pairs):
    n = len(pairs)
    if n < 2:
        return float("nan")
    xs = [p[0] for p in pairs]
    ys = [p[1] for p in pairs]
    rx = assign_ranks(xs)
    ry = assign_ranks(ys)
    mx = sum(rx) / n
    my = sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    denom = (sum((r - mx) ** 2 for r in rx) * sum((r - my) ** 2 for r in ry)) ** 0.5
    return num / denom if denom > 0 else float("nan")


def top_n_words(rows, col, n):
    return {row["word"] for row in rows if int(row[col]) != -1 and int(row[col]) <= n}


def jaccard(a, b):
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


# ── Load ───────────────────────────────────────────────────────────────────────

rows = []
with open(ANCHOR_CSV, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        rows.append(row)

print(f"Loaded {len(rows):,} rows from BCCWJ_LUW_anchor/consolidated.csv")

# ── 1. Spearman correlation ────────────────────────────────────────────────────

def collect_pairs(col_x, col_y):
    return [
        (int(row[col_x]), int(row[col_y]))
        for row in rows
        if int(row[col_x]) != -1 and int(row[col_y]) != -1
    ]

pairs_a_primary   = collect_pairs(COL_A, REF_PRIMARY)
pairs_b_primary   = collect_pairs(COL_B, REF_PRIMARY)
pairs_a_secondary = collect_pairs(COL_A, REF_SECONDARY)
pairs_b_secondary = collect_pairs(COL_B, REF_SECONDARY)
pairs_ab          = collect_pairs(COL_A, COL_B)

rho_a_primary   = spearman(pairs_a_primary)
rho_b_primary   = spearman(pairs_b_primary)
rho_a_secondary = spearman(pairs_a_secondary)
rho_b_secondary = spearman(pairs_b_secondary)
rho_ab          = spearman(pairs_ab)

print(f"\nSpearman vs BCCWJ_LUW:")
print(f"  WIKIPEDIA_V2  n={len(pairs_a_primary):,}  rho={rho_a_primary:.4f}")
print(f"  ADNO          n={len(pairs_b_primary):,}  rho={rho_b_primary:.4f}")
print(f"\nSpearman vs RSPEER:")
print(f"  WIKIPEDIA_V2  n={len(pairs_a_secondary):,}  rho={rho_a_secondary:.4f}")
print(f"  ADNO          n={len(pairs_b_secondary):,}  rho={rho_b_secondary:.4f}")
print(f"\nSpearman WIKIPEDIA_V2 vs ADNO (shared n={len(pairs_ab):,}): rho={rho_ab:.4f}")

# ── 2. Top-N Jaccard ──────────────────────────────────────────────────────────

thresholds = [100, 500, 1000, 5000]
jaccard_rows = []
for n in thresholds:
    ref_set = top_n_words(rows, REF_PRIMARY, n)
    a_set   = top_n_words(rows, COL_A, n)
    b_set   = top_n_words(rows, COL_B, n)
    jaccard_rows.append((n, jaccard(a_set, ref_set), jaccard(b_set, ref_set), jaccard(a_set, b_set)))

print("\nTop-N Jaccard overlap:")
print(f"  {'N':>6}  {'WIKI∩BCCWJ':>11}  {'ADNO∩BCCWJ':>11}  {'WIKI∩ADNO':>10}")
for n, j_a, j_b, j_ab in jaccard_rows:
    print(f"  {n:>6,}  {j_a:>11.3f}  {j_b:>11.3f}  {j_ab:>10.3f}")

# ── 3. Discrepancy analysis ────────────────────────────────────────────────────
# Words in WIKIPEDIA_V2 top 500 absent from ADNO, and vice versa

disc_a = sorted(
    (int(row[COL_A]), row["word"], row["hiragana"])
    for row in rows
    if int(row[COL_A]) != -1 and int(row[COL_A]) <= 500 and int(row[COL_B]) == -1
)
disc_b = sorted(
    (int(row[COL_B]), row["word"], row["hiragana"])
    for row in rows
    if int(row[COL_B]) != -1 and int(row[COL_B]) <= 500 and int(row[COL_A]) == -1
)

print(f"\nIn WIKIPEDIA_V2 top 500, absent from ADNO: {len(disc_a)}")
for rank, word, reading in disc_a:
    print(f"  #{rank:>3}  {word}  ({reading})")

print(f"\nIn ADNO top 500, absent from WIKIPEDIA_V2: {len(disc_b)}")
for rank, word, reading in disc_b:
    print(f"  #{rank:>3}  {word}  ({reading})")

# ── Write markdown ─────────────────────────────────────────────────────────────

md = [
    "# Wikipedia Dataset Comparison: WIKIPEDIA_V2 vs ADNO",
    "",
    "**Primary reference:** `BCCWJ_LUW_rank` (anchor, BCCWJ_LUW_anchor/consolidated.csv)  ",
    "**Secondary reference:** `RSPEER`  ",
    f"**Rows loaded:** {len(rows):,}",
    "",
    "---",
    "",
    "## 1. Spearman Rank Correlation",
    "",
    "| Dataset | n vs BCCWJ_LUW | ρ vs BCCWJ_LUW | n vs RSPEER | ρ vs RSPEER |",
    "|---|---|---|---|---|",
    f"| `WIKIPEDIA_V2` | {len(pairs_a_primary):,} | {rho_a_primary:.4f} | {len(pairs_a_secondary):,} | {rho_a_secondary:.4f} |",
    f"| `ADNO` | {len(pairs_b_primary):,} | {rho_b_primary:.4f} | {len(pairs_b_secondary):,} | {rho_b_secondary:.4f} |",
    "",
    f"Spearman ρ between WIKIPEDIA_V2 and ADNO (shared {len(pairs_ab):,} words): **{rho_ab:.4f}**",
    "",
    "---",
    "",
    "## 2. Top-N Jaccard Overlap",
    "",
    "| Top-N | WIKIPEDIA_V2 ∩ BCCWJ_LUW | ADNO ∩ BCCWJ_LUW | WIKIPEDIA_V2 ∩ ADNO |",
    "|---|---|---|---|",
]
for n, j_a, j_b, j_ab in jaccard_rows:
    md.append(f"| {n:,} | {j_a:.3f} | {j_b:.3f} | {j_ab:.3f} |")

md += [
    "",
    "---",
    "",
    "## 3. Top-500 Discrepancies",
    "",
    f"### In WIKIPEDIA_V2 top 500, absent from ADNO ({len(disc_a)} words)",
    "",
    "| WIKIPEDIA_V2 rank | Word | Reading |",
    "|---|---|---|",
]
for rank, word, reading in disc_a:
    md.append(f"| {rank} | {word} | {reading} |")

md += [
    "",
    f"### In ADNO top 500, absent from WIKIPEDIA_V2 ({len(disc_b)} words)",
    "",
    "| ADNO rank | Word | Reading |",
    "|---|---|---|",
]
for rank, word, reading in disc_b:
    md.append(f"| {rank} | {word} | {reading} |")

with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(md) + "\n")

print(f"\nWrote {OUT_MD}")
