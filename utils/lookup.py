"""
Japanese word reading resolution and cross-source rank lookup.

Builds bidirectional kana/kanji tables from JPDB v2 and CEJC TSV data,
then exposes get_reading() and lookup() for use across scripts.
"""

import csv

from .kana import hiragana_to_katakana, katakana_to_hiragana, is_pure_kana


class JapaneseLookup:
    """Loads JPDB v2 and CEJC TSV data to support reading lookup and
    bidirectional kana/kanji rank lookup across word frequency sources."""

    def __init__(self, jpdb_raw_path: str, cejc_tsv_path: str):
        # term → hiragana reading (most frequent reading wins)
        _jpdb_reading_tmp: dict[str, tuple[str, int]] = {}
        # kanji → kana (only where term != reading)
        _kana_fallback_tmp: dict[str, tuple[str, int]] = {}

        with open(jpdb_raw_path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                term = row["term"]
                reading = row["reading"]
                freq = int(row["frequency"])
                if term not in _jpdb_reading_tmp or freq < _jpdb_reading_tmp[term][1]:
                    _jpdb_reading_tmp[term] = (reading, freq)
                if term == reading:
                    continue
                if term not in _kana_fallback_tmp or freq < _kana_fallback_tmp[term][1]:
                    _kana_fallback_tmp[term] = (reading, freq)

        self._jpdb_reading: dict[str, str] = {
            t: r for t, (r, _) in _jpdb_reading_tmp.items()
        }
        self.kana_fallback: dict[str, str] = {
            t: r for t, (r, _) in _kana_fallback_tmp.items()
        }

        # kana → [kanji forms] (reverse of kana_fallback)
        self.kana_to_kanji: dict[str, list[str]] = {}
        for kanji, kana in self.kana_fallback.items():
            self.kana_to_kanji.setdefault(kana, []).append(kanji)

        # 語彙素 → katakana reading (fallback for words not in JPDB)
        self._cejc_reading: dict[str, str] = {}
        with open(cejc_tsv_path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f, delimiter="\t"):
                word = row.get("語彙素", "").strip()
                kata = row.get("語彙素読み", "").strip()
                if word and kata and word not in self._cejc_reading:
                    self._cejc_reading[word] = kata

    def get_reading(self, word: str) -> tuple[str, str]:
        """Return (hiragana, katakana) for word, or ('-', '-') if unknown."""
        if word in self._jpdb_reading:
            hira = self._jpdb_reading[word]
            return hira, hiragana_to_katakana(hira)
        if word in self._cejc_reading:
            kata = self._cejc_reading[word]
            return katakana_to_hiragana(kata), kata
        if is_pure_kana(word):
            return katakana_to_hiragana(word), hiragana_to_katakana(word)
        return "-", "-"

    def lookup(self, source: dict, word: str) -> int:
        """Look up word rank in source with bidirectional kana/kanji fallback.

        1. Direct match.
        2. Kanji word → try its kana reading in source.
        3. Kana word → try any kanji form that reads as this kana in source.
        Returns -1 if not found.
        """
        if word in source:
            return source[word]
        kana = self.kana_fallback.get(word)
        if kana and kana in source:
            return source[kana]
        for kanji in self.kana_to_kanji.get(word, []):
            if kanji in source:
                return source[kanji]
        return -1
