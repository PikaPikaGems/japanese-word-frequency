"""
Analyzes consolidated.csv for data coverage:
  - Task 1: words with zero -1s across all sources (excl. AOZORA_BUNKO) -> zero_missing.csv
  - Task 3: per-source % missing, restricted to top-25k CEJC words -> coverage_analysis.md
  - Task 5: distribution of how many sources each word is missing from -> coverage_analysis.md
"""

import csv
import os

csv.field_size_limit(10_000_000)

BASE = os.path.dirname(os.path.abspath(__file__))
INPUT = os.path.join(BASE, "data", "ALL", "consolidated.csv")
ZERO_MISSING_OUT = os.path.join(BASE, "data", "ALL", "zero_missing.csv")
REPORT_OUT = os.path.join(BASE, "data", "ALL", "coverage_analysis.md")

CEJC_COLS = {
    "combined_rank", "small_talk_rank", "consultation_rank", "meeting_rank",
    "class_rank", "outdoors_rank", "school_rank", "transportation_rank",
    "public_commercial_rank", "home_rank", "indoors_rank", "workplace_rank",
    "male_rank", "female_rank",
}
EXCLUDE = {"AOZORA_BUNKO"}

with open(INPUT, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    all_cols = reader.fieldnames
    source_cols = [c for c in all_cols if c != "word" and c not in CEJC_COLS]
    check_cols = [c for c in source_cols if c not in EXCLUDE]
    rows = list(reader)

total = len(rows)

# ── Task 1: zero missing ───────────────────────────────────────────────────────
zero_rows = [r for r in rows if all(r[c] != "-1" for c in check_cols)]
with open(ZERO_MISSING_OUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=all_cols)
    writer.writeheader()
    writer.writerows(zero_rows)
print(f"Task 1: {len(zero_rows)} words with zero -1s -> zero_missing.csv")

# ── Task 3: per-source missing % (top-25k CEJC only) ─────────────────────────
top25k = [r for r in rows if r["combined_rank"] != "-1" and int(r["combined_rank"]) <= 25000]
n25 = len(top25k)

source_missing = {}
for col in source_cols:
    missing = sum(1 for r in top25k if r[col] == "-1")
    source_missing[col] = missing

# ── Task 5: distribution of missing-source count per word ────────────────────
def count_missing(row):
    return sum(1 for c in check_cols if row[c] == "-1")

missing_counts = [count_missing(r) for r in rows]
max_missing = max(missing_counts)
dist = [0] * (max_missing + 1)
for c in missing_counts:
    dist[c] += 1

# ── Write report ──────────────────────────────────────────────────────────────
BAR_WIDTH = 40

def bar(val, total_val):
    filled = round(BAR_WIDTH * val / total_val) if total_val else 0
    return "[" + "#" * filled + "-" * (BAR_WIDTH - filled) + "]"

lines = []
lines.append("# Coverage Analysis")
lines.append(f"\nTotal words (CEJC): {total}  |  Top-25k CEJC words: {n25}  |  Source columns: {len(source_cols)} (excl. AOZORA_BUNKO: {len(check_cols)})\n")

# Task 3 table
lines.append("## Per-Source Missing Rate (top-25k CEJC words)\n")
lines.append(f"{'Source':<35} {'Missing':>7}  {'%':>6}  Bar")
lines.append("-" * 80)
for col, miss in sorted(source_missing.items(), key=lambda x: -x[1]):
    pct = 100 * miss / n25
    note = " [EXCLUDED]" if col in EXCLUDE else ""
    lines.append(f"{col:<35} {miss:>7}  {pct:>5.1f}%  {bar(miss, n25)}{note}")

# Task 5 distribution
lines.append("\n## Distribution: How Many Sources Is Each Word Missing From?")
lines.append(f"(Excludes AOZORA_BUNKO; {len(check_cols)} source columns checked)\n")
lines.append(f"{'Missing':>8}  {'Words':>7}  {'%':>6}  Bar")
lines.append("-" * 70)
for i, count in enumerate(dist):
    pct = 100 * count / total
    lines.append(f"{i:>8}  {count:>7}  {pct:>5.1f}%  {bar(count, total)}")

lines.append(f"\nWords with zero -1s: {dist[0]}  ({100*dist[0]/total:.1f}%)")

report = "\n".join(lines)
with open(REPORT_OUT, "w", encoding="utf-8") as f:
    f.write(report)

print(f"Task 3 + 5: report written -> coverage_analysis.md")
print(report)
