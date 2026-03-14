"""
Shared rendering utilities for ALL analysis scripts.
"""

BAR_CHAR = "█"
DEFAULT_BAR_WIDTH = 40


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


def ascii_bar_chart(items: list, fence: bool = True, max_bar: int = DEFAULT_BAR_WIDTH) -> str:
    """items: list of (label, value). Renders horizontal bar chart."""
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
        lines.append(f"{label:<{label_w}}  {bar:<{max_bar}}  {val:{count_w}.1f}  {pct}")

    content = "\n".join(lines)
    return f"```\n{content}\n```" if fence else content
