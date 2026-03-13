#!/usr/bin/env python3
"""
Convert CEJC TSV frequency data to CSV files.

Usage:
    python3 tsv_to_csv.py <input.tsv> <output_dir> [top_n]

Outputs one CSV per breakdown in <output_dir>, all covering the top <top_n>
words by overall frequency rank (default: 12,000).

Each CSV has columns: word, rank, freq, pmw
Rows are sorted ascending by the rank column of that breakdown.

Output files:
    combined.csv
    domain.small_talk.csv         domain.consultation.csv
    domain.meeting.csv            domain.class.csv
    domain.outdoors.csv           domain.school.csv
    domain.transportation.csv     domain.public_commercial.csv
    domain.home.csv               domain.indoors.csv
    domain.workplace.csv
    demographics.m.csv            demographics.f.csv
    demographics.0_4.csv  ...     demographics.unknown.csv
    cross.small_talk.outdoors.csv ... cross.class.workplace.csv  (28 files)
    gender_age.m.0_4.csv  ...     gender_age.f.unknown.csv      (40 files)
"""

import csv
import sys
from pathlib import Path

DEFAULT_TOP_N = 12000

# (output_key, tsv_prefix) pairs — tsv_prefix is used to build
# <prefix>_rank, <prefix>_frequency, <prefix>_pmw column names.
DOMAIN_COLS = [
    ("domain.small_talk",        "雑談"),
    ("domain.consultation",      "用談・相談"),
    ("domain.meeting",           "会議・会合"),
    ("domain.class",             "授業・レッスン"),
    ("domain.outdoors",          "屋外"),
    ("domain.school",            "学校"),
    ("domain.transportation",    "交通機関"),
    ("domain.public_commercial", "公共商業施設"),
    ("domain.home",              "自宅"),
    ("domain.indoors",           "室内"),
    ("domain.workplace",         "職場"),
]

DEMOGRAPHIC_COLS = [
    ("demographics.m",       "男性"),
    ("demographics.f",       "女性"),
    ("demographics.0_4",     "0-4歳"),
    ("demographics.5_9",     "5-9歳"),
    ("demographics.10_14",   "10-14歳"),
    ("demographics.15_19",   "15-19歳"),
    ("demographics.20_24",   "20-24歳"),
    ("demographics.25_29",   "25-29歳"),
    ("demographics.30_34",   "30-34歳"),
    ("demographics.35_39",   "35-39歳"),
    ("demographics.40_44",   "40-44歳"),
    ("demographics.45_49",   "45-49歳"),
    ("demographics.50_54",   "50-54歳"),
    ("demographics.55_59",   "55-59歳"),
    ("demographics.60_64",   "60-64歳"),
    ("demographics.65_69",   "65-69歳"),
    ("demographics.70_74",   "70-74歳"),
    ("demographics.75_79",   "75-79歳"),
    ("demographics.80_84",   "80-84歳"),
    ("demographics.85_89",   "85-89歳"),
    ("demographics.90_94",   "90-94歳"),
    ("demographics.unknown", "年齢不明"),
]

# Cross-tabulation: conversation type × location.
# TSV prefix is "{conv_jp}_{loc_jp}", e.g. "雑談_屋外".
CROSS_CONV_COLS = [
    ("small_talk",   "雑談"),
    ("consultation", "用談・相談"),
    ("meeting",      "会議・会合"),
    ("class",        "授業・レッスン"),
]

CROSS_LOC_COLS = [
    ("outdoors",          "屋外"),
    ("school",            "学校"),
    ("transportation",    "交通機関"),
    ("public_commercial", "公共商業施設"),
    ("home",              "自宅"),
    ("indoors",           "室内"),
    ("workplace",         "職場"),
]

# Gender × age cross-tabulation.
# TSV prefix is "{gender_jp}_{age_jp}", e.g. "男性_0-4歳".
# Note: age uses hyphens in TSV column names (0-4歳), not underscores.
GENDER_AGE_GENDER_COLS = [
    ("m", "男性"),
    ("f", "女性"),
]

GENDER_AGE_AGE_COLS = [
    ("0_4",     "0-4歳"),
    ("5_9",     "5-9歳"),
    ("10_14",   "10-14歳"),
    ("15_19",   "15-19歳"),
    ("20_24",   "20-24歳"),
    ("25_29",   "25-29歳"),
    ("30_34",   "30-34歳"),
    ("35_39",   "35-39歳"),
    ("40_44",   "40-44歳"),
    ("45_49",   "45-49歳"),
    ("50_54",   "50-54歳"),
    ("55_59",   "55-59歳"),
    ("60_64",   "60-64歳"),
    ("65_69",   "65-69歳"),
    ("70_74",   "70-74歳"),
    ("75_79",   "75-79歳"),
    ("80_84",   "80-84歳"),
    ("85_89",   "85-89歳"),
    ("90_94",   "90-94歳"),
    ("unknown", "年齢不明"),
]


def convert(tsv_path: Path, out_dir: Path, top_n: int = DEFAULT_TOP_N):
    out_dir.mkdir(parents=True, exist_ok=True)

    # Accumulate rows filtered to top_n by overall rank.
    # Each row: dict with 'word', 'overall_rank', 'overall_freq', 'overall_pmw',
    # plus per-breakdown tuples keyed by output_key.
    rows = []

    with tsv_path.open(encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")

        for row in reader:
            overall_rank = int(row["rank"])
            if overall_rank > top_n:
                continue

            entry = {
                "word":         row["語彙素"],
                "overall_rank": overall_rank,
                "overall_freq": int(row["frequency"]),
                "overall_pmw":  round(float(row["pmw"]), 4),
            }

            for key, prefix in DOMAIN_COLS + DEMOGRAPHIC_COLS:
                entry[key] = (
                    int(row[prefix + "_rank"]),
                    int(row[prefix + "_frequency"]),
                    round(float(row[prefix + "_pmw"]), 4),
                )

            for conv_key, conv_jp in CROSS_CONV_COLS:
                for loc_key, loc_jp in CROSS_LOC_COLS:
                    prefix = f"{conv_jp}_{loc_jp}"
                    entry[f"cross.{conv_key}.{loc_key}"] = (
                        int(row[prefix + "_rank"]),
                        int(row[prefix + "_frequency"]),
                        round(float(row[prefix + "_pmw"]), 4),
                    )

            for gender_key, gender_jp in GENDER_AGE_GENDER_COLS:
                for age_key, age_jp in GENDER_AGE_AGE_COLS:
                    prefix = f"{gender_jp}_{age_jp}"
                    entry[f"gender_age.{gender_key}.{age_key}"] = (
                        int(row[prefix + "_rank"]),
                        int(row[prefix + "_frequency"]),
                        round(float(row[prefix + "_pmw"]), 4),
                    )

            rows.append(entry)

    def write_csv(filename, sorted_rows, rank_fn, freq_fn, pmw_fn):
        path = out_dir / filename
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["word", "rank", "freq", "pmw"])
            for r in sorted_rows:
                writer.writerow([r["word"], rank_fn(r), freq_fn(r), pmw_fn(r)])
        print(f"Wrote {path}  ({len(sorted_rows):,} rows)")

    # combined — sort by overall rank
    write_csv(
        "combined.csv",
        sorted(rows, key=lambda r: r["overall_rank"]),
        lambda r: r["overall_rank"],
        lambda r: r["overall_freq"],
        lambda r: r["overall_pmw"],
    )

    # domain and demographic breakdowns — sort by each breakdown's rank
    for key, _ in DOMAIN_COLS + DEMOGRAPHIC_COLS:
        write_csv(
            f"{key}.csv",
            sorted(rows, key=lambda r, k=key: r[k][0]),
            lambda r, k=key: r[k][0],
            lambda r, k=key: r[k][1],
            lambda r, k=key: r[k][2],
        )

    # cross-tabulation: one CSV per (conv_type × location) pair
    for conv_key, _ in CROSS_CONV_COLS:
        for loc_key, _ in CROSS_LOC_COLS:
            key = f"cross.{conv_key}.{loc_key}"
            write_csv(
                f"{key}.csv",
                sorted(rows, key=lambda r, k=key: r[k][0]),
                lambda r, k=key: r[k][0],
                lambda r, k=key: r[k][1],
                lambda r, k=key: r[k][2],
            )

    # gender × age: one CSV per (gender × age_group) pair
    for gender_key, _ in GENDER_AGE_GENDER_COLS:
        for age_key, _ in GENDER_AGE_AGE_COLS:
            key = f"gender_age.{gender_key}.{age_key}"
            write_csv(
                f"{key}.csv",
                sorted(rows, key=lambda r, k=key: r[k][0]),
                lambda r, k=key: r[k][0],
                lambda r, k=key: r[k][1],
                lambda r, k=key: r[k][2],
            )


if __name__ == "__main__":
    if not (3 <= len(sys.argv) <= 4):
        print("Usage: python3 tsv_to_csv.py <input.tsv> <output_dir> [top_n]")
        sys.exit(1)

    tsv_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    top_n = int(sys.argv[3]) if len(sys.argv) == 4 else DEFAULT_TOP_N

    if not tsv_path.exists():
        print(f"Error: {tsv_path} not found")
        sys.exit(1)

    convert(tsv_path, out_dir, top_n)
