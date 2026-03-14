"""
utils — general-purpose output formatting helpers.

Quick import:
    from utils import markdown_table, ascii_bar_chart, ascii_stacked_bar_chart, mermaid_pie, mermaid_graph
    from utils import hiragana_to_katakana, katakana_to_hiragana

Scripts in data/CEJC/scripts/ should add the repo root to sys.path first:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parents[3]))
"""

from .format import (
    markdown_table,
    ascii_bar_chart,
    ascii_stacked_bar_chart,
    mermaid_pie,
    mermaid_graph,
)
from .kana import hiragana_to_katakana, katakana_to_hiragana

__all__ = [
    "markdown_table",
    "ascii_bar_chart",
    "ascii_stacked_bar_chart",
    "mermaid_pie",
    "mermaid_graph",
    "hiragana_to_katakana",
    "katakana_to_hiragana",
]
