"""
Shared rendering utilities for CEJC analysis scripts.

Functions:
    markdown_table         — GFM table
    ascii_bar_chart        — horizontal ASCII bar chart
    ascii_stacked_bar_chart — stacked proportional bar chart
    mermaid_pie            — Mermaid pie chart code block
    mermaid_graph          — Mermaid graph code block
"""

STACKED_CHARS = "█▓▒░▄▀"
BAR_CHAR = "█"
DEFAULT_BAR_WIDTH = 40


# ── Markdown table ─────────────────────────────────────────────────────────────

def markdown_table(headers: list, rows: list) -> str:
    str_rows = [[str(c) for c in row] for row in rows]
    str_headers = [str(h) for h in headers]
    widths = [
        max(len(str_headers[i]), max((len(r[i]) for r in str_rows), default=0))
        for i in range(len(str_headers))
    ]

    def fmt_row(cells):
        return "| " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(cells)) + " |"

    sep = "| " + " | ".join("-" * w for w in widths) + " |"
    return "\n".join([fmt_row(str_headers), sep] + [fmt_row(r) for r in str_rows])


# ── ASCII bar chart ────────────────────────────────────────────────────────────

def ascii_bar_chart(items: list, fence: bool = False, max_bar: int = DEFAULT_BAR_WIDTH) -> str:
    """
    items: list of (label: str, value: float)
    Renders one horizontal bar per item, scaled to the maximum value.
    """
    if not items:
        return ""

    labels = [l for l, _ in items]
    values = [v for _, v in items]
    total = sum(values)
    max_val = max(values) if values else 1
    label_w = max(len(l) for l in labels)
    count_w = max(len(f"{v:.1f}") for v in values)

    lines = []
    for label, val in items:
        bar_len = round(val / max_val * max_bar) if max_val else 0
        bar = BAR_CHAR * bar_len
        pct = f"({val / total * 100:.1f}%)" if total else "(0.0%)"
        line = f"{label:<{label_w}}  {bar:<{max_bar}}  {val:{count_w}.1f}  {pct}"
        lines.append(line)

    content = "\n".join(lines)
    return f"```\n{content}\n```" if fence else content


# ── ASCII stacked bar chart ────────────────────────────────────────────────────

def ascii_stacked_bar_chart(
    rows: list,
    max_width: int = 50,
    fence: bool = True,
) -> str:
    """
    rows: list of (label: str, segments: dict[str, float])
          where each segments value is a percentage (0–100).
    Renders a stacked proportional bar per row using block characters.
    """
    if not rows:
        return ""

    # Canonical segment order from the first row
    all_segs = list(rows[0][1].keys())
    seg_chars = {seg: STACKED_CHARS[i % len(STACKED_CHARS)] for i, seg in enumerate(all_segs)}
    label_w = max(len(label) for label, _ in rows)

    lines = []
    for label, seg_dict in rows:
        bar = ""
        allocated = 0
        seg_items = list(seg_dict.items())
        for i, (seg, pct) in enumerate(seg_items):
            if i == len(seg_items) - 1:
                seg_len = max_width - allocated
            else:
                seg_len = round(pct / 100 * max_width)
            allocated += seg_len
            bar += seg_chars.get(seg, BAR_CHAR) * max(seg_len, 0)

        legend_parts = [f"{seg}:{int(round(pct))}%" for seg, pct in seg_dict.items()]
        legend = "  ".join(legend_parts)
        lines.append(f"{label:<{label_w}}  {bar}  {legend}")

    # Legend key
    lines.append("")
    lines.append("Legend: " + "  ".join(f"{seg_chars[s]} = {s}" for s in all_segs))

    content = "\n".join(lines)
    return f"```\n{content}\n```" if fence else content


# ── Mermaid pie chart ──────────────────────────────────────────────────────────

def mermaid_pie(title: str, items: list) -> str:
    """
    items: list of (label: str, value: float)
    """
    lines = ['```mermaid', f'pie title "{title}"']
    for label, val in items:
        lines.append(f'    "{label}" : {float(val):.2f}')
    lines.append("```")
    return "\n".join(lines)


# ── Mermaid graph ──────────────────────────────────────────────────────────────

def mermaid_graph(edges: list, directed: bool = False) -> str:
    """
    edges: list of (node_a: str, node_b: str, label: str)
    """
    arrow = "-->" if directed else "---"
    lines = ["```mermaid", "graph LR"]
    for a, b, label in edges:
        lines.append(f'    {a} {arrow}|"{label}"| {b}')
    lines.append("```")
    return "\n".join(lines)
