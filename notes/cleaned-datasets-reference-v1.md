# Frequency Rank Datasets Reference

Each word in this database is assigned a **frequency rank** from each dataset below. A rank of **1** means it is the single most frequent word in that corpus. A rank of **25,000** means it is the 25,000th most frequent. A **blank/missing value** (or -1) means the word either did not appear in that corpus, or fell outside the top 25,000 (or top ~187k for YOUTUBE_FREQ_V3).

Ranks are not directly comparable across datasets — a rank of 500 in one corpus vs. 500 in another does not mean the word is equally common; corpus size, register, and tokenization method all differ. Use ranks for relative ordering within a single dataset, or to compare whether a word is "top-tier common" vs. "advanced" vs. "rare" across different sources.

---

## How to Use This File

**Is a word blank (or -1) in most datasets?** → It is probably rare, domain-specific, or a proper noun.

**Is a word ranked very high in entertainment datasets but blank (or -1) in BCCWJ/CEJC?** → It is likely fiction/media jargon not used in daily life.

**Is a word ranked very high in CEJC but blank (or -1) in BCCWJ?** → It is a common spoken word that rarely appears in formal written text.

**Does a word have very different ranks across similar datasets?** → Pay attention to the source notes below; tokenization and lemmatization differences are the most common culprit.

---

## Section 1 — CEJC: Corpus of Everyday Japanese Conversation

**Source:** NINJAL (National Institute for Japanese Language and Linguistics)
**Corpus:** 200 hours of audio/video, 577 conversations, ~2.4 million words, 1,675 speakers
**Collected:** April 2016–2020; published March 2022
**Tokenization:** UniDic (Short Unit Word / SUW)

The CEJC is Japan's most carefully designed spoken language corpus. Speakers self-recorded their own daily conversations in natural settings across balanced demographics (age, gender, region). It is one of the best sources for what Japanese people actually say in real life — not scripted or performed speech.

**Important caveat — UniDic kanji lemmas:** CEJC uses UniDic lemma forms, which sometimes differ from surface forms. For example, the word most people write as する appears as 為る, and それ appears as 其れ. The database applies a kana/kanji fallback to reconcile these, but occasional mismatches may remain.

**Important caveat — massive tie groups:** Only 430 of ~29,500 entries have truly unique ranks. At the bottom, 8,831 words all tie at rank 20,704 (appeared exactly once). So a rank of 20,000+ in CEJC is not very informative — it just means "occurred at least once in spoken conversation."

| Column                        | What it means                                                            |
| ----------------------------- | ------------------------------------------------------------------------ |
| `cejc_combined_rank`          | Overall CEJC frequency across all 577 conversations and all domains      |
| `cejc_small_talk_rank`        | Frequency within casual small talk conversations (雑談)                  |
| `cejc_consultation_rank`      | Frequency within counseling/advice consultations (相談)                  |
| `cejc_meeting_rank`           | Frequency within formal meetings (会議)                                  |
| `cejc_class_rank`             | Frequency within classroom/lesson settings (授業)                        |
| `cejc_outdoors_rank`          | Frequency within outdoor activity conversations (屋外活動)               |
| `cejc_school_rank`            | Frequency within school environment conversations (学校生活)             |
| `cejc_transportation_rank`    | Frequency within transportation contexts (交通機関)                      |
| `cejc_public_commercial_rank` | Frequency within public/commercial service interactions (公共・商業施設) |
| `cejc_home_rank`              | Frequency within home/domestic conversations (家庭生活)                  |
| `cejc_indoors_rank`           | Frequency within indoor non-home settings (屋内施設)                     |
| `cejc_workplace_rank`         | Frequency within workplace conversations (職場)                          |
| `cejc_male_rank`              | Frequency in speech produced by male speakers                            |
| `cejc_female_rank`            | Frequency in speech produced by female speakers                          |

**Best for:** Understanding what words actually appear in real spoken Japanese. Excellent for gauging everyday conversational importance. Domain columns are useful if you want to prioritize vocabulary for a specific context (e.g., business Japanese → `meeting_rank`, `workplace_rank`). Gender columns can highlight words that skew strongly male or female in usage.

---

## Section 2 — Written and Web Corpora

These datasets reflect written Japanese — books, news, websites, and encyclopedic text. They capture formal/literate vocabulary well but underrepresent colloquial speech.

---

### BCCWJ — Balanced Corpus of Contemporary Written Japanese

**Creator:** NINJAL
**Materials:** 1976–2006 (main body: 1986–2006); released 2011
**Size:** 104.3 million words; ~1 million unique entries in this version
**Sources:** Books, magazines, newspapers, white papers, blogs, Yahoo! forums, textbooks, legal documents, National Diet minutes
**Version:** Combined SUW + LUW (Short Unit Word + Long Unit Word)

Japan's first and most authoritative balanced written corpus. The "balanced" part is important: NINJAL used statistical sampling to proportionally represent different text types, so it is not dominated by any single genre. This makes it one of the most reliable general-purpose written frequency references.

**Caveats:** Materials are from 1976–2006 — modern internet slang, recent loanwords, and new vocabulary are absent. SUW and LUW rankings are merged; some words appear at the same rank due to ties in the source data.

**Best for:** Formal/academic written Japanese. Reliable benchmark for "standard written vocabulary." Good for learners aiming for JLPT, reading newspapers, or academic texts.

---

### ADNO — Japanese Wikipedia Word Frequency (Cleaned)

**Creator:** adno (fork of IlyaSemenov's project)
**Data date:** October 2022 Wikipedia dump
**Size:** ~550k unique entries; top 25k used
**Metric:** Occurrence count (total times word appeared across all articles)
**Tokenization:** MeCab

A cleaned Wikipedia frequency list with careful filtering — no digits in words, case-preserved, no minimum document threshold. This is a refinement of ILYASEMENOV (see below).

**Best for:** Written reference Japanese. Wikipedia vocabulary skews toward technical, encyclopedic, and proper noun-heavy language. Strong coverage of technical fields (science, history, politics). Compared to ILYASEMENOV, this version has better filtering of noise.

---

### ILYASEMENOV — Japanese Wikipedia Word Frequency

**Creator:** Ilya Semenov
**Data date:** August 2022 Wikipedia dump
**Size:** ~1.7M entries; top 25k used
**Metric:** Document frequency (number of articles containing the word, not occurrence count)
**Tokenization:** MeCab

The original Wikipedia frequency project. Uses document frequency (how many articles contain the word) rather than raw occurrence count, which gives a better sense of how broadly distributed a word is.

**Caveats:** Known to contain HTML entities (amp, gt, lt, etc.) as "words" in the output — these are noise entries and will appear at various ranks. Not suitable as a quality benchmark.

**Best for:** Broad cross-article coverage of Wikipedia vocabulary. The document-frequency metric rewards words that appear across many articles over words that repeat within a few.

---

### WIKIPEDIA_V2 — Japanese Wikipedia Word Frequency v2

**Creator:** Thermospore (community); distributed via Shoui/MarvNC
**Size:** ~850k unique entries; top 25k used
**Source:** Japanese Wikipedia (larger dataset than v0.1)

A community-built Yomitan frequency dictionary from Wikipedia, expanded in v2 to a much larger dataset. Revision history: v0.1 was shorter; v1 was never completed; v2 expanded coverage significantly.

**Best for:** Similar use case to ADNO — encyclopedic/technical written vocabulary. A good secondary check alongside BCCWJ and ADNO.

---

### MALTESAA_NWJC — NINJAL Web Japanese Corpus

**Creator:** NINJAL; Yomitan conversion by Maltesaa
**Size:** ~25.8 billion tokens in source; frequency list goes up to rank 106,762
**Source:** Crawled Japanese web text (~2014–2017)
**Tokenization:** UniDic

One of the largest Japanese corpora by token count. Covers a wide range of web-based written Japanese. Because it is web-crawled, it captures more informal and contemporary vocabulary than BCCWJ.

**Best for:** Broad contemporary written/web Japanese. Good complement to BCCWJ for modern vocabulary and internet-era language.

---

### CC100 — CommonCrawl Japanese Web Text

**Creator:** xydustc (arujisho); based on CC-100 by Facebook AI Research
**Data date:** ~2020
**Size:** ~70GB raw text → ~160k unique entries (after tokenization and dictionary filtering)
**Tokenization:** SudachiPy (Mode B) + fugashi (MeCab wrapper)

Derived from the CC-100 dataset used to train the XLM-R multilingual model. Web text filtered for quality. Dual tokenization (Sudachi + MeCab) produces well-differentiated readings. Community guides frequently recommend this as a primary sort dictionary for Yomitan due to its broad, clean coverage.

**Best for:** General contemporary web Japanese. Broad, well-differentiated vocabulary. A good "first pass" frequency reference for modern vocabulary. The dual tokenizer means more reliable word segmentation than single-tool approaches.

---

## Section 3 — Spoken Japanese: Corpus of Spontaneous Japanese (CSJ)

**Source:** NINJAL + NICT + Tokyo Institute of Technology
**Size:** ~652 hours of speech, ~7 million words
**Collected:** Late 1990s–2004; multiple editions since
**Tokenization:** UniDic

The CSJ is a world-class spoken Japanese corpus, annotated with orthographic transcriptions, phonetics, prosody, POS, and dependency structure. Unlike CEJC (which captures natural everyday conversation), the CSJ primarily contains **academic monologues and presentations** — people formally presenting research or giving prepared speeches.

This means the CSJ register is more **formal spoken Japanese**: structured sentences, technical vocabulary, academic jargon. It is valuable for understanding spoken academic/professional language but less representative of casual conversation.

| Column                       | Japanese     | What it covers                                 |
| ---------------------------- | ------------ | ---------------------------------------------- |
| `MALTESAA_CSJ`               | 全体         | Overall CSJ frequency across all sub-corpora   |
| `MALTESAA_CSJ_DOKWA_GAKKAI`  | 独話・学会   | Academic conference presentations and lectures |
| `MALTESAA_CSJ_DOKWA_MOGI`    | 独話・模擬   | Simulated/practice speeches and presentations  |
| `MALTESAA_CSJ_DOKWA_ROUDOKU` | 独話・朗読   | Prepared text read aloud (first reading)       |
| `MALTESAA_CSJ_DOKWA_SAIRO`   | 独話・再朗読 | Prepared text read aloud (re-reading)          |
| `MALTESAA_CSJ_DOKWA_SONOTA`  | 独話・その他 | Monologues not fitting other categories        |
| `MALTESAA_CSJ_TAIKA_JIYU`    | 対話・自由   | Unstructured free-form dialogue                |
| `MALTESAA_CSJ_TAIKA_KADAI`   | 対話・課題   | Task-based structured dialogue                 |
| `MALTESAA_CSJ_TAIKA_MOGI`    | 対話・模擬   | Simulated/role-play dialogue                   |

**Best for:** Academic spoken Japanese, professional presentations, formal speech. If a word ranks highly in CSJ but not CEJC, it is likely formal/academic vocabulary used in presentations rather than casual daily speech. The dialogue sub-corpora (TAIKA*\*) are closer to natural conversation than the monologue ones (DOKWA*\*).

---

## Section 4 — Fiction and Literary Corpora

These datasets capture vocabulary from novels, web fiction, visual novels, and classical literature. They are ideal for learners reading Japanese fiction.

---

### NOVELS — Japanese Novels (Kuuube)

**Creator:** Kuuube; distributed via MarvNC collection
**Size:** 10,000+ novels; ~270k unique entries

A large-scale novel corpus compiled by Kuuube, covering a broad range of contemporary Japanese fiction. The largest novel-based frequency list available, surpassing the Innocent Corpus in both novel count and coverage.

**Note:** Rank 1 is `、` (Japanese comma) — punctuation is included and not filtered out.

**Best for:** Contemporary fiction vocabulary. If you are reading novels, this is one of the most reliable broad-coverage references.

---

### INNOCENT_RANKED — Innocent Corpus

**Creator:** cb4960 (Koohii forum); ranked version by MarvNC
**Size:** 5,000+ novels; ~285k entries
**Data age:** Original list circa 2010s

One of the longest-used fiction frequency lists in the Japanese learning community, compiled from a large collection of novels. The "Ranked" version reorders by rank (1 = most frequent) rather than raw occurrence count.

**Caveats:** Does not differentiate by reading — all readings of a kanji word share the same frequency value. Provenance of underlying novels is not fully documented. Older dataset.

**Best for:** Cross-referencing fiction vocabulary. Wide community adoption means you will find it referenced in many learning resources.

---

### NAROU — 小説家になろう Web Novels

**Creator:** wareya; distributed via Shoui collection
**Size:** Top 300 stories from Shousetsuka ni Narou; ~49k entries
**Tokenization:** Kuromoji

Derived from the top 300 stories on Japan's most popular web novel platform, which is dominated by isekai, fantasy, and reincarnation genres. Reflects the specific vocabulary of that community rather than "novels" broadly.

**Caveats:** Hobbyist analysis; no quality guarantees (wareya's own note). Kuromoji tokenization may differ from MeCab-based lists. Genre skew is significant — expect fantasy/isekai vocabulary to rank unusually high.

**Best for:** Readers of isekai/fantasy web novels on Narou or similar platforms. If you see a word ranking highly here but not in NOVELS or BCCWJ, it is likely genre-specific web novel vocabulary (e.g., ギルド, 転生, 異世界).

---

### VN_FREQ — Visual Novels

**Creator:** wareya; distributed via Shoui collection
**Size:** 100+ VN script dumps; ~30 million words total; ~35k entries
**Tokenization:** Kuromoji

Word frequency from visual novel scripts. Visual novels contain a mix of narrative prose and dialogue, spanning many genres. Uses lemma/dictionary forms of words (為る for する, 居る for いる).

**Caveats:** Hobbyist analysis. Kuromoji tokenization. UniDic lemma forms may cause mismatches with surface-form-based lists. Genre varies widely by VN title.

**Best for:** Players/readers of visual novels. Broad VN coverage makes this a reasonable reference for fiction vocabulary that overlaps with anime/manga.

---

### AOZORA_BUNKO — Aozora Bunko Public Domain Literature

**Creator:** vtrm (data); MarvNC (Yomitan conversion)
**Size:** ~120k entries (words and jukugo)
**Source:** Pre-1953 Japanese literature (public domain)

Derived from Japan's public-domain digital library — primarily classical and modern pre-war literature (authors like Natsume Soseki, Akutagawa Ryunosuke, etc.).

**Critical caveat:** This list contains **only kanji and jukugo (compound words)** — it has zero hiragana entries by design. Pure-kana words will always be blank in this dataset. This is intentional: the tool it was built with was designed for kanji/jukugo analysis.

**Best for:** Classical and literary vocabulary, rare jukugo not found in modern corpora, and pre-war writing styles. If you are reading Meiji/Taisho/early Showa era literature, this is valuable. Do not use it to judge whether a word is "common in modern Japanese."

---

## Section 5 — Subtitle and Media Corpora

These datasets come from transcribed or subtitled media (anime, drama, movies, YouTube). They reflect the vocabulary of modern spoken/performance Japanese as it appears in media.

---

### ANIME_JDRAMA — Anime & J-drama (Shoui)

**Creator:** Shoui; distributed via anacreondjt.gitlab.io
**Size:** ~100k unique entries; top 25k used

General anime and J-drama subtitle frequency from Shoui's well-known frequency dictionary collection. A solid broad-coverage reference for entertainment media vocabulary.

**Best for:** Learners consuming anime and J-drama. One of the most widely referenced anime/drama frequency lists in the community.

---

### NETFLIX — Netflix Subtitles (Shoui)

**Creator:** Shoui; distributed via Shoui/MarvNC collections
**Size:** ~129k unique entries; top 25k used
**Source:** Japanese subtitles from Netflix

Netflix subtitle frequency from the Shoui collection. Distinct from the DAVE_DOEBRICK dataset (which is also Netflix-derived but uses a different tool and format).

**Best for:** Netflix content — J-drama, anime, and Japanese films available on Netflix. High overlap with ANIME_JDRAMA (both are subtitle-based), but Netflix's catalog includes more drama and live-action content.

---

### DAVE_DOEBRICK — Netflix Subtitles (OhTalkWho)

**Creator:** Dave Doebrick (YouTube: OhTalkWho オタク)
**Date:** ~2019
**Size:** 53 million total kanji occurrences; ~124k entries; top 25k used
**Tool:** cb's Japanese Text Analysis Tool

Dave Doebrick processed all Japanese subtitles available on Netflix Japan at the time (2019) to produce this frequency list. A companion list "Netflix 95% 12K.txt" shows that ~12,000 words cover 95% of Netflix subtitle content.

**Note:** This is a different processing of Netflix data than the NETFLIX (Shoui) dataset. Differences arise from different tools, different corpus snapshots, and different tokenization.

**Best for:** Corroborating the NETFLIX (Shoui) dataset or exploring differences. Produced from a specific point-in-time snapshot of Netflix Japan's catalog.

---

### CHRISKEMPSON — Japanese Subtitles Word Frequency

**Creator:** Chris Kempson
**Size:** 12,277 subtitle files; ~120k entries; top 25k used
**Source:** Japanese subtitle files from Matchoo95/JP-Subtitles (drama, anime, films)
**Tool:** JParser + cb's Japanese Text Analysis Tool
**License:** MIT

Subtitle frequency from a broad subtitle collection. Includes POS tags in the source data. Reasonable general-purpose subtitle reference.

**Best for:** Cross-referencing subtitle vocabulary across drama, anime, and film. The POS information in the source (not included here) makes the original file useful for POS-based analysis.

---

### JLAB — Japanese Like a Breeze Anime Frequency

**Creator:** "Joe" at Japanese Like a Breeze
**Date:** September 2020
**Size:** ~1.85 million sentences from 301 Anki decks (anime/dorama); ~67k entries; top 25k used
**Tokenization:** MeCab + ipadic

Built from anime and dorama flashcard decks rather than raw subtitle files. This means it captures vocabulary that language learners and subtitle creators considered "word-level" content.

**Caveats:** Parser struggles with slang and informal speech. Dictionary-based parser sometimes tokenizes multi-word expressions as single entries (e.g., ような instead of よう + な). Primarily useful for top ~2k words where accuracy is highest.

**Best for:** Cross-checking commonly studied anime vocabulary. Less reliable for words below rank ~2,000.

---

### JITEN_ANIME — Anime Frequency from jiten.moe

**Creator:** jiten.moe
**Data:** Updated periodically; latest revision 2026-01-10
**Size:** ~257k entries; top 25k used
**Source:** Anime media analyzed by jiten.moe

A maintained and periodically updated anime frequency list from the jiten.moe platform. More recently maintained than most other anime lists in this collection.

**Best for:** Anime vocabulary with relatively fresh data. Because it is actively maintained, it is better at capturing newer anime releases than older community lists.

---

### YOUTUBE_FREQ — YouTube Frequency (Shoui, older)

**Creator:** @Zetta, @Vexxed, @Anonymous; distributed via Shoui collection
**Size:** ~56k unique entries; top 25k used
**Source:** Manually transcribed YouTube videos

An older YouTube frequency list from the Shoui collection. Manually transcribed videos are higher quality than auto-generated captions, but the corpus is limited in size.

**Caveats:** "Due to the limited size of the original dataset, frequencies should not be directly compared with larger corpora." (official note from MarvNC). Superseded by YOUTUBE_FREQ_V3 for most purposes.

**Best for:** Spoken YouTube vocabulary. The older version; prefer YOUTUBE_FREQ_V3 for broader coverage.

---

### YOUTUBE_FREQ_V3 — YouTube Frequency V3 (MarvNC)

**Creator:** @Zetta, @Vexxed, @Anonymous; distributed via MarvNC collection
**Date:** Version 3 (more recent than YOUTUBE_FREQ)
**Size:** ~40,000 manually transcribed YouTube videos; ~187k entries (the only dataset here not capped at 25k)
**Domain coverage:** 16 specific domain lists

The expanded version of the YouTube frequency dataset, covering 16 domains of YouTube content (vlogs, gaming, news, film/anime review, cooking, etc.). The largest of the YouTube-based lists. Because it is manually transcribed, the data quality is higher than auto-caption-based lists.

**Caveats:** Same caveat as YOUTUBE_FREQ: "should not be directly compared with larger corpora." The 16 domain sub-lists are not shown individually in this database — only the combined ranking appears here.

**Best for:** Spoken YouTube vocabulary, conversational Japanese as used online. Good complement to CEJC for informal spoken language. The 187k+ entry range means many words that fall outside the top 25k in other lists will still have a rank here.

---

### HERMITDAVE_2016 — OpenSubtitles 2016

**Creator:** Hermit Dave
**Source:** OpenSubtitles 2016 corpus (movie and TV subtitles)
**Size:** Top 25k of ~50k entries
**License:** CC-BY-SA-4.0

Japanese word frequency derived from the OpenSubtitles 2016 subtitle corpus. Widely used across many languages; a standard multilingual subtitle frequency resource.

**⚠️ Structural caveat:** OpenSubtitles-based Japanese lists suffer from MeCab morpheme-splitting issues: words like いる are split into い + る, producing unintuitive single-character "words" at high ranks. This makes the list structurally incompatible with lemma-based lists and reduces its reliability for word-level analysis.

**Best for:** Cross-referencing subtitle vocabulary. Treat with caution due to the morpheme-splitting issue — high ranks for single characters (い, っ, て, る) are an artifact of the tokenizer, not meaningful.

---

### HERMITDAVE_2018 — OpenSubtitles 2018

**Creator:** Hermit Dave
**Source:** OpenSubtitles 2018 corpus
**Size:** Combined from two split files; top 25k of ~116k combined entries
**License:** CC-BY-SA-4.0

The 2018 version of the Hermit Dave OpenSubtitles list. The 2018 dataset was split into a "high-frequency" file and a "full" file during generation; this dataset combines both.

**⚠️ Same structural caveat as HERMITDAVE_2016:** MeCab morpheme-splitting makes single characters appear at high ranks. Use with caution.

**Best for:** Same caveats as HERMITDAVE_2016. The 2018 version covers a more recent subtitle corpus snapshot.

---

### HINGSTON — University of Leeds Japanese Corpus

**Creator:** hingston (GitHub); source data from the University of Leeds
**Source:** http://corpus.leeds.ac.uk/frqc/internet-jp.num (internet-based Japanese corpus)
**Size:** ~45k entries; top 25k used
**Tokenization:** MeCab

Derived from the University of Leeds internet Japanese corpus. The Leeds corpus was an internet-sourced corpus from the mid-2000s.

**Caveats:** The Leeds corpus is reportedly "temporarily unavailable outside the University of Leeds." This is an older internet corpus from ~2005 onward. Modern slang and contemporary vocabulary will be underrepresented.

**Best for:** A secondary cross-check for general web-based Japanese from the mid-2000s. Lower priority compared to CC100 or BCCWJ for most use cases, given its age and limited size.

---

## Section 6 — Dave Doebrick Compilation Variants (DD2\_\*)

Dave Doebrick compiled a collection of frequency lists in multiple formats for different tools (Migaku, Morphman, Yomichan). Several of these cover the same source content but packaged differently. They all originate from Doebrick's analysis, documented at: [Google Doc](https://docs.google.com/document/d/1IUWkvBxhoazBSTyRbdyRVk7hfKE51yorE86DCRNQVuw/edit)

| Column                      | Format                   | Source Content                             | Entries                                   |
| --------------------------- | ------------------------ | ------------------------------------------ | ----------------------------------------- |
| `DD2_MIGAKU_NETFLIX`        | Migaku JSON              | Netflix subtitles                          | ~102k                                     |
| `DD2_MIGAKU_NOVELS`         | Migaku JSON              | Japanese novels (5k focus)                 | ~16.5k — **only ~16.5k entries, not 25k** |
| `DD2_MORPHMAN_NETFLIX`      | Morphman report          | Netflix subtitles, UniDic, no proper names | ~105k                                     |
| `DD2_MORPHMAN_NOVELS`       | Morphman report          | Japanese novels (Kindle 5k)                | ~126k                                     |
| `DD2_MORPHMAN_SHONEN`       | Morphman report          | Shonen manga/anime                         | ~60k                                      |
| `DD2_MORPHMAN_SOL`          | Morphman report          | Slice-of-Life anime                        | ~45k                                      |
| `DD2_YOMICHAN_NOVELS`       | Yomichan (star ratings)  | Japanese novels, star-rated                | ~89k                                      |
| `DD2_YOMICHAN_SHONEN`       | Yomichan (integer ranks) | Shonen top 100 titles                      | ~56k                                      |
| `DD2_YOMICHAN_SHONEN_STARS` | Yomichan (star ratings)  | Shonen manga/anime, star-rated             | ~56k                                      |
| `DD2_YOMICHAN_SOL`          | Yomichan (integer ranks) | Slice-of-Life top 100 titles               | ~43k                                      |
| `DD2_YOMICHAN_VN`           | Yomichan (star ratings)  | Visual novels, star-rated                  | ~85k                                      |

**Notes on DD2 variants:**

- **Migaku vs. Morphman vs. Yomichan** versions of the same source (e.g., Netflix) were packaged for different Anki/dictionary tools. The underlying data is largely the same, but ranking may differ slightly due to different tool processing.
- **DD2_MIGAKU_NOVELS** is a curated learner deck (~16,469 words) rather than a pure corpus frequency list — it covers the "novel top 5k" vocabulary for study purposes. Because it is not a full-corpus list, it is not suitable as a cross-source benchmark.
- **STARS vs. non-STARS:** The Yomichan "stars" format uses ★ ratings (e.g., ★★★★★ (rank)) which were parsed to extract rank numbers. The non-stars version uses plain integer ranks. For `DD2_YOMICHAN_SHONEN` vs. `DD2_YOMICHAN_SHONEN_STARS`, both cover the same Shonen corpus but with different rank scales — they should not be treated as independent data.
- **Morphman format** includes UniDic tokenization and POS tags — `DD2_MORPHMAN_NETFLIX` explicitly excludes proper names ("no names" version), which makes its vocabulary coverage slightly different from `DAVE_DOEBRICK` (which includes all words).

**Best for:** Fine-grained comparison within a specific genre. If you are trying to prioritize vocabulary for Shonen manga specifically, compare `DD2_MORPHMAN_SHONEN`, `DD2_YOMICHAN_SHONEN`, and `DD2_YOMICHAN_SHONEN_STARS`. For Slice-of-Life anime, compare `DD2_MORPHMAN_SOL` and `DD2_YOMICHAN_SOL`. These multiple versions of the same content act as internal consistency checks.

---

## Section 7 — Dictionary-Based Frequency

These datasets are not derived from real-world text corpora but from Japanese dictionary entries. They tell you whether a word is "legitimately dictionary-listed" rather than how often it appears in actual usage.

---

### KOKUGOJITEN — 国語辞典 (Japanese Monolingual Dictionary)

**Creator:** Shoui; distributed via Shoui/MarvNC collections
**Size:** ~156k entries; top 25k used
**Source:** A standard Japanese monolingual dictionary (kokugojiten)

Frequency rank derived from a Japanese monolingual dictionary. The rank here essentially reflects the dictionary's internal ordering — core vocabulary comes first, rarer entries later.

**Caveats:** This is not a corpus frequency list — it reflects dictionary coverage priority, not real-world usage frequency. Notable oddity: rank 5 is `・` (interpunct/nakaguro), suggesting some punctuation slipped through.

**Best for:** Checking whether a word has a standard dictionary entry. If a word has a rank here but is absent from corpus-based lists, it may be an archaic or rare word that is technically "correct" but rarely used. Useful for filtering out neologisms, internet slang, and proper nouns that corpus lists may include.

---

### MONODICTS — Japanese Monolingual Dictionary Frequency (jpDicts 206k)

**Creator:** Distributed via Shoui/MarvNC collections
**Size:** ~206k entries; top 25k used
**Sources:** 12 major Japanese dictionaries including 大辞林, 広辞苑, デジタル大辞泉, 岩波国語辞典, 精選版 日本国語大辞典, 旺文社国語辞典, and others

Frequency rankings derived from multiple major Japanese monolingual dictionaries combined. More comprehensive than KOKUGOJITEN (single dictionary) because it aggregates across 12 dictionaries, providing better coverage of the full range of Japanese vocabulary.

**Best for:** The same use case as KOKUGOJITEN but with broader coverage. If a word appears here, it is recognized by mainstream Japanese lexicography. Words appearing in multiple dictionaries tend to rank higher. Excellent for filtering "real Japanese words" from proper nouns, neologisms, and OCR errors.

---

## Section 8 — Specialized and Niche

These datasets have specific limitations or cover unusual registers. They are valuable precisely because of their specificity but should not be used as general-purpose frequency references.

---

### H_FREQ — Adult (18+) Content Corpus

**Creator:** Kuuube
**Size:** ~44.7k entries; top 25k used

Word frequency from Japanese adult (18+/hentai) content. Included because this is a significant genre of Japanese media, and learners engaging with it will encounter vocabulary that does not appear in standard corpora.

**⚠️ Content note:** This corpus contains 18+ vocabulary. High-ranking words that appear primarily in H_FREQ but not in other corpora are likely genre-specific.

**Best for:** Understanding which words are strongly associated with adult content vs. general vocabulary. A word that ranks very high here but low (or missing) elsewhere is a domain-specific term. Common everyday words will still rank high here (私, 言う, etc.), showing they are universal.

---

### NIER — Nier Game Series

**Creator:** Shoui; distributed via Shoui/MarvNC collections
**Size:** ~10,077 entries (entire corpus, not capped at 25k)
**Source:** Nier game series (Japanese)

A game-specific frequency list derived from a single game series. Only ~10k unique tokens — the entire vocabulary of the Nier games.

**⚠️ Caveat:** This is extremely narrow — a single game franchise. Ranks here are only meaningful relative to other Nier vocabulary. A rank of 1,000 in NIER does not compare meaningfully to rank 1,000 in BCCWJ.

**Best for:** Nier game players who want to know which words are used most in those games. As a cross-reference for other datasets, a high NIER rank with no other corpus rank suggests a game-specific neologism or proper noun.

---

### RSPEER — wordfreq Multi-Source Aggregate

**Creator:** Robyn Speer (Luminoso)
**Data snapshot:** Through ~2021; project is now "sunsetted" (no future updates)
**Size:** 25,000 entries
**Sources:** Wikipedia, subtitles (SUBTLEX), news, books, web (OSCAR), Twitter, Reddit
**Tokenization:** MeCab

A sophisticated multi-source aggregate frequency list using the Zipf scale. The methodology drops the highest and lowest source for each word and averages the rest, minimizing outlier effects. The most-cited general-purpose frequency resource in the Japanese NLP community.

The dataset was deliberately discontinued by its author because LLM-generated "slop" has corrupted web data, and Twitter/Reddit API access was lost — meaning future updates would not reflect real language use.

**Zipf scale reference:**

| Zipf score | Frequency rank range | Meaning                           |
| ---------- | -------------------- | --------------------------------- |
| ≥ 5.1      | Top ~1,000           | Core grammar words (は, の, する) |
| 4.2–5.1    | ~1,000–5,000         | Common vocabulary                 |
| 3.9–4.2    | ~5,000–10,000        | Fluent-level vocabulary           |
| 3.2–3.9    | ~10,000–25,000       | Advanced/rare vocabulary          |

**Note:** The rank shown in this database is based on position in the top-25,000 list (rank 1 = highest Zipf score), not the raw Zipf value.

**Coverage benchmark:** ~1,738 words cover 80% of text; ~5,062 cover 90%; ~9,690 cover 95%.

**Best for:** Cross-language comparison (wordfreq covers 40+ languages), benchmarking against other NLP projects, and as a "sanity check" aggregate view. Because it averages across many sources with outlier removal, it is relatively robust to any single corpus's biases. Its frozen 2021 snapshot means very recent vocabulary (post-2021 words, new anime/game series names) may be absent or underranked.

---

## Quick Reference Summary

| Dataset                          | Type        | Register               | Size            | Key Caveat                                       |
| -------------------------------- | ----------- | ---------------------- | --------------- | ------------------------------------------------ |
| CEJC combined + domains + gender | Spoken      | Everyday conversation  | 2.4M words      | UniDic lemmas; massive tie groups below rank ~5k |
| BCCWJ                            | Written     | Formal/balanced        | 104.3M words    | 1976–2006 only                                   |
| ADNO                             | Written     | Encyclopedia           | ~550k entries   | Wikipedia vocabulary bias                        |
| ILYASEMENOV                      | Written     | Encyclopedia           | ~1.7M entries   | HTML entity noise; document-frequency metric     |
| WIKIPEDIA_V2                     | Written     | Encyclopedia           | ~850k entries   | Community-built                                  |
| MALTESAA_NWJC                    | Written     | Web                    | ~25.8B tokens   | Contemporary web                                 |
| CC100                            | Written     | Web                    | ~160k filtered  | Dual tokenizer; highly recommended               |
| MALTESAA_CSJ + 8 sub-corpora     | Spoken      | Academic/formal speech | 7M words        | Skews to monologue presentations                 |
| NOVELS                           | Fiction     | Contemporary novels    | 10,000+ novels  | Rank 1 is punctuation                            |
| INNOCENT_RANKED                  | Fiction     | Novels                 | 5,000+ novels   | No reading differentiation                       |
| NAROU                            | Fiction     | Web novels (isekai)    | Top 300 stories | Heavy genre bias                                 |
| VN_FREQ                          | Fiction     | Visual novels          | 100+ VNs        | UniDic lemma forms                               |
| AOZORA_BUNKO                     | Fiction     | Classical literature   | Pre-1953 works  | **Zero hiragana entries by design**              |
| ANIME_JDRAMA                     | Subtitles   | Anime + J-drama        | ~100k entries   | General media                                    |
| NETFLIX                          | Subtitles   | Netflix content        | ~129k entries   | Distinct from DAVE_DOEBRICK                      |
| DAVE_DOEBRICK                    | Subtitles   | Netflix (2019)         | ~124k entries   | ~12k words = 95% coverage                        |
| CHRISKEMPSON                     | Subtitles   | Anime + drama + film   | 12,277 files    | Includes POS in source                           |
| JLAB                             | Subtitles   | Anime (Anki decks)     | ~67k entries    | Unreliable below rank ~2k                        |
| JITEN_ANIME                      | Subtitles   | Anime                  | ~257k entries   | Actively maintained (2026)                       |
| YOUTUBE_FREQ                     | Spoken      | YouTube (older)        | ~56k entries    | Limited size                                     |
| YOUTUBE_FREQ_V3                  | Spoken      | YouTube, 16 domains    | ~187k entries   | Only dataset with 187k+ ranks                    |
| HERMITDAVE_2016                  | Subtitles   | Movies + TV            | Top 50k         | Morpheme-split artifacts                         |
| HERMITDAVE_2018                  | Subtitles   | Movies + TV            | ~116k combined  | Morpheme-split artifacts                         |
| HINGSTON                         | Web         | Internet (mid-2000s)   | ~45k entries    | Outdated (2005-era)                              |
| DD2_MIGAKU_NETFLIX               | Subtitles   | Netflix                | ~102k           | Migaku format                                    |
| DD2_MIGAKU_NOVELS                | Fiction     | Novels (curated)       | ~16.5k          | **Curated learner deck, not full corpus**        |
| DD2_MORPHMAN_NETFLIX             | Subtitles   | Netflix, no names      | ~105k           | UniDic, proper names excluded                    |
| DD2_MORPHMAN_NOVELS              | Fiction     | Novels (Kindle)        | ~126k           | Morphman format                                  |
| DD2_MORPHMAN_SHONEN              | Fiction     | Shonen manga/anime     | ~60k            | Morphman format                                  |
| DD2_MORPHMAN_SOL                 | Subtitles   | Slice-of-Life anime    | ~45k            | Morphman format                                  |
| DD2_YOMICHAN_NOVELS              | Fiction     | Novels (5k stars)      | ~89k            | Stars format                                     |
| DD2_YOMICHAN_SHONEN              | Fiction     | Shonen top 100         | ~56k            | Integer ranks                                    |
| DD2_YOMICHAN_SHONEN_STARS        | Fiction     | Shonen (stars)         | ~56k            | Stars format; same corpus as above               |
| DD2_YOMICHAN_SOL                 | Subtitles   | Slice-of-Life top 100  | ~43k            | Integer ranks                                    |
| DD2_YOMICHAN_VN                  | Fiction     | Visual novels (stars)  | ~85k            | Stars format                                     |
| KOKUGOJITEN                      | Dictionary  | 国語辞典               | ~156k entries   | Not corpus-based                                 |
| MONODICTS                        | Dictionary  | 12 major dictionaries  | ~206k entries   | Not corpus-based                                 |
| H_FREQ                           | Specialized | Adult (18+) content    | ~44.7k entries  | 18+ vocabulary                                   |
| NIER                             | Specialized | Nier games only        | ~10k entries    | Single game series                               |
| RSPEER                           | Aggregate   | Multi-source           | 25k entries     | Frozen 2021 snapshot                             |
