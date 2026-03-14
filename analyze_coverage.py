"""
Runs coverage analysis on every consolidated_anchor_*.csv in data/ALL/.
For each anchor, produces:
  - coverage_analysis_anchor_{NAME}.md  (per-source missing %, distribution bar chart)
"""

import csv
import glob
import os

csv.field_size_limit(10_000_000)

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "data", "ALL")
BAR_WIDTH = 40
EXCLUDE = {
    "AOZORA_BUNKO",       # kanji-only source — structurally no hiragana words
    "NIER",               # single game, only ~10k words total
    "ILYASEMENOV",        # Wikipedia dump with HTML entities, wrong domain
    "DD2_MIGAKU_NOVELS",  # curated learner deck, only ~16k words
    "HERMITDAVE_2016",    # MeCab morpheme-split — dictionary-form verbs don't exist as tokens
    "HERMITDAVE_2018",    # same source/tokenization as HERMITDAVE_2016
    "JPDB",               # anime/game corpus — misses general vocabulary (男性, 企業, 監督 all beyond rank 25k)
}
RANK_BANDS = [500, 1000, 3000, 5000, 10000, 25000]  # for rank-band zero-missing breakdown


def bar(val: int, total: int) -> str:
    filled = round(BAR_WIDTH * val / total) if total else 0
    return "[" + "#" * filled + "-" * (BAR_WIDTH - filled) + "]"


for consol_path in sorted(glob.glob(os.path.join(DATA_DIR, "consolidated_anchor_*.csv"))):
    anchor_name = os.path.basename(consol_path).removeprefix("consolidated_anchor_").removesuffix(".csv")
    categ_path = os.path.join(DATA_DIR, f"categorized_anchor_{anchor_name}.csv")
    report_path = os.path.join(DATA_DIR, f"coverage_analysis_anchor_{anchor_name}.md")
    zero_path = os.path.join(DATA_DIR, f"zero_missing_anchor_{anchor_name}.csv")
    neg_path = os.path.join(DATA_DIR, f"has_negative_rank_anchor_{anchor_name}.csv")
    rare_path = os.path.join(DATA_DIR, f"has_rare_category_anchor_{anchor_name}.csv")

    if not os.path.exists(categ_path):
        print(f"Skipping {anchor_name} — no matching categorized file")
        continue

    # ── Load consolidated ────────────────────────────────────────────────────
    with open(consol_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        # Source columns: everything except "word" and the anchor rank column
        anchor_col = f"{anchor_name}_rank"
        source_cols = [c for c in header if c != "word" and c != anchor_col]
        check_cols = [c for c in source_cols if c not in EXCLUDE]
        rows = list(reader)

    total = len(rows)

    # ── zero_missing ─────────────────────────────────────────────────────────
    zero_rows = [r for r in rows if all(r[c] != "-1" for c in check_cols)]
    with open(zero_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(zero_rows)

    # ── has_negative_rank ────────────────────────────────────────────────────
    neg_rows = [r for r in rows if any(r[c] == "-1" for c in check_cols)]
    with open(neg_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(neg_rows)

    # ── has_rare_category (from categorized file) ────────────────────────────
    with open(categ_path, newline="", encoding="utf-8") as f:
        cat_reader = csv.DictReader(f)
        cat_header = cat_reader.fieldnames
        cat_check = [c for c in cat_header if c != "word" and c != anchor_col and c not in EXCLUDE]
        rare_rows = [r for r in cat_reader if any(r[c] == "1" for c in cat_check)]
    with open(rare_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cat_header)
        writer.writeheader()
        writer.writerows(rare_rows)

    # ── Per-source missing rate ───────────────────────────────────────────────
    source_missing = {
        col: sum(1 for r in rows if r[col] == "-1")
        for col in source_cols
    }

    # ── Distribution of missing-source count per word ────────────────────────
    def count_missing(row):
        return sum(1 for c in check_cols if row[c] == "-1")

    missing_counts = [count_missing(r) for r in rows]
    max_m = max(missing_counts) if missing_counts else 0
    dist = [0] * (max_m + 1)
    for c in missing_counts:
        dist[c] += 1

    # ── Rank-band zero-missing breakdown ─────────────────────────────────────
    # rows are sorted by anchor rank already (rank 1 first)
    band_stats = []
    for band in RANK_BANDS:
        band_rows = rows[:band]
        if not band_rows:
            continue
        n = len(band_rows)
        z = sum(1 for r in band_rows if all(r[c] != "-1" for c in check_cols))
        band_stats.append((band, n, z))

    # ── Write report ──────────────────────────────────────────────────────────
    excl_note = ", ".join(sorted(EXCLUDE))
    lines = [
        f"# Coverage Analysis — Anchor: {anchor_name}",
        f"\nTotal words: {total}  |  Source columns: {len(source_cols)}",
        f"Excluded from quality checks: {excl_note}  ({len(check_cols)} remaining)\n",
        "## Per-Source Missing Rate\n",
        f"{'Source':<35} {'Missing':>7}  {'%':>6}  Bar",
        "-" * 80,
    ]
    for col, miss in sorted(source_missing.items(), key=lambda x: -x[1]):
        pct = 100 * miss / total
        note = " [EXCLUDED]" if col in EXCLUDE else ""
        lines.append(f"{col:<35} {miss:>7}  {pct:>5.1f}%  {bar(miss, total)}{note}")

    lines += [
        f"\n## Zero-Missing by Rank Band",
        f"(How many of the top-N words by {anchor_name} rank have zero -1s across all {len(check_cols)} checked sources)\n",
        f"{'Top-N':>8}  {'Total':>7}  {'Zero-missing':>14}  {'%':>6}",
        "-" * 50,
    ]
    for band, n, z in band_stats:
        pct = 100 * z / n
        lines.append(f"{band:>8}  {n:>7}  {z:>14}  {pct:>5.1f}%")

    lines += [
        f"\n## Distribution: How Many Sources Each Word Is Missing From",
        f"({len(check_cols)} columns checked, excluded: {excl_note})\n",
        f"{'Missing':>8}  {'Words':>7}  {'%':>6}  Bar",
        "-" * 70,
    ]
    for i, count in enumerate(dist):
        pct = 100 * count / total
        lines.append(f"{i:>8}  {count:>7}  {pct:>5.1f}%  {bar(count, total)}")

    lines.append(f"\nWords with zero -1s: {dist[0]}  ({100*dist[0]/total:.1f}%)")
    lines.append(f"Words with at least one -1: {total - dist[0]}  ({100*(total-dist[0])/total:.1f}%)")
    lines.append(f"Words with at least one RARE category: {len(rare_rows)}  ({100*len(rare_rows)/total:.1f}%)")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[{anchor_name}] {total} words | zero-missing: {dist[0]} | report -> {os.path.basename(report_path)}")

print("\nAll anchors analyzed.")
