## Data Quality Notes (Last Run March 18, 2026)

### Inspecting the JPDB dataset

- **Surface forms, not lemmas.** JPDB records exactly what was written in the source texts. Inflected and compound forms appear as separate top-ranked entries: `だった` (rank 24), `には` (rank 26), `だろう` (rank 37), `けど` (rank 38), `だから` (rank 43), `ではない` (rank 89), `ことになる` (rank 167). Every other source (CEJC, RSPEER, BCCWJ_LUW, etc.) lemmatizes these to their base forms (`だ`, `けれど`, etc.), so the same underlying word occupies a completely different slot in JPDB's list.

- **Entertainment media-specific vocabulary.** Fantasy and RPG terms (`ギルド`, `ダンジョン`, `スケルトン`, `リザードマン`) and light novel tropes (`ハーレム`, `クラスメイト`) appear in JPDB's top 5k but are absent from general-language corpora.

- **Onomatopoeia and expressive words.** Words like `ぺこり`, `にこり`, `ゆらり`, `ぐるりと`, `ちょこん` are extremely common in fiction narration (describing character movements and expressions) but are rare in general or spoken Japanese.

- **Multi-morpheme phrases as single entries.** Expressions like `ことによって`, `よりによって`, `それゆえに` are stored as single vocabulary items rather than being decomposed into constituent morphemes.

## Experiments 0

[`data/ALL/___experiments0/HISTORY.md`](data/ALL/___experiments0/HISTORY.md) documents the bugs, anomalies, and design decisions discovered while consolidating frequency sources.

**Pipeline bugs fixed:**

- Quite a few sources had duplicate word entries; the pipeline now keeps the minimum (most frequent) rank.
- CEJC uses UniDic kanji lemma forms (其れ for それ, 為る for する). A bidirectional kana/kanji fallback via JPDB v2 readings was added to bridge form mismatches: kanji anchor words look up their kana reading in other sources, and kana anchor words look up any kanji form that shares the same reading.
- AOZORA_BUNKO contains zero hiragana words by design (kanji-only source) and must be excluded from coverage checks.

**Structurally incompatible sources:**
Seven sources are excluded from all coverage quality checks because their -1s reflect structural properties, not word rarity:

| Source               | Reason                                                                                                                                                                  |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AOZORA_BUNKO         | Kanji-only — all hiragana words absent by design                                                                                                                        |
| NIER                 | Single RPG — only ~10,000 unique tokens total                                                                                                                           |
| ILYASEMENOV          | Wikipedia dump with HTML entities (amp, gt, lt) as "words"                                                                                                              |
| DD2_MIGAKU_NOVELS    | Curated learner deck — only ~16,500 words, not a frequency corpus                                                                                                       |
| HERMITDAVE_2016/2018 | MeCab morpheme-split tokenization — dictionary-form verbs do not exist as tokens (い at rank #1 is a morpheme, not a word)                                              |
| JPDB                 | Anime/game register — Surface forms, not lemmas. JPDB records exactly what was written in the source texts. misses 36–42% of general vocabulary (e.g. 企業, 男性, 監督) |

**Tokenization mismatch:** Even top-1,000 common words are missing from HERMITDAVE because morpheme-split tokenization atomizes verbs — `思う` → `思` + `っ` + `て` + `い` + `る`. This is structural and cannot be fixed by lookup.

**Kana reading enrichment:** `hiragana` and `katakana` columns for each word are included per row media-anchored files (ANIME, NETFLIX, YOUTUBE) have 6–11% gaps, mostly conjugated verb forms and proper nouns not listed as dictionary headwords.

## Experiments 1

[`data/ALL/___experiments1/HISTORY.md`](data/ALL/___experiments1/HISTORY.md) documents findings from re-running coverage experiments after the dataset grew from ~35 to 60 external sources and 4 new anchors were added.

**New anchors added (10 total):**

| Anchor       | Type                                     | Words  |
| ------------ | ---------------------------------------- | ------ |
| BCCWJ_LUW    | Balanced written Japanese — LUW (NINJAL) | 25,000 |
| BCCWJ_SUW    | Balanced written Japanese — SUW (NINJAL) | 25,000 |
| CC100        | CommonCrawl web text                     | 24,605 |
| RSPEER       | Multi-source aggregated (wordfreq)       | 25,000 |
| WIKIPEDIA_V2 | Wikipedia (clean)                        | 25,000 |

**Updated EXCLUDE set (10 sources):** H_FREQ, NAROU, and VN_FREQ added to the original 7 — all use UniDic kanji lemma forms or domain-skewed tokenization that causes basic particles to score as absent.

**How to read these tables:**

- **Top-N %** (zero-missing): of the first N words in the anchor's frequency list, the percentage that appear in _every_ checked source (no `-1` rank). A high Top-500 means the most common words are universally found everywhere. The percentage naturally falls as N grows because rarer words start appearing in fewer domain-specific corpora.
- **N≤3**: words missing from _at most 3_ of the ~61 checked sources — the "broadly common" core vocabulary present in nearly all corpora.

**Zero-missing by rank band** ([`top12k/`](data/ALL/___experiments1/top12k/HISTORY.md)):

| Anchor          | Top-500 | Top-1k | Top-3k | Top-5k | Top-12k |
| --------------- | ------- | ------ | ------ | ------ | ------- |
| CC100           | 76.4%   | 65.9%  | 46.6%  | 35.2%  | 17.8%   |
| CEJC            | 76.0%   | 66.7%  | 44.1%  | 32.6%  | 16.9%   |
| BCCWJ_SUW       | 73.0%   | 67.3%  | 51.1%  | 38.1%  | 18.1%   |
| BCCWJ_LUW       | 73.4%   | 67.8%  | 47.1%  | 34.6%  | 17.2%   |
| YOUTUBE_FREQ_V3 | 60.8%   | 56.0%  | 42.3%  | 33.3%  | 17.3%   |
| NETFLIX         | 63.6%   | 58.1%  | 43.0%  | 32.9%  | 17.2%   |
| WIKIPEDIA_V2    | 51.4%   | 47.3%  | 33.9%  | 27.0%  | 15.9%   |
| ANIME_JDRAMA    | 54.2%   | 52.5%  | 40.6%  | 31.4%  | 16.9%   |
| RSPEER          | 52.4%   | 49.5%  | 38.1%  | 30.2%  | 17.1%   |
| JPDB            | 17.8%   | 11.1%  | 4.5%   | 3.0%   | 1.3%    |

**N≤3 missing sources by rank band** (top-12k slices, [`n_leq3_by_rank_band.py`](data/ALL/___experiments1/top12k/n_leq3_by_rank_band.py)):

| Anchor          | Top-500 | Top-1k | Top-3k | Top-5k | Top-12k | N≤3 @25k     |
| --------------- | ------- | ------ | ------ | ------ | ------- | ------------ |
| CEJC            | 92.2%   | 88.7%  | 72.5%  | 59.3%  | 36.4%   | —            |
| CC100           | 92.2%   | 87.0%  | 74.2%  | 63.9%  | 40.8%   | —            |
| BCCWJ_SUW       | 92.2%   | 90.6%  | 82.2%  | 72.8%  | 42.9%   | —            |
| WIKIPEDIA_V2    | 79.8%   | 75.9%  | 60.2%  | 51.1%  | 33.4%   | —            |
| BCCWJ_LUW       | 83.6%   | 81.1%  | 70.7%  | 62.2%  | 38.2%   | —            |
| YOUTUBE_FREQ_V3 | 70.8%   | 72.1%  | 65.4%  | 58.2%  | 38.0%   | —            |
| NETFLIX         | 70.8%   | 69.5%  | 61.6%  | 54.7%  | 37.1%   | —            |
| RSPEER          | 63.4%   | 64.5%  | 60.6%  | 54.2%  | 36.3%   | —            |
| ANIME_JDRAMA    | 62.2%   | 63.2%  | 58.0%  | 50.9%  | 35.2%   | —            |
| JPDB            | 25.8%   | 21.6%  | 11.9%  | 7.6%   | 3.3%    | — (excluded) |
