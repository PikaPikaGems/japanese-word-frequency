# Data Quality Experiments 0

This document records the bugs, anomalies, design quirks, and coverage experiments from consolidating word frequency sources. Sections §1–§8 cover pipeline bugs and fixes. §9–§13 cover coverage analysis experiments and findings. This is a snapshot of the past. The directory and file names as well as the actual structure of the data may have already evolved overtime. However, this is important documentation as it highlights the quality and nature of the datasets found in this repository.

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
Built a bidirectional kana/kanji fallback mapping using JPDB v2 (`jpdb_v2.2_freq_list_2024-10-13.csv`), which contains `term` (kanji form) and `reading` (kana form) for ~278,000 entries. During consolidation, if a word is not found in a source directly, the lookup tries both directions:

```python
def lookup(source, word):
    if word in source:
        return source[word]
    # kanji word → try its kana reading in source
    kana = kana_fallback.get(word)
    if kana and kana in source:
        return source[kana]
    # kana word → try any kanji form that reads as this kana in source
    for kanji in kana_to_kanji.get(word, []):
        if kanji in source:
            return source[kanji]
    return -1
```

`kana_fallback` maps each kanji term to its most frequent reading (lowest frequency rank number); entries where `term == reading` are skipped (already kana). `kana_to_kanji` is the reverse map (kana → list of kanji forms). This logic lives in `utils/lookup.py` (`JapaneseLookup` class) and is shared across all anchor generation scripts.

The bidirectional lookup resolved **4,703 additional rank lookups** (0.35% of all 1,343,424 cells) in the CEJC anchor compared to a kanji→kana-only fallback. The kana→kanji direction helps when a source stores a word in kanji form but the anchor word is in kana.

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

| Source          | Missing from top-1k |
| --------------- | ------------------- |
| HERMITDAVE_2016 | **24.8%**           |
| HERMITDAVE_2018 | **24.4%**           |
| JPDB            | **24.4%**           |
| H_FREQ          | 17.8%               |
| DD2*MORPHMAN*\* | ~16% each           |

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
| ---------------------- | ------------------------------ |
| Top 500                | 45.0%                          |
| Top 1,000              | 38.2%                          |
| Top 3,000              | 27.3%                          |
| Top 5,000              | 22.1%                          |
| Top 10,000             | 14.8%                          |

Even for the top-500 most common words, only 45% have zero -1s because multiple sources (HERMITDAVE_2016, HERMITDAVE_2018, and several DD2_MORPHMAN variants) will always miss lemma-form verbs.

**Practical conclusion: use a missing-source threshold, not zero-missing.**

Since 2–3 sources (specifically the HERMITDAVE pair and some DD2_MORPHMAN variants) will structurally miss lemma-form verbs, the right filter is "missing from at most N sources" rather than "missing from zero." See §9 for the recommended algorithm.

---

## 8. Remaining Expected -1s (Not Bugs)

Even after all fixes, some -1s are expected and correct:

- **Source-specific vocabulary:** some words appear only in specific domains (e.g., literary words in AOZORA, web slang in NAROU) and genuinely won't appear in subtitle or spoken corpora.
- **Morpheme vs. lemma tokenization:** as described in §7, HERMITDAVE and similar sources will always miss dictionary-form verbs because the underlying text was tokenized at morpheme level.
- **Kana fallback is one-to-one (kanji→kana direction):** the fallback maps each kanji term to its single most frequent reading. If a word has multiple valid readings and the source uses a different one, the fallback still misses. The reverse kana→kanji direction is also available (see §3 fix) but covers only exact reading matches.

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

| Exclusion set                          | Zero-missing (CEJC anchor) | Zero-missing (YOUTUBE anchor) |
| -------------------------------------- | -------------------------- | ----------------------------- |
| None                                   | 330                        | —                             |
| + AOZORA_BUNKO                         | ~330 (minimal change)      | —                             |
| + NIER, ILYASEMENOV, DD2_MIGAKU_NOVELS | 1,341                      | 1,975                         |
| + HERMITDAVE_2016, HERMITDAVE_2018     | 1,828                      | 2,708                         |
| + JPDB                                 | **3,478**                  | **4,463**                     |

Adding JPDB improved zero-missing by ~65–90% relative to the 6-source exclusion set (see §11).

Zero-missing counts by anchor after all 7 exclusions (28 remaining sources checked):

| Anchor          | Total words | Zero-missing | %     |
| --------------- | ----------- | ------------ | ----- |
| CEJC            | 27,988      | 3,353        | 12.4% |
| YOUTUBE_FREQ_V3 | 30,000      | 4,463        | 14.9% |
| ANIME_JDRAMA    | 25,000      | 4,377        | 17.5% |
| NETFLIX         | 25,000      | 4,355        | 17.4% |

---

## 10. Recommended Algorithm: Threshold-Based Coverage Filter

Rather than requiring a word to appear in all remaining sources (which ~85–93% of words still fail), filter by how many sources it is missing from.

**Algorithm:**

```
EXCLUDE = {AOZORA_BUNKO, NIER, ILYASEMENOV, DD2_MIGAKU_NOVELS, HERMITDAVE_2016, HERMITDAVE_2018, JPDB}

for each word:
    missing_count = count of -1s across all source columns not in EXCLUDE

filter_words_at_threshold(N):
    return words where missing_count ≤ N
```

**Choosing N** (28 sources remain after exclusion):

| N   | Meaning                                                |
| --- | ------------------------------------------------------ |
| 0   | Present in all 28 checked sources — maximum strictness |
| 3   | Tolerates a few domain-specific sources missing a word |
| 5   | Good general-purpose threshold                         |
| 10  | Permissive — keeps most common vocabulary              |

**No weighting is needed.** A simple count is transparent and reproducible. If you want to be more principled, you could split sources into tiers (broad corpus vs. narrow domain) and require coverage in all broad-corpus sources while tolerating misses in narrow ones — but that adds complexity without clear benefit at this stage.

To produce these filtered lists, run `analyze_coverage.py` (which already computes `missing_count` per word in the distribution table) and filter the resulting `consolidated_anchor_*.csv` at the chosen threshold.

---

## 11. JPDB Excluded: Anime/Game Corpus Misses General Vocabulary

After applying the 6-source exclusion set, JPDB was the single largest non-excluded culprit: 36–42% of "high-frequency" words (those present in ≤2 other sources as missing) were absent from JPDB depending on anchor.

**Initial hypothesis:** JPDB has 25,000 words — very generous. If a word is common enough to appear in 27+ of 29 other sources, it should surely be in JPDB's top 25k.

**Investigation:** A threshold analysis was run to find high-frequency words (missing from ≤2 checked sources) that were absent in JPDB. Sample of words absent in JPDB but present in 27–29 other sources:

- 男性 (man/male) — YOUTUBE rank 1,100
- 企業 (company/enterprise) — YOUTUBE rank 432
- 監督 (director/coach) — YOUTUBE rank 1,808
- 携帯 (mobile phone) — YOUTUBE rank 1,817
- 妖怪 (yokai/monster) — YOUTUBE rank 8,020
- 不満 (dissatisfaction) — YOUTUBE rank 3,710

These are all words any fluent Japanese speaker uses, common in real conversation, YouTube, dramas, and general writing.

**Root cause confirmed:** The JPDB Yomitan source (Shoui/MarvNC) ranks these words by their frequency in JPDB's anime/game/manga/visual novel corpus — a completely different register from real-world Japanese. Checked directly against the raw Yomitan dictionary:

```
男性 (だんせい)   → Yomitan rank 180,271   (well beyond top 25k)
妖怪 (ようかい)   → Yomitan rank 89,185    (beyond top 25k)
企業 (きぎょう)   → Yomitan rank 183,459  ❌ (explicitly not in corpus)
監督 (かんとく)   → Yomitan rank 122,398   (beyond top 25k)
携帯 (けいたい)   → Yomitan rank 122,775   (beyond top 25k)
不満 (ふまん)    → Yomitan rank 95,422    (beyond top 25k)
```

The kana lookup is working correctly — `男性 → だんせい` resolves fine. These kana forms are simply not in JPDB's top 25k because the words themselves are rare in anime/game scripts. Anime characters say 俺 or a character's name, not 男性. 企業 is explicitly flagged absent — corporate vocabulary does not appear in the JPDB corpus.

**Why this is structurally different from NAROU or NOVELS:** Other domain-specific sources (NAROU = light novels, NOVELS = literary fiction) also cover a narrow domain yet miss only ~0.5% of high-frequency words. JPDB misses 36–42% because its source material — anime dialogue, visual novel scripts, game text — is a spoken/fictional register that systematically avoids the formal, real-world vocabulary used everywhere else.

**Impact of excluding JPDB:**

| Anchor          | Zero-missing (6 excl) | Zero-missing (7 excl, +JPDB) | Change |
| --------------- | --------------------- | ---------------------------- | ------ |
| ANIME_JDRAMA    | 2,643 (10.6%)         | 4,377 (17.5%)                | +65%   |
| CEJC            | 1,828 (6.5%)          | 3,478 (12.4%)                | +90%   |
| NETFLIX         | 2,611 (10.4%)         | 4,355 (17.4%)                | +67%   |
| YOUTUBE_FREQ_V3 | 2,708 (9.0%)          | 4,463 (14.9%)                | +66%   |

Adding JPDB to EXCLUDE roughly doubles the zero-missing count, consistent with the HERMITDAVE impact. 28 sources remain after the full 7-source exclusion set.

---

## 12. Why Zero-Missing Is Still Low (14–18%) After 7 Exclusions — Not a Bug

After excluding 7 structurally broken sources, zero-missing across all anchors was still only 14.9–17.5%. This prompted a deeper investigation to confirm whether a logic error remained.

### Investigation: Top-500 Failures

For the YOUTUBE anchor, 150 of the top-500 words still failed zero-missing. Tracing which source caused each failure:

```
H_FREQ               responsible for 89 of 150 failures in top-500
NAROU                responsible for 80
VN_FREQ              responsible for 77
DD2_MORPHMAN_NETFLIX responsible for 58
DD2_MORPHMAN_SHONEN  responsible for 54
DD2_MORPHMAN_SOL     responsible for 54
...
```

Sample top-500 words failing and why:

```
が   (YT rank 7)   missing from: H_FREQ
を   (YT rank 8)   missing from: DD2_YOMICHAN_NOVELS, H_FREQ, INNOCENT_RANKED, NAROU, VN_FREQ
ん   (YT rank 19)  missing from: DD2_MORPHMAN_NETFLIX, DD2_MORPHMAN_SHONEN, DD2_MORPHMAN_SOL, H_FREQ, NAROU, VN_FREQ
けど (YT rank 32)  missing from: CEJC_rank, DD2_MORPHMAN_NETFLIX, DD2_MORPHMAN_SHONEN, DD2_MORPHMAN_SOL, H_FREQ, NAROU, VN_FREQ
```

Basic particles like が and を missing from sources with 25k words — clearly structural problems remain. Three sources were identified:

### H_FREQ: Adult Content Corpus

Actual top entries in DATA.csv:

```
rank=1  私
rank=2  おちんちん
rank=3  言う
rank=5  射精
rank=6  気持ちいい
```

H_FREQ is an adult content frequency list. All basic particles (が, を, は, に, の, で, と) are absent. Its -1s are meaningless for general Japanese vocabulary assessment.

### NAROU and VN_FREQ: UniDic Kanji Lemma Forms (Again)

Top entries in both:

```
NAROU rank=1  為る    (suru — UniDic lemma)
NAROU rank=2  居る    (iru  — UniDic lemma)
NAROU rank=6  事      (koto)
NAROU rank=8  其れ    (sore — UniDic lemma)

VN_FREQ rank=1  為る
VN_FREQ rank=3  無い
VN_FREQ rank=8  其れ
```

Same UniDic lemma tokenization as CEJC (§3), but without the kana fallback bridging it. Standalone particles (が, を, は, の) have no kanji form, so the kana→kanji fallback cannot resolve them. Both sources have を=-1 (completely absent) and の at rank 11,000+ (vs rank 1–3 in normal sources).

### DD2_MORPHMAN Sources: Apparent Problem, Actually Fine

DD2_MORPHMAN_SHONEN/SOL/NETFLIX appeared suspicious: a raw scan of DATA.csv found が at ranks 10,127–21,634. This looked like it could be a MorphMan study-priority ranking problem similar to HERMITDAVE.

**Investigation revealed this was a false alarm.** The DATA.csv files contain duplicate entries for the same word (one word appearing at multiple ranks due to UniDic POS sub-classifications). A raw `{word: rank}` dict scan (last-entry-wins) returns the wrong rank. `make_anchored.py` correctly deduplicates by keeping the minimum rank per word. In the consolidated output, DD2_MORPHMAN_SHONEN has:

```
が = rank 8   ✓
を = rank 7   ✓
は = rank 3   ✓
```

These are correct. The failures from DD2_MORPHMAN_SHONEN/SOL/NETFLIX in the top-500 (54–58 each) are due to colloquial forms like ん and けど, which these genre-specific sources legitimately do not contain. **No fix needed.**

### Impact of Excluding H_FREQ, NAROU, VN_FREQ

| Anchor          | 7 excl (current) | 10 excl (+H_FREQ, NAROU, VN_FREQ) | Change |
| --------------- | ---------------- | --------------------------------- | ------ |
| ANIME_JDRAMA    | 4,377 (17.5%)    | 4,675 (18.7%)                     | +1.2%  |
| CEJC            | 3,478 (12.4%)    | 3,765 (13.5%)                     | +1.1%  |
| NETFLIX         | 4,355 (17.4%)    | 4,657 (18.6%)                     | +1.2%  |
| YOUTUBE_FREQ_V3 | 4,463 (14.9%)    | 4,755 (15.8%)                     | +0.9%  |

Only ~1% improvement despite three clearly broken sources. The failures from H_FREQ, NAROU, and VN_FREQ largely overlap — words they fail are already failing from other sources too. This points to the real explanation.

### The Real Reason: Zero-Missing Is Mathematically Bounded Low

Individual coverage rates across the 28 checked YOUTUBE sources range from 39% (DD2_MORPHMAN_SOL) to 68% (CC100). If these were independent:

```
Expected zero-missing (independent) = product of all coverage rates ≈ 0.000001%
Actual zero-missing                 = 14.9%
```

The 14.9% actual figure is far above the independent-source expectation — because sources are correlated (common words appear in many sources simultaneously). But the ceiling is set by the _worst_ sources in the checked set:

```
CC100                  68.1% coverage  ← best
YOUTUBE_FREQ           62.7%
...
DD2_MORPHMAN_NETFLIX   42.7%
DD2_MORPHMAN_SHONEN    39.7%
DD2_MORPHMAN_SOL       39.0%  ← worst
```

With DD2_MORPHMAN_SOL covering only 39% of YouTube words, at most 39% of words can ever achieve zero-missing. Checking what zero-missing looks like if we only check the N best sources:

```
Top 5 sources only  → 39.2% zero-missing
Top 10 sources only → 28.2% zero-missing
All 28 sources      → 14.9% zero-missing
```

Each additional source reduces the count. This is not a bug — it is the correct answer to "how many words appear in every single domain we have data for." That answer is ~4,400–4,700 words. All other words fall along a spectrum of cross-domain coverage.

### Conclusion

Zero-missing is not a useful primary metric with 28 domain-specific sources. The threshold-based approach (§10) is the correct tool: `missing_count ≤ N` identifies broadly common words without requiring perfect coverage across every narrow-domain source.

H_FREQ, NAROU, and VN_FREQ have genuine structural problems (adult content, UniDic lemma artifacts) and should eventually be added to EXCLUDE. Their ~1% numerical impact is small only because their failures overlap with other sources — the false-negative pollution they introduce to `missing_count` remains real.

---

## 13. Coverage Experiments: Rank-Band Analysis and N≤3 Threshold

### Experiment 1: Does restricting to top-5k or top-10k words improve coverage?

Yes — dramatically. The rank-band zero-missing breakdown (YOUTUBE_FREQ_V3 anchor, 28 checked sources) shows:

| Top-N words | Zero-missing | %     |
| ----------- | ------------ | ----- |
| Top 500     | 351          | 70.2% |
| Top 1,000   | 678          | 67.8% |
| Top 3,000   | 1,759        | 58.6% |
| Top 5,000   | 2,523        | 50.5% |
| Top 10,000  | 3,500        | 35.0% |
| All 30,000  | 4,463        | 14.9% |

The most common 500–1,000 words achieve 68–70% zero-missing across 28 domain-specific sources. This makes intuitive sense: basic particles, core verbs, and high-frequency nouns appear in essentially every corpus regardless of domain. The drop from 70% at top-500 to 15% at the full 30,000 reflects how quickly vocabulary diverges by domain as words become rarer.

**Implication:** If the goal is a "core vocabulary" list for learners, restricting to top-5k words and requiring zero-missing gives ~2,500 genuinely universal words. At top-1k, nearly 68% pass with zero-missing — a much cleaner set than the full-list 15%.

### Experiment 2: N≤3 threshold (missing from at most 3 sources)

The existing `threshold_analysis.py` was updated from `THRESHOLD = 2` to `THRESHOLD = 3` and re-run. Results (`data/ALL/threshold_analysis_N3.md`):

| Anchor          | High-freq (≤2 missing) | %     | High-freq (≤3 missing) | %     | Δ words |
| --------------- | ---------------------- | ----- | ---------------------- | ----- | ------- |
| ANIME_JDRAMA    | 6,821                  | 27.3% | 7,721                  | 30.9% | +900    |
| CEJC            | 5,303                  | 18.9% | 6,047                  | 21.6% | +744    |
| JPDB            | 2,544                  | 10.5% | 2,920                  | 12.1% | +376    |
| NETFLIX         | 6,786                  | 27.1% | 7,712                  | 30.8% | +926    |
| YOUTUBE_FREQ_V3 | 6,914                  | 23.0% | 7,834                  | 26.1% | +920    |

Going from N≤2 to N≤3 adds ~750–930 words per anchor (except JPDB which is domain-constrained). The top non-excluded culprit across all anchors at N≤3 is **ADNO** (12–15% of high-frequency words absent), followed by **H_FREQ** (5–9%) and **CEJC** (5–7%).

**Recommended threshold:** N≤3 is the practical working threshold. It tolerates the handful of domain-specific sources that legitimately skip certain vocabulary (e.g., H_FREQ's adult content register, NAROU's genre vocabulary) without setting an impossibly strict bar.

Filtered CSVs for each anchor are written to `data/ALL/threshold_3_anchor_{NAME}.csv`.

---

## 14. Kana Reading Enrichment: Coverage and Gaps

`hiragana` and `katakana` columns were added to every `categorized.csv` and `consolidated.csv` under `data/ALL/*/`. This section documents the sources used, the coverage achieved, and the nature of the remaining gaps.

### Sources

Two sources were combined into a single lookup of ~280,000 entries:

| Source                                           | Format                               | Reading script | Priority |
| ------------------------------------------------ | ------------------------------------ | -------------- | -------- |
| `data/JPDBV2/jpdb_v2.2_freq_list_2024-10-13.csv` | TSV, `term` + `reading` columns      | hiragana       | primary  |
| `data/CEJC/2_cejc_frequencylist_suw_token.tsv`   | TSV, `語彙素` + `語彙素読み` columns | katakana       | fallback |

JPDBV2 provides hiragana readings; CEJC provides katakana readings (UniDic `語彙素読み`). For each word, a hiragana and katakana form are derived from whichever source has a match, using the conversion functions in `utils/kana.py` (pure Unicode offset arithmetic, no external library).

### Pure-kana back-fill

After the lookup pass, a second pass filled readings for words consisting entirely of hiragana and/or katakana characters (e.g. `う`, `あぁ`, `ンダホ`). For such words the reading is the word itself:

```
hiragana = katakana_to_hiragana(word)
katakana  = hiragana_to_katakana(word)
```

Words filled by this pass per file:

| Anchor          | Pure-kana gaps filled |
| --------------- | --------------------- |
| JPDB            | 41                    |
| NETFLIX         | 317                   |
| ANIME_JDRAMA    | 353                   |
| YOUTUBE_FREQ_V3 | 1,427                 |
| CEJC            | 0 (already complete)  |

### Coverage after both passes

| Anchor          | Total words | Missing reading | % missing |
| --------------- | ----------- | --------------- | --------- |
| CEJC            | 27,987      | 0               | 0.0%      |
| JPDB            | 24,231      | 0               | 0.0%      |
| NETFLIX         | 25,000      | 1,728           | 6.9%      |
| YOUTUBE_FREQ_V3 | 30,000      | 1,935           | 6.5%      |
| ANIME_JDRAMA    | 25,000      | 2,636           | 10.5%     |

CEJC and JPDB-anchored files reach 100% coverage. The media-anchored files (ANIME, NETFLIX, YOUTUBE) have 6–11% gaps.

### Nature of the remaining gaps

All missing words contain Japanese characters — non-Japanese tokens are essentially absent (only `々`, the kanji repetition mark, is unclassifiable; 1 token across all files). The gap breaks down into two categories:

**Conjugated / potential verb forms (~majority):** Words like `会える`, `行ける`, `使える`, `話せる`, `待てる`, `いただける` — potential/potential-passive verb forms — are common in spoken and subtitle corpora but not listed as headwords in either JPDBV2 or CEJC's lemma-based vocabulary lists. Both sources index dictionary/lemma forms only.

**Proper nouns and names:** Anime character names (`悟`, `のび太`), Japanese surnames (`宮近`, `深澤`, `中村`, `井上`, `阿部`), and some proper place/product names account for most of the remainder, particularly in the YOUTUBE file which contains a lot of creator/talent names.

**Implication:** The gaps are structural — they reflect the difference between a lemma-based dictionary and a surface-form subtitle/web corpus. A MeCab-based reading lookup could resolve the conjugated verb forms; a proper noun dictionary would be needed for the names. Both are out of scope for the current pipeline.

### Handling unfixable words

All remaining missing readings are filled with `"-"`. Final counts:

| Anchor          | Total words | Filled with "-" | %     |
| --------------- | ----------- | --------------- | ----- |
| CEJC            | 27,988      | 1               | 0.0%  |
| JPDB            | 24,231      | 0               | 0.0%  |
| NETFLIX         | 25,000      | 1,728           | 6.9%  |
| YOUTUBE_FREQ_V3 | 30,000      | 1,935           | 6.5%  |
| ANIME_JDRAMA    | 25,000      | 2,636           | 10.5% |

The 1 entry in CEJC is a blank word token (empty string) that was present in the source data. No file has any non-Japanese-character words among the unfixable set — all 8,300 "-" entries across the 5 anchors are kanji-containing words whose reading is simply not in either reference source.

### Why JPDB is primary and CEJC is fallback

The ordering may seem counterintuitive given that this is primarily a CEJC-anchored pipeline. The reason is **vocabulary size**: JPDB v2 contains ~497k entries, while CEJC covers only ~27,988 unique words. The `get_reading()` function is used across all five anchor variants (CEJC, JPDB, ANIME_JDRAMA, NETFLIX, YOUTUBE_FREQ_V3). For non-CEJC anchors, the word lists contain many words outside CEJC's 27k vocabulary. Using JPDB as primary means the larger source answers first, leaving CEJC to catch only what JPDB misses.

**Does swapping the order change the output?**

For the CEJC-anchored files: no difference. Both sources reach 100% coverage for CEJC words, and for any word present in both sources the readings agree on pronunciation — the only representation difference is hiragana (JPDB) vs katakana (CEJC), which the conversion functions handle losslessly.

For non-CEJC anchors (ANIME_JDRAMA, NETFLIX, YOUTUBE_FREQ_V3): swapping would produce the same final readings but with more first-pass misses, since CEJC's smaller vocabulary would fail to match many anchor words that then fall through to JPDB anyway. The output would be identical; only the lookup path changes.

One theoretical edge case: polysemous kanji with multiple valid readings (e.g., 上 → うえ / かみ / じょう). JPDB picks the reading with the lowest frequency rank in its entertainment-media corpus; CEJC picks the most common reading in spontaneous speech. These could differ for a small number of ambiguous kanji. In practice, the dominant reading of common words agrees across both sources, so this edge case does not materially affect the output.
