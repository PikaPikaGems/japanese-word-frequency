# Frequency Rank Datasets Reference

## What you are looking at

When you open `consolidated.csv`, each row is a Japanese word. The first three columns identify the word:

| Column | What it contains |
|--------|-----------------|
| `word` | The Japanese word (kanji, kana, or mixed) |
| `hiragana` | The word's reading in hiragana |
| `katakana` | The word's reading in katakana |

Every column after that is a **frequency rank** from a specific Japanese corpus or dataset. A value of **1** means this word is the single most frequent word in that dataset. A value of **5,000** means it is the 5,000th most frequent. A value of **-1** means the word either does not appear in that dataset, or ranked outside its top entries (most datasets are capped at top 25,000; YOUTUBE_FREQ_V3 goes to ~187,000; NIER only has ~10,000 total).

**Ranks are not comparable across columns.** Rank 500 in one dataset and rank 500 in another does not mean the word is equally common — corpus sizes, topics, and tokenization methods all differ. Use ranks to judge relative order *within* a column, or to see whether a word shows up across many different contexts.

**Why is a cell -1?**
- The word didn't appear in that corpus at all (wrong register, too rare, or a proper noun)
- The word appeared but ranked below the cap (e.g., below rank 25,000)
- The word was tokenized differently in that corpus (e.g., AOZORA_BUNKO has *zero* hiragana entries by design — see below)
- For HERMITDAVE datasets: the tokenizer split words into morphemes, so dictionary-form verbs essentially don't exist there

**Practical reading guide:**
- Word is -1 in almost every column → rare, domain-specific, or a proper noun
- Word ranks high in entertainment columns but -1 in BCCWJ/CEJC → fiction/media jargon not used in daily life
- Word ranks high in CEJC but -1 in BCCWJ → common in speech but rarely written formally
- Word ranks high in JPDB but low everywhere else → likely an inflected form or entertainment-specific term

---

## Column Reference

### Non-rank columns

| Column | Description |
|--------|-------------|
| `word` | The Japanese word |
| `hiragana` | Reading in hiragana. Sourced from JPDB v2.2 first; CEJC used as fallback. Pure-kana words use themselves. Empty if reading is unknown. |
| `katakana` | Same reading converted to katakana |

---

### CEJC columns — Everyday Spoken Japanese

**What CEJC is:** The Corpus of Everyday Japanese Conversation, produced by NINJAL (Japan's national language research institute). People self-recorded their own daily conversations across 200 hours, 577 conversations, ~2.4 million words, 1,675 speakers. Collected April 2016–2020. This is the most carefully designed corpus of how Japanese people actually speak in real life.

**Tokenization note:** CEJC uses UniDic lemma forms, which sometimes differ from how words are normally written. For example, する appears as 為る and それ appears as 其れ. The database applies a kana/kanji fallback to match these across sources, but occasional gaps remain.

**Tie-group note:** Below rank ~5,000, CEJC rankings become much less informative. 8,831 words all tie at rank 20,704 (each appeared exactly once). A CEJC rank above ~10,000 just means "this word appeared at least once in spoken conversation" — don't read too much into the specific number.

| Column | What the number means |
|--------|-----------------------|
| `cejc_combined_rank` | Overall CEJC frequency across all conversations and domains combined |
| `cejc_small_talk_rank` | Frequency within casual small talk (雑談) |
| `cejc_consultation_rank` | Frequency within counseling/advice conversations (相談) |
| `cejc_meeting_rank` | Frequency within formal meetings (会議) |
| `cejc_class_rank` | Frequency within classroom and lesson settings (授業) |
| `cejc_outdoors_rank` | Frequency within outdoor activity conversations (屋外活動) |
| `cejc_school_rank` | Frequency within school life conversations (学校生活) |
| `cejc_transportation_rank` | Frequency within conversations on public transportation (交通機関) |
| `cejc_public_commercial_rank` | Frequency within shops, public facilities, service interactions (公共・商業施設) |
| `cejc_home_rank` | Frequency within home and domestic conversations (家庭生活) |
| `cejc_indoors_rank` | Frequency within indoor non-home settings (屋内施設) |
| `cejc_workplace_rank` | Frequency within workplace conversations (職場) |
| `cejc_male_rank` | Frequency rank in speech produced by male speakers |
| `cejc_female_rank` | Frequency rank in speech produced by female speakers |

The domain columns are useful for context-specific vocabulary: if you're learning business Japanese, words that rank high in `cejc_meeting_rank` and `cejc_workplace_rank` are a priority. If a word has very different male vs. female ranks, it has a gendered usage pattern — though note this also reflects which domains each gender participated in within this corpus, not just inherent speech style.

---

### Written corpus columns

These reflect formal and written Japanese — books, news, encyclopedias, web text. They capture literate vocabulary well but underrepresent colloquial speech.

| Column | What the number means | Source summary |
|--------|-----------------------|----------------|
| `BCCWJ` | Rank in Japan's official balanced written corpus | NINJAL's 104.3 million word corpus: books, magazines, newspapers, blogs, forums, legal documents, textbooks. Materials from 1976–2006. The most authoritative general written Japanese reference. A -1 here often means the word is colloquial, very modern, or spoken-only. |
| `ADNO` | Rank in cleaned Japanese Wikipedia (Oct 2022 dump) | Wikipedia text, carefully filtered. Encyclopedic/technical vocabulary ranks high. A well-maintained fork of IlyaSemenov's project with cleaner output. |
| `ILYASEMENOV` | Rank in Japanese Wikipedia by document frequency (Aug 2022 dump) | Uses *document frequency* (how many different articles contain this word) rather than raw occurrence count. Known to contain some HTML entities (amp, gt, lt) as "words" in its data — those are noise. |
| `WIKIPEDIA_V2` | Rank in a community-built Wikipedia frequency dictionary (v2) | Covers ~850k unique entries from a large Wikipedia dataset. Similar use case to ADNO — encyclopedic vocabulary. |
| `MALTESAA_NWJC` | Rank in NINJAL Web Japanese Corpus | One of the largest Japanese corpora (~25.8 billion tokens), crawled from Japanese websites ~2014–2017. More contemporary and informal than BCCWJ. Ranks go up to ~106,762. |
| `CC100` | Rank in CommonCrawl filtered web text (~2020) | ~70GB of Japanese web text tokenized with both SudachiPy and MeCab. Broad contemporary written vocabulary. Community guides frequently recommend this as a reliable general-purpose reference because of its clean, well-differentiated output. |

---

### Spoken Japanese columns — Corpus of Spontaneous Japanese (CSJ)

**What CSJ is:** A major spoken Japanese corpus jointly developed by NINJAL, NICT, and Tokyo Institute of Technology. ~652 hours of speech, ~7 million words. Unlike CEJC (everyday conversation), the CSJ is primarily **academic monologues and presentations** — people formally presenting research at conferences. So it represents formal spoken Japanese, not casual speech.

The sub-corpora let you see how word frequency shifts between different speaking situations within the CSJ.

| Column | Japanese name | What it covers |
|--------|---------------|----------------|
| `MALTESAA_CSJ` | 全体 | Overall CSJ frequency across all sub-corpora |
| `MALTESAA_CSJ_DOKWA_GAKKAI` | 独話・学会 | Academic conference presentations and lectures (monologue) |
| `MALTESAA_CSJ_DOKWA_MOGI` | 独話・模擬 | Simulated/practice speeches (monologue) |
| `MALTESAA_CSJ_DOKWA_ROUDOKU` | 独話・朗読 | Prepared text read aloud, first reading (monologue) |
| `MALTESAA_CSJ_DOKWA_SAIRO` | 独話・再朗読 | Prepared text read aloud, second reading (monologue) |
| `MALTESAA_CSJ_DOKWA_SONOTA` | 独話・その他 | Other monologue types |
| `MALTESAA_CSJ_TAIKA_JIYU` | 対話・自由 | Unstructured free-form dialogue |
| `MALTESAA_CSJ_TAIKA_KADAI` | 対話・課題 | Task-based structured dialogue |
| `MALTESAA_CSJ_TAIKA_MOGI` | 対話・模擬 | Simulated/role-play dialogue |

A word ranking high in `MALTESAA_CSJ_DOKWA_GAKKAI` but not in `cejc_combined_rank` is likely academic/formal vocabulary used in presentations but not in everyday talk. The dialogue sub-corpora (TAIKA_*) are closer to natural conversation than the monologue ones (DOKWA_*).

---

### Fiction and literary columns

| Column | What the number means | Source summary |
|--------|-----------------------|----------------|
| `NOVELS` | Rank in a corpus of 10,000+ contemporary Japanese novels | Created by Kuuube. The largest novel-based list here. Rank 1 is `、` (Japanese comma) — punctuation was not filtered. |
| `INNOCENT_RANKED` | Rank in the Innocent Corpus (5,000+ novels, reordered by rank) | A long-used community fiction reference. Limitation: does not differentiate by reading — all readings of the same kanji word share one frequency value. Older dataset from ~2010s. |
| `NAROU` | Rank in the top 300 stories on 小説家になろう | Web novel platform frequency, dominated by isekai/fantasy/reincarnation genres. Words ranking unusually high here but not elsewhere are likely genre-specific (e.g., ギルド, 転生, 異世界). Hobbyist analysis using Kuromoji tokenizer. |
| `VN_FREQ` | Rank in 100+ visual novel scripts (~30 million words) | Covers a range of VN genres. Uses UniDic lemma forms (為る for する, 居る for いる), so dictionary form verbs rank differently than in surface-form lists. Hobbyist analysis. |
| `AOZORA_BUNKO` | Rank in Aozora Bunko public-domain literature | ⚠️ **This dataset contains zero hiragana entries by design.** It covers only kanji and jukugo (compound words) from pre-1953 classical and modern literature (Soseki, Akutagawa, etc.). A -1 here for a hiragana word means nothing — that word was never going to appear in this list. Useful for classical/literary vocabulary and rare jukugo. |

---

### Subtitle and media columns

These come from anime, drama, film, and Netflix subtitles — representing the vocabulary of performed/scripted Japanese media.

| Column | What the number means | Source summary |
|--------|-----------------------|----------------|
| `ANIME_JDRAMA` | Rank in an anime & J-drama subtitle corpus | From Shoui's widely-used frequency collection. ~100k entries. A standard community reference for entertainment subtitle vocabulary. |
| `NETFLIX` | Rank in Netflix Japan subtitles (Shoui version) | ~129k entries from the Shoui collection. Covers anime, drama, and live-action Netflix content. Distinct from DAVE_DOEBRICK (different tool, different processing). |
| `DAVE_DOEBRICK` | Rank in Netflix Japan subtitles (OhTalkWho version, ~2019) | Dave Doebrick processed all Netflix Japan subtitles available in 2019 using cb's Japanese Text Analysis Tool. 53 million total kanji occurrences. A companion note: ~12,000 words cover 95% of Netflix subtitle content. |
| `CHRISKEMPSON` | Rank in a subtitle corpus from 12,277 files | Drama, anime, and films. MIT licensed. A broad subtitle reference; source data includes POS tags (not shown here). |
| `JLAB` | Rank in anime sentences from ~1.85M Anki flashcards | Built from Japanese Like a Breeze anime/dorama Anki decks rather than raw subtitle files. Less reliable below rank ~2,000 due to parser limitations with informal speech. |
| `JITEN_ANIME` | Rank in anime media tracked by jiten.moe | ~257k entries; updated periodically (latest revision 2026-01-10). More recently maintained than most other anime lists here, so newer anime series are better represented. |
| `YOUTUBE_FREQ` | Rank in manually transcribed YouTube videos (older, ~56k entries) | Created by community members from manually transcribed videos. Note from the source: "Due to the limited size of the original dataset, frequencies should not be directly compared with larger corpora." Superseded by YOUTUBE_FREQ_V3. |
| `YOUTUBE_FREQ_V3` | Rank in manually transcribed YouTube videos (v3, ~187k entries) | Expanded version covering ~40,000 videos across 16 domains of spoken YouTube Japanese. The only dataset here not capped at 25,000 — entries go up to ~187,000. Same caveat about not comparing directly with larger corpora. |
| `HERMITDAVE_2016` | Rank in OpenSubtitles 2016 (movie/TV subtitles) | ⚠️ **Known structural issue:** The Japanese tokenizer (MeCab) split verbs into morphemes, so single characters like い, っ, て, る appear at high ranks as "words." Dictionary-form verbs like 思う essentially don't exist as entries. Treat a -1 here with caution — it may be a tokenization artifact, not a true absence. |
| `HERMITDAVE_2018` | Rank in OpenSubtitles 2018 (movie/TV subtitles) | ⚠️ Same morpheme-splitting issue as HERMITDAVE_2016. Combined from two split source files. Use with the same caution. |
| `HINGSTON` | Rank in a Japanese internet corpus from the University of Leeds | A mid-2000s web corpus (~44,998 entries). Older and limited in size. Lower priority than CC100 or BCCWJ for most use cases. |

---

### Dave Doebrick compilation variants (DD2_*)

Dave Doebrick compiled frequency lists in multiple tool formats. These all originate from the same underlying data but were packaged for different Anki/dictionary tools (Migaku, Morphman, Yomichan). Having multiple formats of the same source lets you cross-check consistency.

| Column | Format | Source content | Notes |
|--------|--------|----------------|-------|
| `DD2_MIGAKU_NETFLIX` | Migaku | Netflix subtitles | ~102k entries |
| `DD2_MIGAKU_NOVELS` | Migaku | Japanese novels (5k focus) | ⚠️ Only ~16,500 entries — a curated learner vocabulary deck, not a full corpus. Missing here does not mean the word is rare in novels. |
| `DD2_MORPHMAN_NETFLIX` | Morphman (UniDic) | Netflix subtitles, **proper names excluded** | ~105k entries. Because proper names were filtered out, this is slightly different from DAVE_DOEBRICK. |
| `DD2_MORPHMAN_NOVELS` | Morphman | Japanese novels (Kindle) | ~126k entries |
| `DD2_MORPHMAN_SHONEN` | Morphman | Shonen manga/anime | ~60k entries |
| `DD2_MORPHMAN_SOL` | Morphman | Slice-of-Life anime | ~45k entries |
| `DD2_YOMICHAN_NOVELS` | Yomichan (star ratings) | Japanese novels | ~89k entries |
| `DD2_YOMICHAN_SHONEN` | Yomichan (integer ranks) | Shonen top 100 titles | ~56k entries |
| `DD2_YOMICHAN_SHONEN_STARS` | Yomichan (star ratings) | Shonen manga/anime | ~56k entries — same corpus as DD2_YOMICHAN_SHONEN, different rank scale |
| `DD2_YOMICHAN_SOL` | Yomichan (integer ranks) | Slice-of-Life top 100 | ~43k entries |
| `DD2_YOMICHAN_VN` | Yomichan (star ratings) | Visual novels | ~85k entries |

If you want to assess a word's importance for a specific genre: compare `DD2_MORPHMAN_SHONEN` + `DD2_YOMICHAN_SHONEN` for Shonen; `DD2_MORPHMAN_SOL` + `DD2_YOMICHAN_SOL` for Slice-of-Life anime; `DD2_YOMICHAN_VN` + `VN_FREQ` for visual novels.

---

### Dictionary-based columns

These are not corpus frequency lists. The "rank" here reflects how words are ordered in Japanese dictionary entries, not how often they appear in real text. A high rank here means the word has a strong presence in standard Japanese dictionaries.

| Column | What the number means | Source summary |
|--------|-----------------------|----------------|
| `KOKUGOJITEN` | Rank in a Japanese monolingual dictionary (国語辞典) | ~156k entries from one standard kokugojiten. A high rank here means the word is a core dictionary headword. Useful for checking whether a word is "officially recognized vocabulary" vs. a neologism or proper noun. |
| `MONODICTS` | Rank across 12 major Japanese dictionaries combined | Aggregated from 大辞林, 広辞苑, デジタル大辞泉, 岩波国語辞典, 精選版 日本国語大辞典, 旺文社国語辞典, and 6 others (~206k entries). If a word appears here, it is recognized by mainstream Japanese lexicography. Broader coverage than KOKUGOJITEN. Words appearing in more of the 12 dictionaries tend to rank higher. |

A word missing from KOKUGOJITEN and MONODICTS but present in corpus-based lists is likely a proper noun, neologism, internet slang, or an inflected/compound form that dictionaries don't list as a headword.

---

### Specialized columns

| Column | What the number means | Source summary |
|--------|-----------------------|----------------|
| `H_FREQ` | Rank in an adult (18+) content corpus | Created by Kuuube from 18+ Japanese content (~44.7k entries). ⚠️ This corpus contains adult vocabulary. High ranks that appear *only* here indicate domain-specific terms. Common everyday words (私, 言う, 中) also rank high here because they are universal. |
| `NIER` | Rank within the Nier game series script | Only ~10,077 entries — the *entire* vocabulary of the Nier games. A rank here only tells you about frequency within those specific games, not Japanese generally. A -1 here simply means the word doesn't appear in Nier, which is normal. |
| `RSPEER` | Rank in a multi-source aggregated frequency list (top 25,000 only) | Built by Robyn Speer using Wikipedia, subtitles, news, books, web, Twitter, and Reddit. The methodology averages across sources while dropping outliers, making it robust to any single corpus's biases. Data frozen at a ~2021 snapshot — the project has been discontinued. A widely cited NLP reference. The 25,000 cap is hard: a -1 here means the word ranked below 25,000 across all its sources. |

---

### JPDB column

`JPDB` deserves a separate callout because it behaves very differently from every other column.

| Column | What the number means |
|--------|-----------------------|
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
- **WIKIPEDIA_V2 ↔ RSPEER: ~65–70%** — both draw from written, encyclopedic text
- **CEJC ↔ others: ~55–65%** — lowest among general-purpose datasets; spoken UniDic lemma forms diverge from written/subtitle surface forms
- **JPDB ↔ anything: ~25–45%** — consistently the lowest; entertainment register + surface forms explain most of the gap

What this means for you: if a word ranks high across BCCWJ, RSPEER, CEJC, and ANIME_JDRAMA, it is genuinely common across formal written, multi-source, spoken, and media Japanese. If it only ranks high in a few niche columns, its utility depends on your specific use case.
