"""
Shared utilities for anchor analysis scripts (experiments0, experiments1, top12k).
"""


def resolve_anchor_col(anchor_name: str, header: list) -> str:
    """Return the rank column name for this anchor in the CSV header.

    The standard naming convention is "{ANCHOR_NAME}_rank" (e.g. "NETFLIX_rank",
    "BCCWJ_rank"). CEJC is the exception: its anchor column is "cejc_combined_rank"
    because the CSV has sub-corpus columns and uses a combined rank, not a simple
    "{ANCHOR_NAME}_rank".

    The fallback prefix-match finds any header column that starts with the anchor
    name (case-insensitive) and ends with "_rank", so it handles CEJC and any future
    anchors whose rank column doesn't follow the standard naming.
    """
    col = f"{anchor_name}_rank"
    if col not in header:
        # Fallback for anchors like CEJC whose rank column is "cejc_combined_rank".
        candidates = [c for c in header if c.lower().startswith(anchor_name.lower()) and c.endswith("_rank")]
        if candidates:
            col = candidates[0]
    return col


def get_anchor_family_cols(anchor_name: str, header: list) -> set:
    """Return all columns that belong to this anchor (anchor col + sub-corpus cols).

    For most anchors this is just the single rank column (e.g. "NETFLIX_rank").
    For CEJC it also includes the 13 domain sub-corpus columns (cejc_small_talk_rank,
    cejc_meeting_rank, etc.) which are internal breakdowns of CEJC itself, not
    independent external sources. All of these are prefixed with the anchor name
    (case-insensitive) to make them detectable.

    Excluding the whole family from source checks ensures CEJC is compared against
    the same ~38 external sources as every other anchor.
    """
    prefix = anchor_name.lower() + "_"
    return {c for c in header if c.lower().startswith(prefix)}
