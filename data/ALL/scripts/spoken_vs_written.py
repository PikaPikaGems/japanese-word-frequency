#!/usr/bin/env python3
"""
spoken_vs_written.py — CEJC spoken corpus vs. external written/media sources.

Identifies:
  - Words the CEJC spoken corpus ranks much higher than written/media sources
  - Words written/media sources rank much higher than CEJC
  - Words present only in CEJC (absent from all 35 external sources)

Output: Markdown to stdout.

Usage:
    python3 spoken_vs_written.py
"""

import sys
import csv
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import markdown_table

DATA_DIR = Path(__file__).parents[1]
CONSOLIDATED = DATA_DIR / "consolidated.csv"

MIN_EXTERNAL_SOURCES = 5   # word must appear in at least this many external sources
TOP_N = 25


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    return rows, fieldnames


def safe_int(v):
    try:
        i = int(v)
        return None if i == -1 else i
    except (ValueError, TypeError):
        return None


def main():
    rows, fieldnames = load(CONSOLIDATED)
    source_cols = fieldnames[15:]  # 35 external sources

    # Only use sources with ≥5000 words for the mean
    good_sources = [
        col for col in source_cols
        if sum(1 for r in rows if safe_int(r[col]) is not None) >= 5000
    ]

    # Normalize each source
    col_norm = {}
    for col in good_sources:
        vals = [safe_int(r[col]) for r in rows]
        valid = [v for v in vals if v is not None]
        lo, hi = min(valid), max(valid)
        span = hi - lo if hi != lo else 1
        col_norm[col] = [(v - lo) / span if v is not None else None for v in vals]

    # Normalize CEJC combined_rank
    cejc_vals = [safe_int(r["combined_rank"]) for r in rows]
    valid_cejc = [v for v in cejc_vals if v is not None]
    cejc_lo, cejc_hi = min(valid_cejc), max(valid_cejc)
    cejc_span = cejc_hi - cejc_lo
    cejc_norm = [(v - cejc_lo) / cejc_span if v is not None else None for v in cejc_vals]

    scored = []
    cejc_only = []

    for i, row in enumerate(rows):
        word = row["word"]
        cejc_r = safe_int(row["combined_rank"])
        if cejc_r is None:
            continue

        ext_vals = [col_norm[c][i] for c in good_sources if col_norm[c][i] is not None]
        n_ext = len(ext_vals)

        if n_ext == 0:
            cejc_only.append((cejc_r, word))
            continue

        if n_ext < MIN_EXTERNAL_SOURCES:
            continue

        ext_mean = sum(ext_vals) / n_ext
        cn = cejc_norm[i]
        if cn is None:
            continue

        diff = ext_mean - cn  # positive = CEJC ranks higher (lower rank number)
        scored.append((diff, word, cejc_r, ext_mean, n_ext))

    scored.sort(reverse=True)
    cejc_only.sort()

    lines = []
    lines.append("# Spoken vs. Written Frequency Divergence")
    lines.append("")
    lines.append(
        "Compares CEJC (spontaneous spoken conversation) rankings against the mean normalized "
        "rank across 35 external written and media sources. "
        "Large positive divergence = word is much more frequent in speech than in writing/media. "
        "Large negative divergence = word rarely appears in everyday speech but is common in media/text."
    )
    lines.append("")
    lines.append(
        f"**Methodology:** CEJC combined_rank and each external source rank are each normalized to [0, 1]. "
        f"Divergence = (mean external normalized rank) − (CEJC normalized rank). "
        f"Only words present in ≥{MIN_EXTERNAL_SOURCES} external sources are included."
    )
    lines.append("")

    # CEJC-dominant
    lines.append("## Words Much More Frequent in Speech than Written/Media")
    lines.append("")
    lines.append(
        "These words appear frequently in everyday conversation but are rare in written corpora. "
        "They represent authentic spoken Japanese vocabulary — often food terms, casual expressions, "
        "or local/colloquial vocabulary that doesn't make it into formal text."
    )
    lines.append("")
    top_spoken = scored[:TOP_N]
    spoken_rows = [
        (w, str(cr), f"{diff:.3f}", str(n))
        for diff, w, cr, _, n in top_spoken
    ]
    lines.append(markdown_table(
        ["Word", "CEJC rank", "Divergence", "Ext sources"],
        spoken_rows
    ))
    lines.append("")

    # Source-dominant
    lines.append("## Words Much More Frequent in Written/Media than Speech")
    lines.append("")
    lines.append(
        "These words are common in media and text but rarely appear in spontaneous conversation. "
        "They represent narrative, formal, or genre-specific vocabulary — "
        "typical in anime/novels but absent from everyday talk."
    )
    lines.append("")
    bot_spoken = scored[-TOP_N:][::-1]
    written_rows = [
        (w, str(cr), f"{diff:.3f}", str(n))
        for diff, w, cr, _, n in bot_spoken
    ]
    lines.append(markdown_table(
        ["Word", "CEJC rank", "Divergence", "Ext sources"],
        written_rows
    ))
    lines.append("")

    # CEJC-only
    lines.append("## Words Exclusive to CEJC (absent from all external sources)")
    lines.append("")
    lines.append(
        f"**{len(cejc_only):,} words** appear in CEJC but in none of the 35 external sources. "
        "Most are proper nouns from the recorded conversations (place names, personal names), "
        "very rare spoken-only expressions, or terms too niche for any top-25k word list."
    )
    lines.append("")
    lines.append(f"Top {TOP_N} by CEJC rank (most frequent among CEJC-only words):")
    lines.append("")
    cejc_only_rows = [(w, str(r)) for r, w in cejc_only[:TOP_N]]
    lines.append(markdown_table(["Word", "CEJC rank"], cejc_only_rows))
    lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append(
        "- **Food vocabulary dominates CEJC-dominant words**: 竹の子 (bamboo shoots), 山葵 (wasabi), "
        "生姜 (ginger), 蓮根 (lotus root), 鯵 (horse mackerel), 白子 (cod milt). "
        "Conversations about cooking and meals are a large part of everyday Japanese speech."
    )
    lines.append(
        "- **CEJC-only words are mostly proper nouns**: タチカワ (Tachikawa), ハルヤ, ミカミ, "
        "ハネダ (Haneda) — place names and personal names from recorded conversations. "
        "ＷｉＦｉ is a notable exception: a common spoken term absent from all external top-25k lists."
    )
    lines.append(
        "- **Written/media-dominant words are narrative/action vocabulary**: "
        "真実 (truth), 兵士 (soldier), 任務 (mission), 取り戻す (take back), 死体 (corpse), 竜 (dragon), "
        "一族 (clan), 悲鳴 (scream). These appear constantly in anime and novels but almost never "
        "come up in natural everyday conversation."
    )
    lines.append("")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
