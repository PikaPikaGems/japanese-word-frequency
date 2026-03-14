"""
Kana conversion utilities — hiragana ↔ katakana.

Hiragana: U+3041–U+3096
Katakana: U+30A1–U+30F6
Offset between the two blocks: 0x60 (96 code points)
"""

_HIRA_START = 0x3041  # ぁ
_HIRA_END   = 0x3096  # ゖ
_KATA_START = 0x30A1  # ァ
_KATA_END   = 0x30F6  # ヶ
_OFFSET     = 0x60


def hiragana_to_katakana(text: str) -> str:
    """Convert hiragana characters in *text* to their katakana equivalents.

    Non-hiragana characters are passed through unchanged.
    """
    result = []
    for ch in text:
        cp = ord(ch)
        if _HIRA_START <= cp <= _HIRA_END:
            result.append(chr(cp + _OFFSET))
        else:
            result.append(ch)
    return "".join(result)


def katakana_to_hiragana(text: str) -> str:
    """Convert katakana characters in *text* to their hiragana equivalents.

    Non-katakana characters are passed through unchanged.
    """
    result = []
    for ch in text:
        cp = ord(ch)
        if _KATA_START <= cp <= _KATA_END:
            result.append(chr(cp - _OFFSET))
        else:
            result.append(ch)
    return "".join(result)


def is_pure_kana(word: str) -> bool:
    """Return True if *word* consists entirely of hiragana and/or katakana characters."""
    return bool(word) and all(0x3040 <= ord(c) <= 0x30FF for c in word)
