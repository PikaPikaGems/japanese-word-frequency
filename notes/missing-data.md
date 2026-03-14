# Missing Datasets — Referenced but Not Processed

These sources are described in [`consolidated-reference-verbose.md`](consolidated-reference-verbose.md)
and/or [`consolidated-reference-short.md`](consolidated-reference-short.md)
but have **no corresponding processed data** anywhere under `data/` (no entry in `data/RAW/___FILTERED/`,
nor a standalone directory like `data/CEJC/` or `data/RSPEER/`).

## 1. Tsukuba Web Corpus (TWC)

**Listed in:** both notes files

- ~1.1 billion words of Japanese web text
- Creator: University of Tsukuba + NINJAL collaboration
- Official search interface: https://tsukubawebcorpus.jp/en/
- **Why not processed:** Primarily a collocation/lexical profiling tool. No bulk frequency list download; headword list available as `.xlsx` from their site but not distributed in a Yomitan-compatible format. Access focused on research/educational use.

---

## 2. JLPT Vocab Frequency

**Listed in:** both notes files

- JLPT N5–N1 vocabulary organized by level, used as a frequency proxy
- Creator: stephenmk (yomichan-jlpt-vocab dict), distributed via [MarvNC collection](https://github.com/MarvNC/yomitan-dictionaries)
- **Why not processed:** Not a corpus-based frequency list — it reflects exam vocabulary levels, not naturally observed frequency. Lower priority compared to true corpus sources. Useful as a supplement but not a frequency ranking in the traditional sense.

---

## Summary Table

| Dataset                  | In verbose? | In short? | Reason not processed                         |
| ------------------------ | ----------- | --------- | -------------------------------------------- |
| Tsukuba Web Corpus (TWC) | ✓           | ✓         | No bulk download; tool-only access           |
| JLPT Vocab Frequency     | ✓           | ✓         | Not a true frequency corpus; proxy data only |

---
