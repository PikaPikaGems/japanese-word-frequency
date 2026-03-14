# Data Quality Bugs and Strange Phenomena

This document records the bugs, anomalies, and design quirks discovered during consolidation of word frequency sources, and how each was addressed.

---

## 1. HERMITDAVE_2018: CSV Corruption from Unquoted Special Characters

**What happened:**
`data/RAW/___FILTERED/HERMITDAVE_2018/DATA.csv` was loading only 36 of 25,000 words during consolidation.

**Root cause:**
The original `SCRIPT.py` wrote rows manually using f-strings:
```python
f.write(f"{word},{rank}\n")
```
The HermitDave source contains `"` (double-quote) as an actual word token (it appears in Japanese subtitle transcriptions). When written unquoted into a CSV, the double-quote character broke the CSV format — every parser reading the file from that row onward treated the rest of the file as one giant quoted field.

**Fix:**
Switched to `csv.writer.writerow([word, rank])`, which properly quotes special characters. Regenerated `DATA.csv` — all 25,000 words now load correctly.

---

## 2. Duplicate Word Entries Within Single Source Files

**What happened:**
13 out of the source files had duplicate entries for the same word (e.g., そう appeared at ranks 14 and 35 in NAROU). The consolidation script was silently keeping whichever rank it read last.

**Root cause:**
Some raw frequency lists contain a word multiple times (different inflected forms merged under the same surface form, or the raw data itself has duplicates). The original `data/ALL/SCRIPT.py` simply overwrote the rank on each re-encounter:
```python
word_rank[word] = rank  # last one wins — wrong
```

**Fix:**
Keep the minimum (most frequent) rank for each word:
```python
if word not in word_rank or rank < word_rank[word]:
    word_rank[word] = rank
```
Note: lower rank number = more frequent (rank 1 = most common), so "higher on the list" = "smaller number" = more important to keep.

---

## 3. CEJC Uses UniDic Lemma Notation (Kanji Lemmas, Not Surface Hiragana)

**What happened:**
Words like それ、する、これ、あれ were showing up as -1 (absent) in almost every other source, even though they are among the most common Japanese words. Meanwhile the CEJC data had entries like 其れ (rank 36), 為る, 此れ, 彼れ.

**Root cause:**
The CEJC corpus was processed with morphological analysis (MeCab + NINJAL UniDic dictionary). UniDic normalizes words to their **canonical lemma forms**, which are often written in historical/literary kanji (其れ for それ, 為る for する, etc.). This is a standard in formal Japanese NLP — it avoids conflating different surface readings of the same underlying word.

This is not a bug in CEJC. It is an intentional design choice that causes a **form mismatch** when joining with other sources: subtitle datasets, novel corpora, and web corpora all use surface hiragana forms.

**Why both forms exist in CEJC:**
Standard competition ranking (1224 style) means each unique spelling gets its own rank. CEJC has both 其れ (rank 36, the UniDic lemma) and それ (rank 8967, the hiragana surface form as a separate entry). They are treated as distinct lexemes.

**Fix:**
Built a kanji→kana fallback mapping using JPDB v2 (`jpdb_v2.2_freq_list_2024-10-13.csv`), which contains `term` (kanji form) and `reading` (kana form) for ~278,000 entries. During consolidation, if a word is not found in a source directly, look up its kana reading and try that instead:

```python
def lookup(source, word):
    if word in source:
        return source[word]
    reading = kana_fallback.get(word)
    if reading and reading in source:
        return source[reading]
    return -1
```

For the kana fallback map itself, only the most frequent reading per kanji term is kept (lowest frequency rank number), and entries where `term == reading` are skipped (already kana).

**Result:**
其れ went from 21 missing sources → 4 missing sources after the fix.

---

## 4. AOZORA_BUNKO: Zero Hiragana Words by Design

**What happened:**
AOZORA_BUNKO had -1 for virtually every hiragana word — all common function words (は、が、の、に、を…) were absent.

**Root cause:**
AOZORA_BUNKO is a Yomitan frequency dictionary built from kanji token frequencies in the Aozora Bunko literary corpus. The source JSON was generated from kanji-heavy classical/literary texts; hiragana-only tokens were not included in the source data at all. This is a property of the source, not a processing bug.

**Implication:**
A -1 in AOZORA_BUNKO means "not a kanji word" — it has no bearing on how rare or common a word actually is. Including it in any "missing from corpus" filter would falsely flag every hiragana word as rare/absent.

**Fix:**
Excluded AOZORA_BUNKO from the -1 and RARE category filters in `filter_words.py`:
```python
EXCLUDE = {"AOZORA_BUNKO"}
check_indices = [i for i, col in enumerate(header) if i > 0 and col not in EXCLUDE]
```

---

## 5. Why "All 27,988 Words Have At Least One -1" (The Combined Effect)

Before fixing issues 1–4, every single word in the dataset appeared to have at least one -1 rank. The causes stacked:

1. HERMITDAVE_2018 only loaded 36 words (corruption) → nearly everything was -1 in that source
2. Duplicate handling was wrong → some words got a worse rank than they should
3. CEJC kanji lemmas had no match in hiragana-based sources → even top-10 words like 其れ showed as absent
4. AOZORA_BUNKO had zero hiragana entries → all function words flagged

After all fixes, the filter produces a much smaller, meaningful set of words that are genuinely absent or rare across sources.

---

## 6. Three More Sources Excluded: NIER, ILYASEMENOV, DD2_MIGAKU_NOVELS

After investigating why ~98% of words still had at least one -1 even after fixes 1–5, three more sources were found to be structurally unsuitable for coverage checks.

**NIER** — Only **10,077 unique words** in the entire dataset. NieR: Automata is a single RPG. Its script simply doesn't contain most common Japanese words. There is no "top 25k" — the game only has ~10k unique tokens. Its -1s mean "not in this game," not "rare in Japanese."

**ILYASEMENOV** — Has 25,000 entries but is a raw Wikipedia dump that was never properly cleaned. Top entries: は (#1), また (#2), **概要 (#3)** (Wikipedia section header), しかし (#4), なお (#5), **the (#7)**, 経歴 (#9), **amp (#14)**, **gt (#15)**, **lt (#18)**. HTML entities (`&amp;`, `&gt;`, `&lt;`) are treated as words. The vocabulary is entirely biased toward formal biographical Wikipedia articles and has nothing to do with conversational Japanese.

**DD2_MIGAKU_NOVELS** — Only **16,469 unique words**. This is a curated Anki/Migaku deck for novel vocabulary, designed for learners. It is not a comprehensive frequency list.

**Updated exclusion set:**
```python
EXCLUDE = {
    "AOZORA_BUNKO",       # kanji-only — no hiragana words by design
    "NIER",               # single game, only ~10k words total
    "ILYASEMENOV",        # Wikipedia dump with HTML entities, wrong domain
    "DD2_MIGAKU_NOVELS",  # curated learner deck, only ~16k words
}
```

After excluding all four, zero-missing words jumped from 330 → ~1,341–1,975 depending on anchor.

---

## 7. The Tokenization Mismatch Problem (Why Even Top-1000 Words Have -1s)

After all fixes and all four exclusions, even the top 1,000 most common words are still missing from some sources. Specifically, looking at the top-1,000 YOUTUBE_FREQ_V3 words against the remaining 31 sources:

| Source | Missing from top-1k |
|---|---|
| HERMITDAVE_2016 | **24.8%** |
| HERMITDAVE_2018 | **24.4%** |
| JPDB | **24.4%** |
| H_FREQ | 17.8% |
| DD2_MORPHMAN_* | ~16% each |

HERMITDAVE (OpenSubtitles) and JPDB are missing roughly 1 in 4 of the most common Japanese words. This is not a rank-cutoff problem — these are top-1,000 words, well within any source's 25k cap. The missing words were verified: `思う` (#30), `見る` (#56), `できる` (#50), `言う` (#40), `食べる` (#154), `わかる` (#132) — all extremely common verbs — are absent.

**Root cause: morpheme tokenization vs. lemma tokenization.**

The key evidence is HERMITDAVE's actual top entries:

```
HERMITDAVE rank #1:  い    ← individual hiragana character
HERMITDAVE rank #21: う    ← individual hiragana character
HERMITDAVE rank #36: ろ    ← individual hiragana character
```

Compare to YOUTUBE:

```
YOUTUBE rank #11: する   ← full verb (dictionary/lemma form)
YOUTUBE rank #16: いう   ← full verb
YOUTUBE rank #56: 見る   ← full verb
```

HERMITDAVE ran MeCab (or similar) in **morpheme mode** with IPAdic. In this mode, the analyzer splits verbs into their constituent morphemes:

- `思っている` → `思` + `っ` + `て` + `い` + `る`
- `できます` → `でき` + `ます`
- `見ました` → `見` + `まし` + `た`

The token `い` at rank #1 in HERMITDAVE is the auxiliary `い` that appears in every progressive/existential form (`している`, `いる`, `ている`, etc.). It is not the interjection — it is a morpheme.

As a result, the dictionary form `思う` simply **does not exist as a token** in HERMITDAVE. Its frequency is split across `思`, `っ`, `て`, `い`, `る` separately, each too low to rank in the top-25k on its own.

YOUTUBE_FREQ_V3 (and most modern learner-oriented sources) use a **lemmatizing tokenizer** that normalizes inflected forms to the dictionary entry: all forms of 思う collapse into a single `思う` entry with their combined frequency.

This was confirmed by checking whether conjugated forms exist in HERMITDAVE as a fallback:
- `いる` (YOUTUBE #20): NOT in HERMITDAVE → split as `い` + `る`
- `思う` (YOUTUBE #30): NOT in HERMITDAVE, conjugations also absent → split at morpheme level
- `でき` (morpheme stem): rank 77 in HERMITDAVE ← the stem of `できる`
- `いた` (past of いる): rank 1,036 in HERMITDAVE ← one conjugated form, but frequency is spread thin

**Why restricting to top 3k or top 1k doesn't help:**

The problem is not about which words are "common enough" — even the top-500 most frequent Japanese words by YOUTUBE ranking have this issue. The problem is structural: a lemma-form word will never match a morpheme-split corpus regardless of its rank.

| Top-N (YOUTUBE anchor) | Zero-missing across 31 sources |
|---|---|
| Top 500 | 45.0% |
| Top 1,000 | 38.2% |
| Top 3,000 | 27.3% |
| Top 5,000 | 22.1% |
| Top 10,000 | 14.8% |

Even for the top-500 most common words, only 45% have zero -1s because multiple sources (HERMITDAVE_2016, HERMITDAVE_2018, and several DD2_MORPHMAN variants) will always miss lemma-form verbs.

**Practical conclusion: use a missing-source threshold, not zero-missing.**

Since 2–3 sources (specifically the HERMITDAVE pair and some DD2_MORPHMAN variants) will structurally miss lemma-form verbs, the right filter is "missing from at most N sources" rather than "missing from zero." See §9 for the recommended algorithm.

---

## 8. Remaining Expected -1s (Not Bugs)

Even after all fixes, some -1s are expected and correct:

- **Source-specific vocabulary:** some words appear only in specific domains (e.g., literary words in AOZORA, web slang in NAROU) and genuinely won't appear in subtitle or spoken corpora.
- **Morpheme vs. lemma tokenization:** as described in §7, HERMITDAVE and similar sources will always miss dictionary-form verbs because the underlying text was tokenized at morpheme level.
- **Kana fallback is one-to-one:** the fallback maps each kanji term to its single most frequent reading. If a word has multiple valid readings and the source uses a different one, the fallback still misses.

---

## 9. The Excluded Sources: Why Each One Is Structurally Incompatible

These six sources are excluded from all coverage quality checks. Each is excluded for a distinct, evidence-backed reason — not poor data quality in the general sense, but a fundamental mismatch with the rest of the corpus that makes their -1s meaningless as a signal of word rarity.

---

### AOZORA_BUNKO

**Reason:** Kanji-only source — structurally contains zero hiragana-only words.

**Evidence:** Inspection of the raw Yomitan JSON confirms the source contains only kanji-form tokens derived from the Aozora Bunko literary corpus. Function words (は、が、の、に、を、て…) that are written exclusively in hiragana are entirely absent. This is not a processing error; the source JSON was built from kanji token frequencies and hiragana-only tokens were never included.

A -1 from AOZORA_BUNKO means "this word is not written in kanji," not "this word is rare." Every hiragana word — including the most common words in Japanese — gets -1. Including it in quality checks would falsely flag all function words as absent.

---

### NIER

**Reason:** Single video game with only ~10,000 unique tokens — far below the 25,000 source cap.

**Evidence:** `wc -l data/RAW/___FILTERED/NIER/DATA.csv` → **10,078 lines** (10,077 words + header). NieR: Automata is one RPG. Its entire script simply does not contain most Japanese words. A -1 here means "not used in this game's dialogue," which is meaningless for general frequency ranking.

---

### ILYASEMENOV

**Reason:** Raw Wikipedia dump — contains HTML entities as "words" and is domain-locked to formal biographical writing.

**Evidence:** Actual top entries in `DATA.csv`:

```
#1  は        (fine)
#2  また      (also — formal writing marker)
#3  概要      (overview — Wikipedia section header)
#7  the       (English word)
#9  経歴      (career history — Wikipedia infobox term)
#14 amp       (HTML entity &amp;)
#15 gt        (HTML entity &gt;)
#18 lt        (HTML entity &lt;)
```

HTML artifacts (`amp`, `gt`, `lt`) are counted as vocabulary. The top non-particle words are Wikipedia-specific (`概要`, `経歴`, `来歴`, `人物`) — these are recurring section headers in Japanese Wikipedia biographical articles, not general vocabulary. Conversational words, particles in context, and spoken-Japanese vocabulary are essentially absent.

---

### DD2_MIGAKU_NOVELS

**Reason:** Curated learner deck — only ~16,000 words, not a comprehensive frequency list.

**Evidence:** `wc -l data/RAW/___FILTERED/DD2_MIGAKU_NOVELS/DATA.csv` → **16,470 lines** (16,469 words + header). This is a Migaku/Anki vocabulary deck designed to help Japanese learners study novel vocabulary. It was never intended to be an exhaustive frequency corpus. Its coverage ceiling of ~16k words means the bottom ~12k of any 25k anchor list will always be -1.

---

### HERMITDAVE_2016 and HERMITDAVE_2018

**Reason:** MeCab morpheme-split tokenization — dictionary-form verbs and adjectives do not exist as tokens in these sources.

**Evidence:** The actual top entries reveal the tokenization level:

```
HERMITDAVE rank #1:  い    ← morpheme, not word
HERMITDAVE rank #21: う    ← morpheme (volitional suffix)
HERMITDAVE rank #36: ろ    ← morpheme (imperative suffix)
HERMITDAVE rank #77: でき  ← stem of できる, not the verb itself
```

`い` at rank #1 is not the word "i" — it is the auxiliary morpheme appearing in every progressive form (`している`, `いる`, `ている`). MeCab with IPAdic in morpheme mode splits `思っている` → `思` + `っ` + `て` + `い` + `る`, so each morpheme accumulates frequency separately.

Consequence: the dictionary forms `思う`, `見る`, `できる`, `いる`, `食べる` simply do not exist as tokens. Their frequency is atomized. Cross-checked: none of these words appear anywhere in HERMITDAVE's word list, not even as conjugated forms (`思います`, `食べた`, etc. also absent). This was verified by string-searching all 25,000 HERMITDAVE entries.

In contrast, YOUTUBE_FREQ_V3 (and most other sources) use a lemmatizing tokenizer that collapses all inflections of 思う into a single entry, which reaches rank #30.

**Missing rate for top-1,000 YOUTUBE words before exclusion:**
- HERMITDAVE_2016: **24.8%**
- HERMITDAVE_2018: **24.4%**

These are not domain gaps — they are tokenization artifacts. No lookup or fallback can bridge morpheme-split tokens to lemma-form entries.

---

### Impact of the Full Exclusion Set

Each source added to EXCLUDE improves the zero-missing count because words that were falsely failing (due to structural incompatibility, not genuine absence) are no longer penalized. The progression:

| Exclusion set | Zero-missing (CEJC anchor) | Zero-missing (YOUTUBE anchor) |
|---|---|---|
| None | 330 | — |
| + AOZORA_BUNKO | ~330 (minimal change) | — |
| + NIER, ILYASEMENOV, DD2_MIGAKU_NOVELS | 1,341 | 1,975 |
| + HERMITDAVE_2016, HERMITDAVE_2018 | **1,828** | **2,708** |

Adding the two HERMITDAVE sources improved zero-missing by ~36–37% relative to the 4-source exclusion set.

Zero-missing counts by anchor after all 6 exclusions (29 remaining sources checked):

| Anchor | Total words | Zero-missing | % |
|---|---|---|---|
| CEJC | 27,988 | 1,828 | 6.5% |
| JPDB | 24,231 | 1,642 | 6.8% |
| YOUTUBE_FREQ_V3 | 30,000 | 2,708 | 9.0% |
| ANIME_JDRAMA | 25,000 | 2,643 | 10.6% |
| NETFLIX | 25,000 | 2,611 | 10.4% |

---

## 10. Recommended Algorithm: Threshold-Based Coverage Filter

Rather than requiring a word to appear in all remaining sources (which ~85–93% of words still fail), filter by how many sources it is missing from.

**Algorithm:**

```
EXCLUDE = {AOZORA_BUNKO, NIER, ILYASEMENOV, DD2_MIGAKU_NOVELS, HERMITDAVE_2016, HERMITDAVE_2018}

for each word:
    missing_count = count of -1s across all source columns not in EXCLUDE

filter_words_at_threshold(N):
    return words where missing_count ≤ N
```

**Choosing N** (29 sources remain after exclusion):

| N | Meaning |
|---|---|
| 0 | Present in all 29 checked sources — maximum strictness |
| 3 | Tolerates a few domain-specific sources missing a word |
| 5 | Good general-purpose threshold |
| 10 | Permissive — keeps most common vocabulary |

**No weighting is needed.** A simple count is transparent and reproducible. If you want to be more principled, you could split sources into tiers (broad corpus vs. narrow domain) and require coverage in all broad-corpus sources while tolerating misses in narrow ones — but that adds complexity without clear benefit at this stage.

To produce these filtered lists, run `analyze_coverage.py` (which already computes `missing_count` per word in the distribution table) and filter the resulting `consolidated_anchor_*.csv` at the chosen threshold.

---

## 8. Remaining Expected -1s (Not Bugs)

Even after all fixes, some -1s are expected and correct:

- **Source-specific vocabulary:** some words appear only in specific domains (e.g., literary words in AOZORA, web slang in NAROU) and genuinely won't appear in subtitle or spoken corpora.
- **Tokenization differences:** as described in §7, word-boundary disagreements across sources produce unavoidable mismatches that no form-lookup can fix.
- **Kana fallback is one-to-one:** the fallback maps each kanji term to its single most frequent reading. If a word has multiple valid readings and the source uses a different one, the fallback still misses.
