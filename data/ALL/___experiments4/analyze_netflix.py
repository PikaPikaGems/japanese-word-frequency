"""
Compare NETFLIX vs DD2_MORPHMAN_NETFLIX using ANIME_JDRAMA as the reference.

Metrics:
  1. Spearman rank correlation of each against ANIME_JDRAMA_rank
  2. Spearman rank correlation between NETFLIX and DD2_MORPHMAN_NETFLIX directly
  3. Top-N Jaccard overlap at multiple thresholds
  4. Words in NETFLIX top 300 that DD2_MORPHMAN_NETFLIX filtered out (absent or rank > 2000)
     — these are the proper names / noise entries removed by DD2's name filter

Anchor used: ANIME_JDRAMA_anchor/consolidated.csv
Reference column: ANIME_JDRAMA_rank

Run from repo root:
  python data/ALL/___experiments4/analyze_netflix.py
"""

import csv
import os

csv.field_size_limit(10_000_000)

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ALL_DIR = os.path.join(REPO_ROOT, "data", "ALL")
ANCHOR_CSV = os.path.join(ALL_DIR, "ANIME_JDRAMA_anchor", "consolidated.csv")
OUT_MD = os.path.join(os.path.dirname(__file__), "NETFLIX_ANALYSIS.md")

REF = "ANIME_JDRAMA_rank"
COL_A = "NETFLIX"
COL_B = "DD2_MORPHMAN_NETFLIX"


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

print(f"Loaded {len(rows):,} rows from ANIME_JDRAMA_anchor/consolidated.csv")

# ── 1. Spearman correlation ────────────────────────────────────────────────────

pairs_a, pairs_b, pairs_ab = [], [], []
for row in rows:
    ref = int(row[REF])
    a = int(row[COL_A])
    b = int(row[COL_B])
    if ref != -1 and a != -1:
        pairs_a.append((a, ref))
    if ref != -1 and b != -1:
        pairs_b.append((b, ref))
    if ref != -1 and a != -1 and b != -1:
        pairs_ab.append((a, b))

rho_a = spearman(pairs_a)
rho_b = spearman(pairs_b)
rho_ab = spearman(pairs_ab)

print(f"\nSpearman vs ANIME_JDRAMA:")
print(f"  NETFLIX               n={len(pairs_a):,}  rho={rho_a:.4f}")
print(f"  DD2_MORPHMAN_NETFLIX  n={len(pairs_b):,}  rho={rho_b:.4f}")
print(f"\nSpearman NETFLIX vs DD2_MORPHMAN_NETFLIX (shared n={len(pairs_ab):,}): rho={rho_ab:.4f}")

# ── 2. Top-N Jaccard ──────────────────────────────────────────────────────────

thresholds = [100, 500, 1000, 5000]
jaccard_rows = []
for n in thresholds:
    ref_set = top_n_words(rows, REF, n)
    a_set = top_n_words(rows, COL_A, n)
    b_set = top_n_words(rows, COL_B, n)
    jaccard_rows.append((n, jaccard(a_set, ref_set), jaccard(b_set, ref_set), jaccard(a_set, b_set)))

print("\nTop-N Jaccard overlap:")
print(f"  {'N':>6}  {'NET∩ANIME':>10}  {'DD2∩ANIME':>10}  {'NET∩DD2':>10}")
for n, j_a, j_b, j_ab in jaccard_rows:
    print(f"  {n:>6,}  {j_a:>10.3f}  {j_b:>10.3f}  {j_ab:>10.3f}")

# ── 3. Proper-name filter analysis ────────────────────────────────────────────
# Words Netflix ranks in top 300 that DD2 either removed (−1) or ranked far lower (>2000)

filtered_out = []
for row in rows:
    a = int(row[COL_A])
    b = int(row[COL_B])
    if a != -1 and a <= 300 and (b == -1 or b > 2000):
        filtered_out.append((a, row["word"], row["hiragana"], b))

filtered_out.sort()

print(f"\nNETFLIX top 300 words absent or poorly ranked (>2000) in DD2_MORPHMAN_NETFLIX:")
print(f"  Total: {len(filtered_out)}")
for rank, word, reading, dd2 in filtered_out:
    dd2_str = f"{dd2:,}" if dd2 != -1 else "absent"
    print(f"  #{rank:>3}  {word}  ({reading})  → DD2: {dd2_str}")

# ── Write markdown ─────────────────────────────────────────────────────────────

md = [
    "# Netflix Dataset Comparison: NETFLIX vs DD2_MORPHMAN_NETFLIX",
    "",
    "**Reference:** `ANIME_JDRAMA_rank` (anchor, ANIME_JDRAMA_anchor/consolidated.csv)  ",
    f"**Rows loaded:** {len(rows):,}",
    "",
    "---",
    "",
    "## 1. Spearman Rank Correlation vs ANIME_JDRAMA",
    "",
    "| Dataset | Valid pairs with ANIME_JDRAMA | Spearman ρ |",
    "|---|---|---|",
    f"| `NETFLIX` | {len(pairs_a):,} | {rho_a:.4f} |",
    f"| `DD2_MORPHMAN_NETFLIX` | {len(pairs_b):,} | {rho_b:.4f} |",
    "",
    f"Spearman ρ between NETFLIX and DD2_MORPHMAN_NETFLIX (shared {len(pairs_ab):,} words): **{rho_ab:.4f}**",
    "",
    "---",
    "",
    "## 2. Top-N Jaccard Overlap",
    "",
    "| Top-N | NETFLIX ∩ ANIME_JDRAMA | DD2 ∩ ANIME_JDRAMA | NETFLIX ∩ DD2 |",
    "|---|---|---|---|",
]
for n, j_a, j_b, j_ab in jaccard_rows:
    md.append(f"| {n:,} | {j_a:.3f} | {j_b:.3f} | {j_ab:.3f} |")

md += [
    "",
    "---",
    "",
    "## 3. Words Netflix Ranks in Top 300 That DD2 Filtered Out",
    "",
    "These are words NETFLIX ranks in its top 300 but DD2_MORPHMAN_NETFLIX either",
    "removed entirely (absent) or ranked far lower (>2000). DD2 excludes proper names",
    "using a UniDic name filter — words appearing here are likely character/person names",
    "or other noise entries.",
    "",
    f"**Total:** {len(filtered_out)} words",
    "",
    "| NETFLIX rank | Word | Reading | DD2 rank |",
    "|---|---|---|---|",
]
for rank, word, reading, dd2 in filtered_out:
    dd2_str = f"{dd2:,}" if dd2 != -1 else "absent"
    md.append(f"| {rank} | {word} | {reading} | {dd2_str} |")

with open(OUT_MD, "w", encoding="utf-8") as f:
    f.write("\n".join(md) + "\n")

print(f"\nWrote {OUT_MD}")
