"""
Output formatting utilities — all functions return strings.
"""

import unicodedata


# ── Display-width helpers ─────────────────────────────────────────────────────

def _dw(s: str) -> int:
    """Return the display width of a string.

    Full-width and wide CJK characters count as 2 columns; everything else as 1.
    This is needed because str.ljust() / len() count code points, not columns.
    """
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1 for c in s)


def _pad(s: str, width: int) -> str:
    """Left-pad string to a given display width using spaces."""
    return s + " " * max(0, width - _dw(s))


# ── Markdown ─────────────────────────────────────────────────────────────────

def markdown_table(headers: list[str], rows: list[list]) -> str:
    """Render a GitHub-flavoured Markdown table.

    Args:
        headers: Column header labels.
        rows:    List of rows; each row is a list of cell values (str or number).
    """
    def cell(v) -> str:
        return str(v).replace("|", "\\|")

    col_widths = [_dw(h) for h in headers]
    str_rows = [[cell(v) for v in row] for row in rows]
    for row in str_rows:
        for i, v in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], _dw(v))

    def fmt_row(cells):
        return "| " + " | ".join(_pad(c, col_widths[i]) for i, c in enumerate(cells)) + " |"

    sep = "| " + " | ".join("-" * w for w in col_widths) + " |"
    lines = [fmt_row(headers), sep] + [fmt_row(row) for row in str_rows]
    return "\n".join(lines)


# ── ASCII charts ─────────────────────────────────────────────────────────────

def ascii_bar_chart(
    items: list[tuple[str, float]],
    max_width: int = 40,
    title: str = "",
    fence: bool = False,
) -> str:
    """Horizontal ASCII bar chart.

    Args:
        items:     List of (label, value) pairs.
        max_width: Width of the widest bar in characters.
        title:     Optional title printed above the chart.
        fence:     Wrap output in a triple-backtick code block for monospace rendering.
    """
    if not items:
        return ""

    max_val = max(v for _, v in items)
    total   = sum(v for _, v in items)
    label_w = max(_dw(lbl) for lbl, _ in items)

    lines = []
    if title:
        lines.append(title)

    for label, value in items:
        bar_len = int(round(value / max_val * max_width)) if max_val else 0
        bar     = "█" * bar_len
        pct     = value / total * 100 if total else 0
        lines.append(f"{_pad(label, label_w)}  {bar:<{max_width}}  {value:>8.1f}  ({pct:.1f}%)")

    body = "\n".join(lines)
    if fence:
        return f"```\n{body}\n```"
    return body


def ascii_stacked_bar_chart(
    rows: list[tuple[str, dict[str, float]]],
    max_width: int = 40,
    title: str = "",
    fill_chars: str = "█▓▒░▄▀",
    fence: bool = False,
) -> str:
    """Stacked horizontal ASCII bar chart.

    Each row is (label, {segment_key: value}). Segments are drawn left-to-right
    using characters from fill_chars (cycling if needed), then a legend is appended.

    Args:
        rows:       List of (row_label, {segment: value}) pairs.
        max_width:  Total bar width in characters.
        title:      Optional title.
        fill_chars: Characters used for successive segments.
        fence:      Wrap output in a triple-backtick code block.
    """
    if not rows:
        return ""

    # Collect all segment keys in order of first appearance
    all_keys: list[str] = []
    seen: set[str] = set()
    for _, seg_dict in rows:
        for k in seg_dict:
            if k not in seen:
                all_keys.append(k)
                seen.add(k)

    label_w  = max(_dw(lbl) for lbl, _ in rows)
    char_map = {k: fill_chars[i % len(fill_chars)] for i, k in enumerate(all_keys)}

    lines = []
    if title:
        lines.append(title)

    for label, seg_dict in rows:
        total = sum(seg_dict.values())
        bar   = ""
        for k in all_keys:
            v = seg_dict.get(k, 0)
            seg_len = int(round(v / total * max_width)) if total else 0
            bar += char_map[k] * seg_len
        bar = (bar + " " * max_width)[:max_width]

        pcts = "  ".join(
            f"{k}:{seg_dict.get(k, 0) / total * 100:.0f}%" if total else f"{k}:0%"
            for k in all_keys
        )
        lines.append(f"{_pad(label, label_w)}  {bar}  {pcts}")

    legend = "  ".join(f"{char_map[k]} = {k}" for k in all_keys)
    lines += ["", f"Legend: {legend}"]

    body = "\n".join(lines)
    if fence:
        return f"```\n{body}\n```"
    return body


# ── Mermaid diagrams ──────────────────────────────────────────────────────────

def mermaid_pie(title: str, items: list[tuple[str, float]]) -> str:
    """Return a fenced mermaid pie chart block.

    Args:
        title: Chart title.
        items: List of (label, value) pairs.
    """
    lines = ["```mermaid", f'pie title "{title}"']
    for label, value in items:
        lines.append(f'    "{label}" : {value:.2f}')
    lines.append("```")
    return "\n".join(lines)


def mermaid_graph(
    edges: list[tuple[str, str, str | None]],
    directed: bool = False,
) -> str:
    """Return a fenced mermaid graph block.

    Args:
        edges:    List of (from_node, to_node, label_or_None) tuples.
        directed: Use TD (top-down directed) if True, LR undirected otherwise.
    """
    direction = "TD" if directed else "LR"
    arrow     = "-->" if directed else "---"

    lines = ["```mermaid", f"graph {direction}"]
    for src, dst, label in edges:
        if label:
            lines.append(f'    {src} {arrow}|"{label}"| {dst}')
        else:
            lines.append(f"    {src} {arrow} {dst}")
    lines.append("```")
    return "\n".join(lines)
