"""
Check that kanji words have their readings populated.
Prints the first 20 rows with non-empty hiragana for one file.
"""

import csv
from pathlib import Path

path = Path(__file__).parent / "CEJC_anchor" / "consolidated.csv"

count = 0
with open(path, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        word = row["word"]
        hira = row["hiragana"]
        kata = row["katakana"]
        # show rows where word != hiragana (i.e. contains kanji or katakana)
        if hira and word != hira:
            print(f"{word!s:<12} hira={hira!s:<12} kata={kata!s:<12}")
            count += 1
            if count >= 20:
                break
