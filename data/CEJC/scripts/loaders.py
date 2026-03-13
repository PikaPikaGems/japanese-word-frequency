"""
Data loading utilities for CEJC frequency data.
"""

import csv
import json
from pathlib import Path


def load_cejc_json(json_dir) -> dict:
    """Load cejc.json → { word: [entry, ...] }

    Each entry has: reading, pos, subcategory, origin,
    combined [rank, freq, pmw], domains {key: [r,f,p]},
    demographics {key: [r,f,p]}.
    """
    path = Path(json_dir) / "cejc.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def load_cejc_cross_json(json_dir) -> dict:
    """Load cejc.cross.json → { word: [entry, ...] }

    Each entry has: { conv_type: { location: [rank, freq, pmw] } }
    """
    path = Path(json_dir) / "cejc.cross.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def load_cejc_gender_age_json(json_dir) -> dict:
    """Load cejc.gender_age.json → { word: [entry, ...] }

    Each entry has: { gender: { age_group: [rank, freq, pmw] } }
    """
    path = Path(json_dir) / "cejc.gender_age.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def load_csv(path) -> list[dict]:
    """Load a CEJC CSV file → list of row dicts with keys: word, rank, freq, pmw."""
    rows = []
    with Path(path).open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "word": row["word"],
                "rank": int(row["rank"]),
                "freq": int(row["freq"]),
                "pmw":  float(row["pmw"]),
            })
    return rows
