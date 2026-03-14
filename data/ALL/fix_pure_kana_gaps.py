"""
Fill missing hiragana/katakana readings for words that consist
entirely of kana characters (hiragana and/or katakana only).

For such words the reading IS the word itself:
  hiragana = katakana_to_hiragana(word)
  katakana  = hiragana_to_katakana(word)

Patches all categorized.csv and consolidated.csv files in-place.
"""

import csv
import importlib.util
from pathlib import Path

ROOT    = Path(__file__).parents[2]
ALL_DIR = Path(__file__).parent

_spec = importlib.util.spec_from_file_location("kana", ROOT / "utils" / "kana.py")
_mod  = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
hiragana_to_katakana = _mod.hiragana_to_katakana
katakana_to_hiragana = _mod.katakana_to_hiragana

# Hiragana block U+3040–U+309F, Katakana block U+30A0–U+30FF
def _is_pure_kana(word: str) -> bool:
    if not word:
        return False
    return all(0x3040 <= ord(ch) <= 0x30FF for ch in word)


def _patch(path: Path) -> int:
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))

    if not rows:
        return 0

    header = rows[0]
    if "hiragana" not in header or "katakana" not in header:
        return 0

    word_idx = header.index("word")
    hira_idx = header.index("hiragana")
    kata_idx = header.index("katakana")

    filled = 0
    for row in rows[1:]:
        if row[hira_idx]:
            continue  # already has a reading
        word = row[word_idx] if word_idx < len(row) else ""
        if _is_pure_kana(word):
            row[hira_idx] = katakana_to_hiragana(word)
            row[kata_idx] = hiragana_to_katakana(word)
            filled += 1

    with open(path, "w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(rows)

    return filled


targets = sorted(ALL_DIR.glob("*/categorized.csv")) + sorted(ALL_DIR.glob("*/consolidated.csv"))
for path in targets:
    n = _patch(path)
    print(f"{path.relative_to(ALL_DIR)}: filled {n} pure-kana gaps")
