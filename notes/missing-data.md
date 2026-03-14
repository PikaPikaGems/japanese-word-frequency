# Missing Datasets — Referenced but Not Processed

These sources are described in [`consolidated-reference-verbose.md`](consolidated-reference-verbose.md)
and/or [`consolidated-reference-short.md`](consolidated-reference-short.md)
but have **no corresponding processed data** anywhere under `data/` (no entry in `data/RAW/___FILTERED/`,
nor a standalone directory like `data/CEJC/` or `data/RSPEER/`).

---

## 1. CSJ — Corpus of Spontaneous Japanese
**Listed in:** both notes files

- ~650 hours of spontaneous speech, ~7M words (primarily academic monologues/conference presentations)
- Creator: NINJAL + NICT + Tokyo Institute of Technology
- Yomitan dicts exist: [Maltesaa](https://github.com/Maltesaa/CSJ_and_NWJC_yomitan_freq_dict), [MarvNC collection](https://github.com/MarvNC/yomitan-dictionaries#corpus-of-spontaneous-japanese)
- **Why not processed:** NINJAL licensing restricts redistribution. Freq list is small (~31,605 entries). Skews formal/academic (less useful alongside CEJC for everyday spoken coverage).

---

## 2. NWJC — NINJAL Web Japanese Corpus
**Listed in:** both notes files

- ~25.8 billion tokens from crawled Japanese websites; one of the largest Japanese corpora by token count
- Creator: NINJAL (Masayu Asahara et al.)
- Yomitan dicts exist: [Maltesaa](https://github.com/Maltesaa/CSJ_and_NWJC_yomitan_freq_dict), [MarvNC collection](https://github.com/MarvNC/yomitan-dictionaries#ninjal-web-japanese-corpus)
- **Why not processed:** NINJAL licensing restricts redistribution of derived frequency dictionaries. Some community tools generate them locally from source data.

---

## 3. Tsukuba Web Corpus (TWC)
**Listed in:** both notes files

- ~1.1 billion words of Japanese web text
- Creator: University of Tsukuba + NINJAL collaboration
- Official search interface: https://tsukubawebcorpus.jp/en/
- **Why not processed:** Primarily a collocation/lexical profiling tool. No bulk frequency list download; headword list available as `.xlsx` from their site but not distributed in a Yomitan-compatible format. Access focused on research/educational use.

---

## 4. University of Leeds Corpus
**Listed in:** both notes files

- Web-crawled Japanese internet corpus (~44,998-word derived list from [hingston's GitHub](https://github.com/hingston/japanese))
- Creator: Centre for Translation Studies, University of Leeds (Serge Sharoff et al.)
- Reference: https://www.latl.leeds.ac.uk/resources/corpora-and-corpus-tools/
- **Why not processed:** Corpus noted as "temporarily unavailable outside the University of Leeds." Derived word lists exist on Wiktionary (CC BY-2.5) and hingston's GitHub, but the list is relatively old (~2005 onward) and small.

---

## 5. JLPT Vocab Frequency
**Listed in:** both notes files

- JLPT N5–N1 vocabulary organized by level, used as a frequency proxy
- Creator: stephenmk (yomichan-jlpt-vocab dict), distributed via [MarvNC collection](https://github.com/MarvNC/yomitan-dictionaries)
- **Why not processed:** Not a corpus-based frequency list — it reflects exam vocabulary levels, not naturally observed frequency. Lower priority compared to true corpus sources. Useful as a supplement but not a frequency ranking in the traditional sense.

---

## 6. Japanese Like a Breeze (Anime Frequency List)
**Listed in:** verbose notes only (not in short notes)

- ~2 million sentences from anime/dorama Anki decks; focuses on top ~2k words
- Creator: Joe (Japanese Like a Breeze blog), published September 2020
- Blog post: https://www.japanese-like-a-breeze.com/computing-a-word-frequency-list-based-on-anime/
- **Why not processed:** Small coverage (top ~2k words only). Anime subtitle domain already covered by `ANIME_JDRAMA`, `JITEN_ANIME`, and `YOUTUBE_FREQ*`. Known parsing issues with slang/sloppy speech. Lower added value given existing coverage.

---

## Summary Table

| Dataset                    | In verbose? | In short? | Reason not processed                              |
| -------------------------- | ----------- | --------- | ------------------------------------------------- |
| CSJ                        | ✓           | ✓         | Licensing + small size + formal register          |
| NWJC                       | ✓           | ✓         | Licensing restrictions                            |
| Tsukuba Web Corpus (TWC)   | ✓           | ✓         | No bulk download; tool-only access                |
| University of Leeds Corpus | ✓           | ✓         | Corpus unavailable externally; old/small          |
| JLPT Vocab Frequency       | ✓           | ✓         | Not a true frequency corpus; proxy data only      |
| Japanese Like a Breeze     | ✓           | ✗         | Small coverage; domain already covered by others  |

---

## Notes on Coverage

- The short reference file (`consolidated-reference-short.md`) covers 17 sources and omits 5 that **are** processed: Aozora Bunko, chriskempson, hermitdave/FrequencyWords, IlyaSemenov/wikipedia-word-frequency, and Kuuube's Novels (H_FREQ). Those are not missing — they are documented only in the verbose file and fully processed under `data/RAW/___FILTERED/`.
- All 35 sources in `data/RAW/___FILTERED/` and the 3 standalone datasets (`data/CEJC/`, `data/JPDBV2/`, `data/RSPEER/`) are accounted for across the two notes files.