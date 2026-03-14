"""
For each categorized.csv and consolidated.csv, report:
  - Total words still missing a reading (after pure-kana fix)
  - Non-Japanese tokens  : word has NO hiragana, katakana, or CJK characters
  - Potential proper nouns: missing reading AND word contains at least one kanji
                            (single-kanji names, place names, character names, etc.)

CJK Unified Ideographs ranges checked:
  U+4E00–U+9FFF   (main block)
  U+3400–U+4DBF   (Extension A)
  U+20000–U+2A6DF (Extension B)
  U+F900–U+FAFF   (Compatibility Ideographs)
"""

import csv
from pathlib import Path

ALL_DIR = Path(__file__).parent

HIRA  = (0x3040, 0x309F)
KATA  = (0x30A0, 0x30FF)
CJK_RANGES = [
    (0x4E00,  0x9FFF),
    (0x3400,  0x4DBF),
    (0x20000, 0x2A6DF),
    (0xF900,  0xFAFF),
]

def _has_japanese(word: str) -> bool:
    for ch in word:
        cp = ord(ch)
        if HIRA[0] <= cp <= HIRA[1]: return True
        if KATA[0] <= cp <= KATA[1]: return True
        if any(lo <= cp <= hi for lo, hi in CJK_RANGES): return True
    return False

def _has_kanji(word: str) -> bool:
    for ch in word:
        cp = ord(ch)
        if any(lo <= cp <= hi for lo, hi in CJK_RANGES):
            return True
    return False

targets = (
    sorted(ALL_DIR.glob("*/categorized.csv")) +
    sorted(ALL_DIR.glob("*/consolidated.csv"))
)

for csv_path in targets:
    total = missing = non_japanese = proper_nouns = 0
    non_jp_examples = []
    pn_examples     = []

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "hiragana" not in (reader.fieldnames or []):
            print(f"{csv_path.relative_to(ALL_DIR)}: no hiragana column\n")
            continue
        for row in reader:
            word = row["word"]
            if not word:
                continue
            total += 1
            if not row["hiragana"]:
                missing += 1
                if not _has_japanese(word):
                    non_japanese += 1
                    if len(non_jp_examples) < 8:
                        non_jp_examples.append(word)
                elif _has_kanji(word):
                    proper_nouns += 1
                    if len(pn_examples) < 8:
                        pn_examples.append(word)

    label = csv_path.relative_to(ALL_DIR)
    print(f"=== {label} ===")
    print(f"  total words       : {total:,}")
    print(f"  missing reading   : {missing:,}  ({missing/total*100:.1f}%)")
    print(f"  non-Japanese      : {non_japanese:,}  — e.g. {non_jp_examples}")
    print(f"  potential proper  : {proper_nouns:,}  — e.g. {pn_examples}")
    print()
