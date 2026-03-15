# Frequency Rank Datasets Reference

## What you are looking at

When you open `consolidated.csv`, each row is a Japanese word. The first three columns identify the word:

| Column     | What it contains                          |
| ---------- | ----------------------------------------- |
| `word`     | The Japanese word (kanji, kana, or mixed) |
| `hiragana` | The word's reading in hiragana            |
| `katakana` | The word's reading in katakana            |

Every column after that is a **frequency rank** from a specific Japanese corpus or dataset. A value of **1** means this word is the single most frequent word in that dataset. A value of **5,000** means it is the 5,000th most frequent. A value of **-1** means the word either does not appear in that dataset, or ranked outside its top entries (most datasets are capped at top 25,000; NIER only has ~10,000 total).

**Ranks are not comparable across columns.** Rank 500 in one dataset and rank 500 in another does not mean the word is equally common — corpus sizes, topics, and tokenization methods all differ. Use ranks to judge relative order _within_ a column, or to see whether a word shows up across many different contexts.

**Why is a cell -1?**

- The word didn't appear in that corpus at all (wrong register, too rare, or a proper noun)
- The word appeared but ranked below the cap (e.g., below rank 25,000)
- The word was tokenized differently in that corpus (e.g., AOZORA*BUNKO has \_zero* hiragana entries by design — see below)
- For HERMITDAVE datasets: the tokenizer split words into morphemes, so dictionary-form verbs essentially don't exist there

**Practical reading guide:**

- Word is -1 in almost every column → rare, domain-specific, or a proper noun
- Word ranks high in entertainment columns but -1 in BCCWJ_LUW/CEJC → fiction/media jargon not used in daily life
- Word ranks high in CEJC but -1 in BCCWJ_LUW → common in speech but rarely written formally
- Word ranks high in JPDB but low everywhere else → likely an inflected form or entertainment-specific term

---

## SAMPLE DATA

CEJC

```
    1  word,hiragana,katakana,cejc_combined_rank,cejc_small_talk_rank,cejc_consultation_rank,cejc_meeting_rank,cejc_class_rank,cejc_outdoors_rank,cejc_school_rank,cejc_transportation_rank,cejc_public_commercial_rank,cejc_home_rank,cejc_indoors_rank,cejc_workplace_rank,cejc_male_rank,cejc_female_rank,ADNO,ANIME_JDRAMA,AOZORA_BUNKO,BCCWJ_LUW,BCCWJ_SUW,CC100,CHRISKEMPSON,DAVE_DOEBRICK,DD2_MIGAKU_NETFLIX,DD2_MORPHMAN_NETFLIX,DD2_MORPHMAN_NOVELS,DD2_MORPHMAN_SHONEN,DD2_MORPHMAN_SOL,DD2_YOMICHAN_NOVELS,DD2_YOMICHAN_SHONEN,DD2_YOMICHAN_SHONEN_STARS,DD2_YOMICHAN_SOL,DD2_YOMICHAN_VN,HERMITDAVE_2016,HERMITDAVE_2018,HINGSTON,H_FREQ,ILYASEMENOV,INNOCENT_RANKED,JITEN_ANIME,JLAB,JPDB,MALTESAA_CSJ,MALTESAA_CSJ_DOKWA_GAKKAI,MALTESAA_CSJ_DOKWA_MOGI,MALTESAA_CSJ_DOKWA_ROUDOKU,MALTESAA_CSJ_DOKWA_SAIRO,MALTESAA_CSJ_DOKWA_SONOTA,MALTESAA_CSJ_TAIKA_JIYU,MALTESAA_CSJ_TAIKA_KADAI,MALTESAA_CSJ_TAIKA_MOGI,MALTESAA_NWJC,NAROU,NETFLIX,NIER,NOVELS,VN_FREQ,WIKIPEDIA_V2,YOUTUBE_FREQ,YOUTUBE_FREQ_V3,RSPEER
     2  うん,うん,ウン,1,2,2,1,2,2,2,2,2,2,1,1,2,1,12004,59,326,2172,4034,50,100,102,109,588,71,51,369,71,65,46,86,284,239,3066,3755,13881,519,76,62,85,104,2172,186,201,939,450,1,8,2,2061,1798,103,722,393,2517,11480,158,145,584
     3  だ,だ,ダ,2,1,1,2,1,1,1,1,1,1,2,2,1,2,54,2,113,9,6,13,2,1,1,9,1,1,3647,1,1,1,2,10,10,29,12909,3457,4,10,4,9,3,5,2,1,5,3,2,2,1,7,6225,2,6,4,9043,12,7,3,14
     4  ね,ね,ネ,3,3,3,5,5,3,3,3,3,4,3,3,3,3,1543,19,394,73,42,10,20,19,21,50,27,20,1437,27,24,19,31,31,38,82,5508,13696,3042,15,13,18,24,38,21,41,24,14,5,3,5,46,2583,20,25,52,2133,1572,14,17,26
```

---

## Column Reference

### Non-rank columns

| Column     | Description                                                                                                                            |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `word`     | The Japanese word                                                                                                                      |
| `hiragana` | Reading in hiragana. Sourced from JPDB v2.2 first; CEJC used as fallback. Pure-kana words use themselves. Empty if reading is unknown. |
| `katakana` | Same reading converted to katakana                                                                                                     |

---

### CEJC columns — Everyday Spoken Japanese

**What CEJC is:** The Corpus of Everyday Japanese Conversation, produced by NINJAL (Japan's national language research institute). People self-recorded their own daily conversations across 200 hours, 577 conversations, ~2.4 million words, 1,675 speakers. Collected April 2016–2020. This is the most carefully designed corpus of how Japanese people actually speak in real life.

**Tokenization note:** CEJC uses UniDic lemma forms, which sometimes differ from how words are normally written. For example, する appears as 為る and それ appears as 其れ. The database applies a kana/kanji fallback to match these across sources, but occasional gaps remain.

**Tie-group note:** Below rank ~5,000, CEJC rankings become much less informative. 8,831 words all tie at rank 20,704 (each appeared exactly once). A CEJC rank above ~10,000 just means "this word appeared at least once in spoken conversation" — don't read too much into the specific number.

| Column                        | What the number means                                                            |
| ----------------------------- | -------------------------------------------------------------------------------- |
| `cejc_combined_rank`          | Overall CEJC frequency across all conversations and domains combined             |
| `cejc_small_talk_rank`        | Frequency within casual small talk (雑談)                                        |
| `cejc_consultation_rank`      | Frequency within counseling/advice conversations (相談)                          |
| `cejc_meeting_rank`           | Frequency within formal meetings (会議)                                          |
| `cejc_class_rank`             | Frequency within classroom and lesson settings (授業)                            |
| `cejc_outdoors_rank`          | Frequency within outdoor activity conversations (屋外活動)                       |
| `cejc_school_rank`            | Frequency within school life conversations (学校生活)                            |
| `cejc_transportation_rank`    | Frequency within conversations on public transportation (交通機関)               |
| `cejc_public_commercial_rank` | Frequency within shops, public facilities, service interactions (公共・商業施設) |
| `cejc_home_rank`              | Frequency within home and domestic conversations (家庭生活)                      |
| `cejc_indoors_rank`           | Frequency within indoor non-home settings (屋内施設)                             |
| `cejc_workplace_rank`         | Frequency within workplace conversations (職場)                                  |
| `cejc_male_rank`              | Frequency rank in speech produced by male speakers                               |
| `cejc_female_rank`            | Frequency rank in speech produced by female speakers                             |

The domain columns are useful for context-specific vocabulary: if you're learning business Japanese, words that rank high in `cejc_meeting_rank` and `cejc_workplace_rank` are a priority. If a word has very different male vs. female ranks, it has a gendered usage pattern — though note this also reflects which domains each gender participated in within this corpus, not just inherent speech style.

---

### Written corpus columns

These reflect formal and written Japanese — books, news, encyclopedias, web text. They capture literate vocabulary well but underrepresent colloquial speech.

| Column          | What the number means                                            | Source summary                                                                                                                                                                                                                                                               |
| --------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `BCCWJ_LUW`     | Rank in Japan's official balanced written corpus (Long Unit Word)  | NINJAL's 104.3 million word corpus: books, magazines, newspapers, blogs, forums, legal documents, textbooks. Materials from 1976–2006. LUW treats compound words and verb+auxiliary sequences as single units — ranks surface more content words as learners encounter them. The most authoritative general written Japanese reference. |
| `BCCWJ_SUW`     | Rank in Japan's official balanced written corpus (Short Unit Word) | Same BCCWJ corpus as above. SUW is the smallest morphological unit — particles, auxiliaries, and content words are all separate entries. Top ranks are dominated by grammatical particles and auxiliaries (の, は, を, て…). The standard BCCWJ tokenization. |
| `ADNO`          | Rank in cleaned Japanese Wikipedia (Oct 2022 dump)               | Wikipedia text, carefully filtered. Encyclopedic/technical vocabulary ranks high. A well-maintained fork of IlyaSemenov's project with cleaner output.                                                                                                                       |
| `ILYASEMENOV`   | Rank in Japanese Wikipedia by document frequency (Aug 2022 dump) | Uses _document frequency_ (how many different articles contain this word) rather than raw occurrence count. Known to contain some HTML entities (amp, gt, lt) as "words" in its data — those are noise.                                                                      |
| `WIKIPEDIA_V2`  | Rank in a community-built Wikipedia frequency dictionary (v2)    | Covers ~850k unique entries from a large Wikipedia dataset. Similar use case to ADNO — encyclopedic vocabulary.                                                                                                                                                              |
| `MALTESAA_NWJC` | Rank in NINJAL Web Japanese Corpus                               | One of the largest Japanese corpora (~25.8 billion tokens), crawled from Japanese websites ~2014–2017. More contemporary and informal than BCCWJ_LUW. Ranks go up to ~106,762.                                                                                               |
| `CC100`         | Rank in CommonCrawl filtered web text (~2020)                    | ~70GB of Japanese web text tokenized with both SudachiPy and MeCab. Broad contemporary written vocabulary. Community guides frequently recommend this as a reliable general-purpose reference because of its clean, well-differentiated output.                              |

---

### Spoken Japanese columns — Corpus of Spontaneous Japanese (CSJ)

**What CSJ is:** A major spoken Japanese corpus jointly developed by NINJAL, NICT, and Tokyo Institute of Technology. ~652 hours of speech, ~7 million words. Unlike CEJC (everyday conversation), the CSJ is primarily **academic monologues and presentations** — people formally presenting research at conferences. So it represents formal spoken Japanese, not casual speech.

The sub-corpora let you see how word frequency shifts between different speaking situations within the CSJ.

| Column                       | Japanese name | What it covers                                             |
| ---------------------------- | ------------- | ---------------------------------------------------------- |
| `MALTESAA_CSJ`               | 全体          | Overall CSJ frequency across all sub-corpora               |
| `MALTESAA_CSJ_DOKWA_GAKKAI`  | 独話・学会    | Academic conference presentations and lectures (monologue) |
| `MALTESAA_CSJ_DOKWA_MOGI`    | 独話・模擬    | Simulated/practice speeches (monologue)                    |
| `MALTESAA_CSJ_DOKWA_ROUDOKU` | 独話・朗読    | Prepared text read aloud, first reading (monologue)        |
| `MALTESAA_CSJ_DOKWA_SAIRO`   | 独話・再朗読  | Prepared text read aloud, second reading (monologue)       |
| `MALTESAA_CSJ_DOKWA_SONOTA`  | 独話・その他  | Other monologue types                                      |
| `MALTESAA_CSJ_TAIKA_JIYU`    | 対話・自由    | Unstructured free-form dialogue                            |
| `MALTESAA_CSJ_TAIKA_KADAI`   | 対話・課題    | Task-based structured dialogue                             |
| `MALTESAA_CSJ_TAIKA_MOGI`    | 対話・模擬    | Simulated/role-play dialogue                               |

A word ranking high in `MALTESAA_CSJ_DOKWA_GAKKAI` but not in `CEJC_rank` is likely academic/formal vocabulary used in presentations but not in everyday talk. The dialogue sub-corpora (TAIKA*\*) are closer to natural conversation than the monologue ones (DOKWA*\*).

---

### Fiction and literary columns

| Column            | What the number means                                          | Source summary                                                                                                                                                                                                                                                                                                                                    |
| ----------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `NOVELS`          | Rank in a corpus of 10,000+ contemporary Japanese novels       | Created by Kuuube. The largest novel-based list here. Rank 1 is `、` (Japanese comma) — punctuation was not filtered.                                                                                                                                                                                                                             |
| `INNOCENT_RANKED` | Rank in the Innocent Corpus (5,000+ novels, reordered by rank) | A long-used community fiction reference. Limitation: does not differentiate by reading — all readings of the same kanji word share one frequency value. Older dataset from ~2010s.                                                                                                                                                                |
| `NAROU`           | Rank in the top 300 stories on 小説家になろう                  | Web novel platform frequency, dominated by isekai/fantasy/reincarnation genres. Words ranking unusually high here but not elsewhere are likely genre-specific (e.g., ギルド, 転生, 異世界). Hobbyist analysis using Kuromoji tokenizer.                                                                                                           |
| `VN_FREQ`         | Rank in 100+ visual novel scripts (~30 million words)          | Covers a range of VN genres. Uses UniDic lemma forms (為る for する, 居る for いる), so dictionary form verbs rank differently than in surface-form lists. Hobbyist analysis.                                                                                                                                                                     |
| `AOZORA_BUNKO`    | Rank in Aozora Bunko public-domain literature                  | ⚠️ **This dataset contains zero hiragana entries by design.** It covers only kanji and jukugo (compound words) from pre-1953 classical and modern literature (Soseki, Akutagawa, etc.). A -1 here for a hiragana word means nothing — that word was never going to appear in this list. Useful for classical/literary vocabulary and rare jukugo. |

---

### Subtitle and media columns

These come from anime, drama, film, and Netflix subtitles — representing the vocabulary of performed/scripted Japanese media.

| Column            | What the number means                                             | Source summary                                                                                                                                                                                                                                                                                                                                                                                                            |
| ----------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ANIME_JDRAMA`    | Rank in an anime & J-drama subtitle corpus                        | Compiled by Shoui from anime and J-drama subtitle files using cb's Japanese Text Analysis Tool. ~100k entries. Widely referenced in the Japanese learning community (TheMoeWay, Refold) as a primary entertainment subtitle reference. Its ~80% pairwise overlap with NETFLIX at the top 5k confirms it captures subtitle vocabulary representatively.                                                                    |
| `NETFLIX`         | Rank in Netflix Japan subtitles (Shoui version)                   | ~129k entries from the Shoui collection. Covers anime, drama, and live-action Netflix content. Distinct from DAVE_DOEBRICK (different tool, different processing).                                                                                                                                                                                                                                                        |
| `DAVE_DOEBRICK`   | Rank in Netflix Japan subtitles (OhTalkWho version, ~2019)        | Dave Doebrick processed all Netflix Japan subtitles available in 2019 using cb's Japanese Text Analysis Tool. 53 million total kanji occurrences. A companion note: ~12,000 words cover 95% of Netflix subtitle content.                                                                                                                                                                                                  |
| `CHRISKEMPSON`    | Rank in a subtitle corpus from 12,277 files                       | Drama, anime, and films. Built using JParser and cb's Japanese Text Analysis Tool. Broad coverage but less curated than the Shoui collections and not actively maintained.                                                                                                                                                                                                                                                |
| `JLAB`            | Rank in anime sentences from ~1.85M Anki flashcards               | Built by Joe (japanese-like-a-breeze.com) from 301 Anki decks (anime/dorama sentences). Tokenized with MeCab + ipadic + a Jisho.org C++ parser that struggles with slang and informal speech — it sometimes treats multi-word expressions as single tokens (e.g., ような as よう な). Rankings below ~2,000 are unreliable due to these parsing errors. Readings come from JMdict's first entry only and may be outdated. |
| `JITEN_ANIME`     | Rank in anime media tracked by jiten.moe                          | ~257k entries; updated periodically (latest revision 2026-01-10). More recently maintained than most other anime lists here, so newer anime series are better represented.                                                                                                                                                                                                                                                |
| `YOUTUBE_FREQ`    | Rank in manually transcribed YouTube videos (older, ~56k entries) | Created by community members from manually transcribed videos. Note from the source: "Due to the limited size of the original dataset, frequencies should not be directly compared with larger corpora." Superseded by YOUTUBE_FREQ_V3.                                                                                                                                                                                   |
| `YOUTUBE_FREQ_V3` | Rank in manually transcribed YouTube videos (v3, top 25k)         | Expanded version covering ~40,000 videos across 16 domains of spoken YouTube Japanese. The upstream source contains ~187k entries; capped at top 25,000 here like all other sources. Same caveat about not comparing directly with larger corpora.                                                                                                                                                                        |
| `HERMITDAVE_2016` | Rank in OpenSubtitles 2016 (movie/TV subtitles)                   | ⚠️ **Known structural issue:** The Japanese tokenizer (MeCab) split verbs into morphemes, so single characters like い, っ, て, る appear at high ranks as "words." Dictionary-form verbs like 思う essentially don't exist as entries. Treat a -1 here with caution — it may be a tokenization artifact, not a true absence.                                                                                             |
| `HERMITDAVE_2018` | Rank in OpenSubtitles 2018 (movie/TV subtitles)                   | ⚠️ Same morpheme-splitting issue as HERMITDAVE_2016. Combined from two split source files. Use with the same caution.                                                                                                                                                                                                                                                                                                     |
| `HINGSTON`        | Rank in a Japanese internet corpus from the University of Leeds   | A mid-2000s web corpus (~44,998 entries). Older and limited in size. Lower priority than CC100 or BCCWJ_LUW for most use cases.                                                                                                                                                                                                                                                                                           |

---

### Dave Doebrick compilation variants (DD2\_\*)

Dave Doebrick compiled frequency lists in multiple tool formats. These were packaged for different Anki/dictionary tools (Migaku, Morphman, Yomichan). The Yomichan source files used either integer ranks or a star-rating display format (`★★★★★ (N)`) — but the processing scripts extract the underlying integer N in both cases, so all DD2*YOMICHAN*\* columns in this CSV store sequential integer ranks. The star-rating label in the column name refers to the source format, not the values stored here. Having multiple formats of the same source lets you cross-check consistency.

| Column                      | Format            | Source content                               | Notes                                                                                                                                  |
| --------------------------- | ----------------- | -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `DD2_MIGAKU_NETFLIX`        | Migaku            | Netflix subtitles                            | ~102k entries                                                                                                                          |
| `DD2_MORPHMAN_NETFLIX`      | Morphman (UniDic) | Netflix subtitles, **proper names excluded** | ~105k entries. Proper name filtering makes this slightly different from DAVE_DOEBRICK; prefer this when you want to avoid name noise.  |
| `DD2_MORPHMAN_NOVELS`       | Morphman          | Japanese novels (Kindle)                     | ~126k entries                                                                                                                          |
| `DD2_MORPHMAN_SHONEN`       | Morphman          | Shonen manga/anime                           | ~60k entries                                                                                                                           |
| `DD2_MORPHMAN_SOL`          | Morphman          | Slice-of-Life anime                          | ~45k entries                                                                                                                           |
| `DD2_YOMICHAN_NOVELS`       | Yomichan          | Japanese novels                              | ~89k entries                                                                                                                           |
| `DD2_YOMICHAN_SHONEN`       | Yomichan          | Shonen top 100 titles                        | ~56k entries                                                                                                                           |
| `DD2_YOMICHAN_SHONEN_STARS` | Yomichan          | Shonen manga/anime                           | ~56k entries — same corpus as DD2_YOMICHAN_SHONEN, different source file.                                                              |
| `DD2_YOMICHAN_SOL`          | Yomichan          | Slice-of-Life top 100                        | ~43k entries                                                                                                                           |
| `DD2_YOMICHAN_VN`           | Yomichan          | Visual novels                                | ~85k entries                                                                                                                           |

For genre-specific assessment: `DD2_MORPHMAN_SHONEN` + `DD2_YOMICHAN_SHONEN` for Shonen; `DD2_MORPHMAN_SOL` + `DD2_YOMICHAN_SOL` for Slice-of-Life anime; `DD2_YOMICHAN_VN` + `VN_FREQ` for visual novels.

---

### Specialized columns

| Column        | What the number means                                              | Source summary                                                                                                                                                                                                                                                                                                                                                                                           |
| ------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `H_FREQ`      | Rank in an adult (18+) content corpus                              | Created by Kuuube from 18+ Japanese content (~44.7k entries). ⚠️ This corpus contains adult vocabulary. High ranks that appear _only_ here indicate domain-specific terms. Common everyday words (私, 言う, 中) also rank high here because they are universal.                                                                                                                                          |
| `NIER`        | Rank within the Nier game series script                            | Only ~10,077 entries — the _entire_ vocabulary of the Nier games. A rank here only tells you about frequency within those specific games, not Japanese generally. A -1 here simply means the word doesn't appear in Nier, which is normal.                                                                                                                                                               |
| `RSPEER_rank` | Rank in a multi-source aggregated frequency list (top 25,000 only) | Built by Robyn Speer using Wikipedia, subtitles, news, books, web, Twitter, and Reddit. The methodology averages across sources while dropping outliers, making it robust to any single corpus's biases. Data frozen at a ~2021 snapshot — the project has been discontinued. A widely cited NLP reference. The 25,000 cap is hard: a -1 here means the word ranked below 25,000 across all its sources. |

---

### JPDB column

`JPDB` deserves a separate callout because it behaves very differently from every other column.

| Column | What the number means                                                                                                     |
| ------ | ------------------------------------------------------------------------------------------------------------------------- |
| `JPDB` | Rank in jpdb.io's entertainment media corpus (light novels, visual novels, anime, J-drama, web novels). Scraped May 2022. |

**Why JPDB ranks look "wrong" compared to other columns:**

JPDB records **surface forms, not lemmas**. This means inflected verb forms count as separate vocabulary items. For example, だった (past tense of だ) appears at rank 24, には at rank 26, だろう at rank 37, ではない at rank 89. Every other dataset in this CSV lemmatizes these back to their base forms (だ, に, は, etc.). This is why a word can rank top-100 in JPDB but be -1 or ranked much lower everywhere else — you may be looking at a base form that JPDB only counts when inflected.

JPDB also has a strong entertainment media bias. Fantasy and RPG terms (ギルド, ダンジョン, スケルトン), light novel tropes (ハーレム, クラスメイト), and movement/expression onomatopoeia (ぺこり, にこり, ゆらり) appear in JPDB's top 5k but are absent from general corpora. Cross-source analysis confirms JPDB misses 36–42% of general vocabulary that other sources agree on.

**Bottom line:** JPDB is useful for learners consuming Japanese entertainment fiction, but comparing its rank numbers directly against other columns is misleading. It operates on a different vocabulary model.

---

## Cross-dataset agreement at a glance

At the top 5,000 words, these are the pairwise overlaps between the main anchor datasets (how much of one dataset's top-5k appears in another's top-5k):

- **NETFLIX ↔ ANIME_JDRAMA: ~80%** — highest overlap; both are subtitle corpora of the same spoken register
- **YOUTUBE_FREQ_V3 ↔ CC100: ~75–77%** — both capture broad everyday language
- **WIKIPEDIA_V2 ↔ RSPEER_rank: ~65–70%** — both draw from written, encyclopedic text
- **CEJC ↔ others: ~55–65%** — lowest among general-purpose datasets; spoken UniDic lemma forms diverge from written/subtitle surface forms
- **JPDB ↔ anything: ~25–45%** — consistently the lowest; entertainment register + surface forms explain most of the gap

What this means for you: if a word ranks high across `BCCWJ_LUW`, `RSPEER_rank`, `CEJC_rank`, and `ANIME_JDRAMA`, it is genuinely common across formal written, multi-source, spoken, and media Japanese. If it only ranks high in a few niche columns, its utility depends on your specific use case.

---

## Quality Assessments

Sources are grouped by how much you should trust their ranks as signals of real-world Japanese frequency.

---

### Tier 1 — Most reliable for general Japanese

**`RSPEER_rank`** is methodologically the strongest general-purpose list. It aggregates frequency data from Wikipedia, subtitles, news, books, web crawls (OSCAR), Twitter, and Reddit — then for each word drops the highest and lowest source before averaging the rest. This outlier-dropping step makes it uniquely resistant to any single corpus's genre skew. Hard cap at 25,000 entries: a -1 here means ranked below 25,000 across all its sources. The project was discontinued ~2022 because LLM-generated web text was contaminating new crawl data.

**`CC100`** draws from ~70GB of filtered Japanese CommonCrawl (~2020), tokenized with two independent tokenizers (SudachiPy and MeCab), producing ~160k entries. Its ~75–77% top-5k overlap with `YOUTUBE_FREQ_V3` — the highest overlap between a written and a spoken-transcription corpus in this dataset — suggests it captures broad everyday language well, not just formal text. Community guides consistently single it out for clean, well-differentiated output.

**`BCCWJ_LUW`** and **`BCCWJ_SUW`** are the authoritative reference for formal written Japanese. NINJAL built the corpus from 104 million words spanning books, magazines, newspapers, blogs, legal documents, textbooks, and more (1976–2006), deliberately balanced across text types to avoid single-domain bias. `BCCWJ_LUW` (Long Unit Word) treats compound words and verb+auxiliary sequences as single units — better for vocabulary learning as words appear as learners encounter them. `BCCWJ_SUW` (Short Unit Word) uses the finest morphological segmentation, so top ranks are dominated by particles and auxiliaries. A -1 in either column reliably indicates a word is colloquial, very modern, or spoken-only.

**`CEJC_rank`** is the authoritative reference for everyday spoken Japanese. NINJAL recorded 200 hours of naturalistic self-recorded daily conversations from 1,675 speakers (2016–2020) — not broadcast speech, not read-aloud text, but people recording their own ambient conversations. **Critical caveat:** below rank ~5,000 the rankings become unreliable due to mass tie-groups. 8,831 words all tie at rank 20,704 (each appeared exactly once). Only the top ~5,000 `CEJC_rank` values meaningfully differentiate frequency.

---

### Tier 2 — Reliable for specific domains

**`ANIME_JDRAMA` and `NETFLIX`** are the most consistent entertainment subtitle sources in this dataset. At the top 5k they overlap ~80% — the highest pairwise overlap among all anchors — because both are subtitle corpora of the same spoken media register. A word ranking well in both is a reliable signal of anime/drama vocabulary. `ANIME_JDRAMA` covers anime and J-drama; `NETFLIX` covers anime, drama, and live-action Netflix content.

**`JITEN_ANIME`** is the most up-to-date anime-specific list (~257k entries, last revised 2026-01-10). `ANIME_JDRAMA` and `NETFLIX` predate many recent seasons; `JITEN_ANIME` is the better choice when recency matters.

**`YOUTUBE_FREQ_V3`** covers ~40,000 manually transcribed YouTube videos across 16 spoken domains. It has ~75–77% top-5k overlap with `CC100`, suggesting their vocabulary largely agrees despite one being web text and the other spoken transcription. Note from the source: "frequencies should not be directly compared with larger corpora" — the raw counts are not comparable, but the rank order is useful. The upstream source contains ~187k entries.

**`MALTESAA_NWJC`** is one of the largest corpora here (~25.8 billion tokens from Japanese websites, 2014–2017). Its main value over `BCCWJ_LUW` is contemporary and informal web language; its main value over `CC100` is earlier coverage of the 2010s web. Ranks go up to ~106,762.

**`WIKIPEDIA_V2` and `ADNO`** are both Wikipedia-derived, but from different pipelines (see FAQ). Both are reliable for encyclopedic and technical vocabulary. A word ranking well in either but poorly everywhere else is likely domain-specific or a proper noun.

**`MALTESAA_CSJ`** and its sub-columns cover formal spoken Japanese — primarily academic conference presentations and monologues. A word ranking well here but absent from `CEJC_rank` is academic vocabulary that appears in presentations but not everyday conversation.

**`NOVELS`** (Kuuube, 10,000+ contemporary novels) is the largest and most recent fiction corpus here. **`INNOCENT_RANKED`** (5,000+ novels) has been a community reference for years but has a known limitation: it does not differentiate by reading — all orthographic variants of the same kanji string share one frequency value.

---

### Tier 3 — Useful with notable caveats

**`DAVE_DOEBRICK`** and **`DD2_MORPHMAN_NETFLIX`** are both based on Netflix subtitles Dave Doebrick processed in 2019. The difference: `DAVE_DOEBRICK` used cb's Japanese Text Analysis Tool; `DD2_MORPHMAN_NETFLIX` used Morphman with UniDic tokenization and excluded proper names. Their vocabulary overlaps heavily but tokenization differences mean inflected forms and compound words can be split or grouped differently. Both are a 2019 snapshot — newer Netflix content is not reflected.

**`CHRISKEMPSON`** is built from 12,277 subtitle files using JParser and cb's Japanese Text Analysis Tool. The corpus is broad (drama, anime, film) but the pipeline is less maintained than Shoui's collections and the source files are not dated. Treat it as a corroborating signal rather than a primary reference.

**`JLAB`** is derived from 301 Anki decks (anime/dorama sentences) rather than raw subtitle files. Its parser (MeCab + ipadic + Jisho.org C++ parser) fails on slang and informal speech — it sometimes treats multi-word expressions as single tokens (e.g., ような parsed as よう な). Rankings below ~2,000 are unreliable due to accumulated parsing errors.

**`NAROU`** covers only the top 300 stories on 小説家になろう, which skew heavily toward isekai/fantasy/reincarnation. Terms like ギルド, 転生, 異世界 are inflated relative to their general Japanese frequency. Its tokenizer (Kuromoji) also differs from the UniDic-based sources.

**`VN_FREQ`** covers 100+ visual novel scripts (~30 million words) with UniDic lemma tokenization. Hobbyist-produced. Genre variation across VNs is wide, so a word's rank here depends heavily on which VN types are in the corpus.

**`HINGSTON`** is a mid-2000s Japanese web corpus from the University of Leeds (~45k entries). Both the age and the small size limit its value. `CC100` or `MALTESAA_NWJC` supersede it for any web-text use case.

---

### Tier 4 — Use with significant caution

**`JPDB`** records surface forms rather than lemmas, unlike every other source in this dataset. Inflected verb forms are separate vocabulary items: だった ranks #24, には ranks #26, だろう ranks #37, ではない ranks #89 — all of which every other source folds into だ, に, は. Additionally, JPDB has strong entertainment-fiction bias: fantasy/RPG terms (ギルド, ダンジョン), light novel tropes (ハーレム, クラスメイト), and expression onomatopoeia (ぺこり, にこり, ゆらり) appear in JPDB's top 5k but are absent from general corpora. Cross-source analysis confirms JPDB misses 36–42% of vocabulary that other sources agree on, with pairwise top-5k overlap of only 25–45% against all other anchors. Do not compare `JPDB` rank numbers directly to any other column.

**`HERMITDAVE_2016` and `HERMITDAVE_2018`** have a structural tokenization flaw: MeCab split verbs into morphemes, so い, っ, て, る appear as high-frequency "words" while dictionary-form verbs like 思う essentially don't exist as entries. A -1 here for a common verb is a tokenization artifact, not evidence the word is rare.

**`ILYASEMENOV`** uses document frequency (how many Wikipedia articles contain the word) rather than occurrence count, and is known to contain HTML entities (amp, gt, lt) as vocabulary entries in the raw data.

---

### Not frequency corpora — different interpretation required

**`AOZORA_BUNKO`** contains zero hiragana entries by design — it covers only kanji and jukugo from pre-1953 public-domain literature. A -1 for any hiragana word is structurally guaranteed.

**`NIER`** covers only ~10,077 unique words from the NieR game scripts. A -1 simply means the word doesn't appear in those games.

**`H_FREQ`** is an adult (18+) content corpus. Common everyday words (私, 言う, 中) also rank high because they're universal. Only ranks that appear _exclusively_ high in `H_FREQ` carry domain-specific signal.

---

## FAQ

### What is the difference between `NETFLIX`, `DAVE_DOEBRICK`, and `DD2_MORPHMAN_NETFLIX`?

All three are derived from Netflix Japan subtitle data, but they come from different sources and processing pipelines:

| Column                 | Who made it   | Tool used                        | Scope                                         | Key difference                                                                |
| ---------------------- | ------------- | -------------------------------- | --------------------------------------------- | ----------------------------------------------------------------------------- |
| `NETFLIX`              | Shoui         | Yomitan packaging                | Netflix subtitles (no year given)             | Shoui's collection; different processing than Doebrick                        |
| `DAVE_DOEBRICK`        | Dave Doebrick | cb's Japanese Text Analysis Tool | All Netflix Japan subtitles available in 2019 | ~53M kanji occurrences; includes proper names                                 |
| `DD2_MORPHMAN_NETFLIX` | Dave Doebrick | Morphman + UniDic (unidic_3011)  | Same 2019 Netflix data as DAVE_DOEBRICK       | Proper names **excluded**; UniDic lemmatization means different form grouping |

`NETFLIX` and `DAVE_DOEBRICK` both use surface-form tokenization but with different tools, so they can diverge on how compound words and verb forms are handled. `DD2_MORPHMAN_NETFLIX` uses UniDic lemmas, which means some inflected forms are merged — closer to what lemmatized sources like `BCCWJ_LUW` and `CEJC_rank` produce. Because proper names are filtered out in `DD2_MORPHMAN_NETFLIX`, it has fewer entries (~105k) than `DAVE_DOEBRICK` (~124k).

If you want to check a word's Netflix-subtitle importance and avoid proper-name noise, use `DD2_MORPHMAN_NETFLIX`. If you want raw coverage breadth, `NETFLIX` or `DAVE_DOEBRICK` give more entries.

---

### What is the difference between `WIKIPEDIA_V2` and `ADNO`?

Both are built from Japanese Wikipedia dumps but come from completely different processing pipelines:

| Column         | Source dump                | Pipeline                                                                | What's counted                                               |
| -------------- | -------------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------ |
| `ADNO`         | Oct 2022 Wikipedia dump    | Custom cleaning pipeline; fork of IlyaSemenov with additional filtering | Raw occurrence count, ranked by frequency                    |
| `WIKIPEDIA_V2` | Separate Wikipedia dataset | MarvNC/Shoui Yomitan collection                                         | Pre-ranked integer ranks from the Yomitan dictionary package |

`ADNO` is closer to a raw corpus frequency list — it counts how many times each word appears in the Wikipedia text. `WIKIPEDIA_V2` comes packaged as a pre-ranked Yomitan dictionary, so the ranking methodology (and what was filtered) reflects the decisions of the MarvNC/Shoui collection rather than a single transparent pipeline. `WIKIPEDIA_V2` has ~850k unique entries, making it far larger than `ADNO`'s 25k cap in this CSV.

In practice: if they disagree on a word's rank, the discrepancy reflects different pipeline decisions (tokenizer, filtering, normalization). `ADNO` is more transparent because the source dump and cleaning steps are documented. `ILYASEMENOV` is a third Wikipedia source using _document frequency_ (how many articles contain the word rather than total occurrences) — a fundamentally different metric — and has HTML entity noise in the raw data.
