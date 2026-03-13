"""
Analysis helpers for CEJC frequency data.

Data shape (cejc.json):
  { word: [ entry, ... ] }

  entry = {
    "reading":      str,
    "pos":          str,
    "subcategory":  str,
    "origin":       str,
    "combined":     [rank, freq, pmw],
    "domains":      { domain_key: [rank, freq, pmw], ... },
    "demographics": { demo_key:   [rank, freq, pmw], ... },
  }

The "overall rank" for a word is the minimum combined[0] across all its
POS entries (a word can appear multiple times with different POS tags).
"""

from collections import defaultdict


def word_min_rank(entries: list) -> int:
    """Return the minimum combined rank across all POS entries for a word."""
    return min(e["combined"][0] for e in entries)


def tier_slice(data: dict, top_n: int) -> dict:
    """Return a subset of data keeping only words with min rank <= top_n."""
    return {word: entries for word, entries in data.items()
            if word_min_rank(entries) <= top_n}


def flat_entries(data: dict):
    """Yield (word, entry) pairs for every POS entry of every word."""
    for word, entries in data.items():
        for entry in entries:
            yield word, entry


def count_distribution(entries, key_fn) -> dict[str, int]:
    """Count occurrences of key_fn(entry) across a list of entries.

    Returns {label: count} sorted descending by count.
    """
    counts: dict[str, int] = defaultdict(int)
    for entry in entries:
        counts[key_fn(entry)] += 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))


def get_pmw(entry: dict, *keys) -> float:
    """Navigate into a nested entry structure and return the pmw value (index 2).

    Examples:
        get_pmw(entry, "combined")                  → entry["combined"][2]
        get_pmw(entry, "demographics", "m")         → entry["demographics"]["m"][2]
        get_pmw(entry, "domains", "home")           → entry["domains"]["home"][2]
    """
    val = entry
    for k in keys:
        val = val[k]
    return float(val[2])


def pmw_ratio(entry: dict, path_a: tuple, path_b: tuple) -> float | None:
    """Return pmw_a / pmw_b for two paths into an entry. None if pmw_b is 0.

    Example:
        pmw_ratio(entry, ("demographics", "m"), ("demographics", "f"))
    """
    pmw_a = get_pmw(entry, *path_a)
    pmw_b = get_pmw(entry, *path_b)
    return pmw_a / pmw_b if pmw_b != 0 else None
