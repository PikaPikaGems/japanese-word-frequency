#!/usr/bin/env python3
"""
Convert CEJC TSV frequency data to JSON files.

Usage:
    python3 tsv_to_json.py <input.tsv> <output_dir> [top_n]

Outputs three JSON files in <output_dir>:
    cejc.json            — combined, domains, demographics per word
    cejc.cross.json      — conversation-type × location cross-tabs per word
    cejc.gender_age.json — gender × age cross-tabs per word

Only the top <top_n> words by overall frequency rank are included
(default: 12,000).

Each word key maps to an array of entries (one per POS), since the same
word surface form can appear multiple times with different grammatical
categories (e.g. の as 助詞-格助詞, 助詞-準体助詞, 助詞-終助詞).

All leaf values are [rank, freq, pmw] arrays.
"""

import csv
import json
import sys
from pathlib import Path

DEFAULT_TOP_N = 12000

DOMAIN_COLS = {
    "small_talk":        "雑談",
    "consultation":      "用談・相談",
    "meeting":           "会議・会合",
    "class":             "授業・レッスン",
    "outdoors":          "屋外",
    "school":            "学校",
    "transportation":    "交通機関",
    "public_commercial": "公共商業施設",
    "home":              "自宅",
    "indoors":           "室内",
    "workplace":         "職場",
}

CROSS_CONV_COLS = {
    "small_talk":   "雑談",
    "consultation": "用談・相談",
    "meeting":      "会議・会合",
    "class":        "授業・レッスン",
}

CROSS_LOC_COLS = {
    "outdoors":          "屋外",
    "school":            "学校",
    "transportation":    "交通機関",
    "public_commercial": "公共商業施設",
    "home":              "自宅",
    "indoors":           "室内",
    "workplace":         "職場",
}

AGE_COLS = {
    "0_4":     "0-4歳",
    "5_9":     "5-9歳",
    "10_14":   "10-14歳",
    "15_19":   "15-19歳",
    "20_24":   "20-24歳",
    "25_29":   "25-29歳",
    "30_34":   "30-34歳",
    "35_39":   "35-39歳",
    "40_44":   "40-44歳",
    "45_49":   "45-49歳",
    "50_54":   "50-54歳",
    "55_59":   "55-59歳",
    "60_64":   "60-64歳",
    "65_69":   "65-69歳",
    "70_74":   "70-74歳",
    "75_79":   "75-79歳",
    "80_84":   "80-84歳",
    "85_89":   "85-89歳",
    "90_94":   "90-94歳",
    "unknown": "年齢不明",
}


def rfp(row, prefix):
    """Extract [rank, freq, pmw] for a column prefix."""
    r = int(row[prefix + "_rank"])
    f = int(row[prefix + "_frequency"])
    p = round(float(row[prefix + "_pmw"]), 4)
    return [r, f, p]


def convert(tsv_path: Path, out_dir: Path, top_n: int = DEFAULT_TOP_N):
    out_dir.mkdir(parents=True, exist_ok=True)

    main = {}
    cross = {}
    gender_age = {}

    with tsv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")

        for row in reader:
            rank = int(row["rank"])
            if rank > top_n:
                continue

            word = row["語彙素"]

            # ── main ────────────────────────────────────────────────────
            domains = {k: rfp(row, v) for k, v in DOMAIN_COLS.items()}

            demographics = {"m": rfp(row, "男性"), "f": rfp(row, "女性")}
            for age_key, age_jp in AGE_COLS.items():
                demographics[age_key] = rfp(row, age_jp)

            main.setdefault(word, []).append({
                "reading":     row["語彙素読み"],
                "pos":         row["品詞"],
                "subcategory": row["語彙素細分類"],
                "origin":      row["語種"],
                "combined":    [rank, int(row["frequency"]), round(float(row["pmw"]), 4)],
                "domains":     domains,
                "demographics": demographics,
            })

            # ── cross (conversation × location) ────────────────────────
            cross_entry = {}
            for conv_key, conv_jp in CROSS_CONV_COLS.items():
                locs = {}
                for loc_key, loc_jp in CROSS_LOC_COLS.items():
                    locs[loc_key] = rfp(row, f"{conv_jp}_{loc_jp}")
                cross_entry[conv_key] = locs
            cross.setdefault(word, []).append(cross_entry)

            # ── gender_age ──────────────────────────────────────────────
            ga_entry = {}
            for gender_key, gender_jp in [("m", "男性"), ("f", "女性")]:
                ages = {}
                for age_key, age_jp in AGE_COLS.items():
                    ages[age_key] = rfp(row, f"{gender_jp}_{age_jp}")
                ga_entry[gender_key] = ages
            gender_age.setdefault(word, []).append(ga_entry)

    def write(name, data):
        path = out_dir / name
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        unique_words = len(data)
        total_entries = sum(len(v) for v in data.values())
        print(f"Wrote {path}  ({unique_words:,} words, {total_entries:,} entries)")

    write("cejc.json", main)
    write("cejc.cross.json", cross)
    write("cejc.gender_age.json", gender_age)


if __name__ == "__main__":
    if not (3 <= len(sys.argv) <= 4):
        print("Usage: python3 tsv_to_json.py <input.tsv> <output_dir> [top_n]")
        sys.exit(1)

    tsv_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    top_n = int(sys.argv[3]) if len(sys.argv) == 4 else DEFAULT_TOP_N

    if not tsv_path.exists():
        print(f"Error: {tsv_path} not found")
        sys.exit(1)

    convert(tsv_path, out_dir, top_n)
