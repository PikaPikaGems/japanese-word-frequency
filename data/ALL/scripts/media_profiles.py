#!/usr/bin/env python3
"""
media_profiles.py — Distinctive vocabulary per media-type group.

Groups the 35 sources by media type and finds the words each group
ranks unusually high relative to all other sources combined.

Output: Markdown to stdout.

Usage:
    python3 media_profiles.py
"""

import sys
import csv
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from utils import markdown_table

DATA_DIR = Path(__file__).parents[1]
CONSOLIDATED = DATA_DIR / "consolidated.csv"

TOP_N = 12  # distinctive words to show per group

MEDIA_GROUPS = {
    "Written / Wikipedia": {
        "sources": ["ADNO", "ILYASEMENOV", "WIKIPEDIA_V2", "CC100"],
        "description": "Wikipedia and general web text corpora",
    },
    "Literature / Novels": {
        "sources": [
            "AOZORA_BUNKO", "INNOCENT_RANKED", "NOVELS",
            "DD2_MORPHMAN_NOVELS", "DD2_YOMICHAN_NOVELS", "DD2_MIGAKU_NOVELS", "NAROU",
        ],
        "description": "Public-domain literature, novel corpora, web novels (Narou)",
    },
    "Anime / Drama": {
        "sources": [
            "ANIME_JDRAMA", "DAVE_DOEBRICK", "CHRISKEMPSON",
            "DD2_MORPHMAN_SHONEN", "DD2_YOMICHAN_SHONEN", "DD2_YOMICHAN_SHONEN_STARS",
            "JITEN_ANIME",
        ],
        "description": "Anime subtitles, J-drama, shōnen anime/manga",
    },
    "Netflix": {
        "sources": ["NETFLIX", "DD2_MIGAKU_NETFLIX", "DD2_MORPHMAN_NETFLIX"],
        "description": "Netflix subtitle corpora",
    },
    "Slice of Life Anime": {
        "sources": ["DD2_MORPHMAN_SOL", "DD2_YOMICHAN_SOL"],
        "description": "Slice-of-life anime subtitle corpora",
    },
    "Visual Novels": {
        "sources": ["VN_FREQ", "DD2_YOMICHAN_VN"],
        "description": "Visual novel script corpora",
    },
    "YouTube": {
        "sources": ["YOUTUBE_FREQ", "YOUTUBE_FREQ_V3"],
        "description": "YouTube subtitle frequency lists",
    },
    "Dictionary / Balanced": {
        "sources": ["KOKUGOJITEN", "MONODICTS", "H_FREQ", "BCCWJ"],
        "description": "Dictionary headwords, community lists, NINJAL balanced written corpus",
    },
}


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
    source_cols = fieldnames[15:]

    # Normalize each source's ranks to [0, 1]
    col_norm = {}
    for col in source_cols:
        vals = [safe_int(r[col]) for r in rows]
        valid = [v for v in vals if v is not None]
        if not valid:
            col_norm[col] = [None] * len(rows)
            continue
        lo, hi = min(valid), max(valid)
        span = hi - lo if hi != lo else 1
        col_norm[col] = [
            (v - lo) / span if v is not None else None
            for v in vals
        ]

    def group_mean(i, sources):
        vals = [col_norm[c][i] for c in sources if c in col_norm and col_norm[c][i] is not None]
        return sum(vals) / len(vals) if vals else None

    def group_coverage(i, sources):
        return sum(1 for c in sources if c in col_norm and col_norm[c][i] is not None)

    lines = []
    lines.append("# Media-Type Vocabulary Profiles")
    lines.append("")
    lines.append(
        "For each media-type group, the words ranked unusually high (lower normalized rank) "
        "relative to all other sources combined. A high 'advantage' score means this group "
        "considers the word much more frequent than the rest of the corpus collection does."
    )
    lines.append("")
    lines.append(
        "Note: character names and proper nouns often appear as distinctive words — "
        "they are frequent within a specific franchise's corpus but absent elsewhere."
    )
    lines.append("")

    all_group_sections = []
    for group_name, group_info in MEDIA_GROUPS.items():
        group_sources = [c for c in group_info["sources"] if c in source_cols]
        other_sources = [c for c in source_cols if c not in group_sources]

        # Compute advantage = other_mean - group_mean for each word
        # Positive = group ranks it higher (lower normalized rank number)
        scored = []
        for i, row in enumerate(rows):
            cov = group_coverage(i, group_sources)
            if cov < max(1, len(group_sources) // 3):
                continue
            gm = group_mean(i, group_sources)
            om = group_mean(i, other_sources)
            if gm is None or om is None:
                continue
            scored.append((om - gm, row["word"], int(row["combined_rank"])))

        scored.sort(reverse=True)
        top = scored[:TOP_N]

        section = []
        section.append(f"## {group_name}")
        section.append("")
        section.append(f"*{group_info['description']}*")
        section.append(f"*Sources: {', '.join(group_sources)}*")
        section.append("")
        section.append(f"Words this group ranks significantly higher than other sources:")
        section.append("")
        tbl_rows = [
            (w, str(rank), f"{adv:.3f}")
            for adv, w, rank in top
        ]
        section.append(markdown_table(["Word", "Overall rank", "Advantage score"], tbl_rows))
        section.append("")
        all_group_sections.append("\n".join(section))

    lines.extend(all_group_sections)

    lines.append("## Interpretation Notes")
    lines.append("")
    lines.append(
        "- **Advantage score**: difference in mean normalized rank between other sources and this group. "
        "Higher = this group ranks the word more frequently by a larger margin."
    )
    lines.append(
        "- **Slice of Life / Anime**: many top distinctive words are female character names "
        "(ユカリ, タマミ, カズミ) and school-life vocabulary (席替え = seat shuffle, 追試 = makeup exam)."
    )
    lines.append(
        "- **Visual Novels**: top distinctive words skew toward adult content vocabulary — "
        "a known characteristic of the VN corpus."
    )
    lines.append(
        "- **YouTube**: top distinctive words are practical/DIY terms "
        "(画角 = camera angle/framing, コンセント = electrical outlet, 付箋 = sticky note, レジュメ = résumé/handout). "
        "YouTube tutorials and how-to content drive this vocabulary."
    )
    lines.append(
        "- **Dictionary / Balanced**: top distinctive words are classical and archaic terms "
        "(なむ, 拾遺, 若紫 from Tale of Genji, 雅楽 = court music). "
        "Dictionaries include headwords that almost never appear in modern media."
    )
    lines.append("")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
