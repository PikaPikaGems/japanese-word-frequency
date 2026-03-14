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

HERMITDAVE (OpenSubtitles) and JPDB are missing roughly 1 in 4 of the most common Japanese words. This is not a rank-cutoff problem — these are top-1,000 words, well within any source's 25k cap.

**Root cause: tokenization mismatch.** Each corpus was processed with a different tokenizer or MeCab dictionary configuration. Different tokenizers produce different word boundaries for the same raw text:

- One source might emit `じゃない` as a single token
- Another might split it as `じゃ` + `ない`
- `してください` could be one token or three
- Compound nouns are split differently across tools

The kanji↔kana fallback (fix #3) resolves form differences for the same word unit, but **cannot bridge word-boundary differences** — `じゃない` and `じゃ` are genuinely different strings with no lookup path between them.

**Implication for the zero-missing filter:**
Asking "is this word present in every source?" is too strict. With 31 heterogeneous sources using different tokenization, even the single most common word in Japanese is likely to fail a literal string match in at least one source. Even restricting to the top 3k, top 1k, or top 500 words doesn't help — the missing rate for those bands is:

| Top-N (YOUTUBE anchor) | Zero-missing (31 sources) |
|---|---|
| Top 500 | 45.0% |
| Top 1,000 | 38.2% |
| Top 3,000 | 27.3% |
| Top 5,000 | 22.1% |
| Top 10,000 | 14.8% |

**Practical conclusion:** the right filter is not "missing from zero sources" but "missing from at most N sources." A word missing from ≤2–3 of 31 sources is much more meaningful than strict zero-missing.

---

## 8. Remaining Expected -1s (Not Bugs)

Even after all fixes, some -1s are expected and correct:

- **Source-specific vocabulary:** some words appear only in specific domains (e.g., literary words in AOZORA, web slang in NAROU) and genuinely won't appear in subtitle or spoken corpora.
- **Tokenization differences:** as described in §7, word-boundary disagreements across sources produce unavoidable mismatches that no form-lookup can fix.
- **Kana fallback is one-to-one:** the fallback maps each kanji term to its single most frequent reading. If a word has multiple valid readings and the source uses a different one, the fallback still misses.
