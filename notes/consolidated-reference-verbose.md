# Japanese Word Frequency Lists — Consolidated Reference

---

## 1. BCCWJ (Balanced Corpus of Contemporary Written Japanese)

- **Description:** Japan's first 100-million-word balanced corpus of written Japanese. Designed to represent the breadth of contemporary written Japanese through random sampling across genres.
- **Creator:** NINJAL (National Institute for Japanese Language and Linguistics). Corpus compilation started in 2006, publicly released in 2011.
- **Date:** Materials from 1976–2006 (main body: 1986–2006).
- **Size:** 104.3 million words total. The Yomitan frequency dictionary contains ~536k unique words.
- **Data Type:** Books, magazines, newspapers, business reports (white papers), blogs, internet forums (Yahoo! Answers, Yahoo! Blogs), textbooks, legal documents, National Diet minutes.
- **Links:**
  - Official page: https://clrd.ninjal.ac.jp/bccwj/en/
  - Frequency list download: https://clrd.ninjal.ac.jp/bccwj/en/freq-list.html
  - Springer paper (Maekawa et al., 2014): https://link.springer.com/article/10.1007/s10579-013-9261-0
  - Yomitan dict by Kuuube: https://github.com/Kuuuube/yomitan-dictionaries
  - Marv's collection: https://github.com/MarvNC/yomitan-dictionaries
- **Notes:** Available in Short Unit Word (SUW) and Long Unit Word (LUW) formats. Free frequency list available for research/educational use. Full corpus access requires a paid subscription with NINJAL. Online search available via Shonagon (free) and Chunagon (subscription). A "balanced" corpus meaning it uses statistical sampling methods to proportionally represent different text types.

---

## 2. CEJC (Corpus of Everyday Japanese Conversation)

- **Description:** Large-scale corpus of naturally occurring everyday Japanese conversations, including both audio and video data. Designed to capture the diversity of daily spoken language.
- **Creator:** NINJAL. Lead researchers include Hanae Koiso et al. Yomitan frequency dictionary converted by forsakeninfinity (GitHub username).
- **Date:** Recorded approximately April 2016 – 2020. Published March 2022.
- **Size:** 200 hours of speech, 577 conversations, ~2.4 million words, 1,675 total conversants. Corpus design based on a survey of conversational behavior of ~250 adults.
- **Data Type:** Naturally occurring everyday spoken conversations (participants self-recorded their daily conversations).
- **Links:**
  - NINJAL project page: https://www.ninjal.ac.jp/english/research/cr-project/project-3/institute/spoken-language/
  - Frequency list source: https://www2.ninjal.ac.jp/conversation/cejc/cejc-wc.html
  - Yomitan dict by forsakeninfinity: https://github.com/forsakeninfinity/CEJC_yomichan_freq_dict
  - LREC 2022 paper (Koiso et al.): https://aclanthology.org/2022.lrec-1.599/
- **Notes:** Unique among Japanese corpora for including video data alongside audio. Informants recorded their own conversations in natural settings, making this one of the best corpora for real-life spoken Japanese. The frequency list used for Yomitan uses the "overall rank" from the source data.

---

## 3. CSJ (Corpus of Spontaneous Japanese)

- **Description:** World-class spoken language corpus containing a large collection of Japanese spontaneous speech data with rich annotations.
- **Creator:** Jointly developed by NINJAL, NICT (National Institute of Information and Communications Technology), and the Tokyo Institute of Technology.
- **Date:** Developed early 2000s. Currently on 5th edition.
- **Size:** ~650 hours of spontaneous speech, ~7 million words. Core subset: ~45 hours, ~500k words. Yomitan frequency dictionary goes up to ~31,605 frequency.
- **Data Type:** Spontaneous spoken Japanese — primarily academic conference presentations and monologues. Includes orthographic and phonetic transcriptions, POS analysis, dependency structure, prosodic information.
- **Links:**
  - Official page: https://clrd.ninjal.ac.jp/csj/en/
  - Yomitan dict (Maltesaa): https://github.com/Maltesaa/CSJ_and_NWJC_yomitan_freq_dict
  - Marv's collection: https://github.com/MarvNC/yomitan-dictionaries#corpus-of-spontaneous-japanese
- **Notes:** Due to its focus on academic monologues/presentations, the language register skews more formal than everyday conversation (unlike CEJC). Available online and via USB flash drive; frequency list limited in size compared to written corpora. NINJAL licensing restricts direct redistribution.

---

## 4. rspeer/wordfreq

- **Description:** Python library providing word frequency estimates in 40+ languages, combining multiple data sources with outlier mitigation. A snapshot of language usage through approximately 2021. Now "sunsetted" — data will not be updated again.
- **Creator:** Robyn Speer, via a Luminoso project called Exquisite Corpus.
- **Date:** Latest release: v3.0.2 (2022). Data snapshot through ~2021.
- **Size:** Multi-source. "Large" lists cover words appearing at least once per 100 million words. Japanese uses MeCab for tokenization.
- **Data Type:** Wikipedia, subtitles (SUBTLEX), news, books, web (OSCAR), Twitter, Reddit, and other Exquisite Corpus sources.
- **Links:**
  - GitHub: https://github.com/rspeer/wordfreq
  - Sunset explanation: https://github.com/rspeer/wordfreq/blob/master/SUNSET.md
  - Exquisite Corpus: https://github.com/LuminosoInsight/exquisite-corpus
  - Zenodo citation: Robyn Speer. (2022). rspeer/wordfreq: v3.0 (v3.0.2).
  - PyPI: https://pypi.org/project/wordfreq/
- **Notes:** Frequencies use the Zipf scale (logarithmic), precise to within 1%. Methodology drops highest and lowest source for each word and averages the rest, minimizing outlier impact. The author explicitly discontinued the project because LLM-generated "slop" has corrupted web data, and Twitter/Reddit API access has been lost. For Japanese, requires the optional `mecab-python3` dependency. One of the most-cited general-purpose frequency resources, but now frozen in time.

---

## 5. JPDBv2

- **Description:** Frequency dictionary scraped from jpdb.io's large corpus of Japanese entertainment media. JPDBv2 is a significantly expanded version of the original JPDB frequency list.
- **Creator:** Kuuube (GitHub: Kuuuube) created the v2 scraper/dictionary. Original JPDB frequency list by Marv (MarvNC). The jpdb.io site itself is a separate project.
- **Date:** v2 is more recent than the original May 2022 scrape.
- **Size:** ~497k words (JPDBv2). Original JPDB had ~183k. Coverage: 99.99% of jpdb corpus up to rank 25,000; 99.5% up to 70,000; 98.6% up to 100,000.
- **Data Type:** Light novels, visual novels, anime, J-drama, web novels — Japanese entertainment/fiction media.
- **Links:**
  - Kuuube's frequency lookup tool: https://kuuuube.github.io/japanese-word-frequency/
  - Kuuube's Yomitan dictionaries: https://github.com/Kuuuube/yomitan-dictionaries
  - Original JPDB scraper by Marv: https://github.com/MarvNC/jpdb-freq-list
  - jpdb.io: https://jpdb.io/
- **Notes:** Particularly useful for immersion learners consuming fiction media. Notable feature: displays separate frequencies for kanji and kana versions of words (marked with ㋕), letting you see how often a word is written in kanji vs. kana. A caveat: the original JPDB list was limited to JMDict entries and had some missing/incorrect readings (e.g., 経緯 only listed いきさつ, not けいい). JPDBv2 addresses much of this.

---

## 6. CC-100 Japanese

- **Description:** Frequency list derived from the CC-100 dataset, a high-quality monolingual dataset filtered from CommonCrawl web data.
- **Creator:** CC-100 dataset by the research community (used in XLM-R training). Yomitan frequency dictionary created by xydustc (the developer behind arujisho).
- **Date:** CC-100 released ~2020.
- **Size:** Source data: ~70GB of Japanese text. Tokenized to ~900k words; filtered using monolingual dictionaries to ~160k words.
- **Data Type:** Web text (CommonCrawl-sourced, filtered for quality).
- **Links:**
  - CC-100 data: https://data.statmt.org/cc-100/
  - Marv's collection entry: https://github.com/MarvNC/yomitan-dictionaries#cc100
- **Notes:** Tokenized using MeCab (via fugashi) and Sudachi. Very wide coverage due to web origins. Formal/written language tends to rank higher compared to fiction-oriented lists like JPDB. Recommended by several community guides as a good sort dictionary for Yomitan due to its broad, well-differentiated readings.

---

## 7. NINJAL Web Japanese Corpus (NWJC)

- **Description:** Ultra-large-scale web corpus constructed by NINJAL from crawled Japanese websites.
- **Creator:** NINJAL. Key researcher: Masayuki Asahara (GitHub: masayu-a). Asahara et al., 2014.
- **Date:** Project launched 2011, corpus developed ~2014–2017.
- **Size:** ~25.8 billion tokens (per NWJC2Vec paper). KOTONOHA search index contains ~86 million SUWs (a subset).
- **Data Type:** Web-crawled Japanese text.
- **Links:**
  - GitHub: https://github.com/masayu-a/NWJC
  - Yomitan dict (Maltesaa): https://github.com/Maltesaa/CSJ_and_NWJC_yomitan_freq_dict
  - Another frequency dict (uncomputable): https://github.com/uncomputable/frequency-dict
  - Marv's collection entry: https://github.com/MarvNC/yomitan-dictionaries#ninjal-web-japanese-corpus
- **Notes:** One of the largest Japanese corpora by token count. NINJAL's licensing restricts direct redistribution of derived frequency dictionaries — some community tools generate them locally from source data. Searchable via KOTONOHA (NINJAL's cross-corpus search system).

---

## 8. Tsukuba Web Corpus (TWC)

- **Description:** Large-scale corpus of Japanese web text, searchable through the NINJAL-LWP (Lexical Word Profiler) interface.
- **Creator:** International Student Center, University of Tsukuba, with NINJAL collaboration (NINJAL-LWP tool developed jointly by NINJAL and Lago Institute of Language).
- **Date:** 2013–2021 (copyright notice on the tool).
- **Size:** ~1.1 billion words.
- **Data Type:** Japanese website text.
- **Links:**
  - Official NLT search interface: https://tsukubawebcorpus.jp/en/
  - Headword frequency list available as .xlsx download from the NLT site
- **Notes:** Primarily a collocation and lexical profiling tool rather than a downloadable frequency list. The search tool uses MeCab + IPA Dictionary for morphological analysis. Usage is limited to research and educational purposes.

---

## 9. YouTube Frequency Dictionaries

- **Description:** Domain-specific frequency lists created from manually transcribed YouTube videos.
- **Creator:** @Zetta, @Vexxed, @Anonymous (community members).
- **Date:** Not precisely stated; available as YoutubeFreqV3.
- **Size:** Data from ~40k manually transcribed YouTube videos. 16 domain-specific lists. Frequency goes up to around 20,000.
- **Data Type:** YouTube video transcripts (spoken Japanese, various domains).
- **Links:**
  - Marv's collection entry: https://github.com/MarvNC/yomitan-dictionaries#youtube-frequency-dictionaries
- **Notes:** Due to the limited size of the original dataset, frequencies should not be directly compared with larger corpora. Still useful for gauging relative word commonality in conversational/spoken YouTube Japanese.

---

## 10. OhTalkWho オタク Frequency Dictionaries

- **Description:** A collection of kanji/word frequency lists derived from Japanese subtitles on various media platforms.
- **Creator:** Dave Doebrick (YouTube: OhTalkWho オタク, Twitter: @DaveDoeb).
- **Date:** Netflix list published ~2019.
- **Size:** Netflix list: 53 million total kanji occurrences.
- **Data Type:** Multiple lists from different sources:
  - Netflix (Japanese subtitles from Netflix Japan)
  - Top 100 Shonen manga/anime
  - Top 100 Slice of Life
  - Novel 5k
  - Visual Novels
- **Links:**
  - Netflix list video: https://www.youtube.com/watch?v=DwJWld8hW0M
  - Google Drive download: https://drive.google.com/file/d/1qHEfYHXjEp83i6PxxMlSxluFyQg2W8Up/view
  - Marv's collection: https://github.com/MarvNC/yomitan-dictionaries (under OhTalkWho section)
- **Notes:** Created using CB's Japanese Text Analysis Tool (SourceForge). The Netflix list was created by processing all Japanese subtitles available on Netflix Japan at the time. Primarily kanji frequency (not word frequency like most others). Useful for prioritizing which kanji to learn for media consumption.

---

## 11. Innocent Corpus

- **Description:** Frequency list based on a large collection of Japanese novels. Distributed with Yomichan/Yomitan.
- **Creator:** cb4960 (Koohii forum username). Rank-based version by Marv (MarvNC).
- **Date:** Original list predates 2019 (Koohii forum thread archived March 2019).
- **Size:** 5,000+ novels. ~285k word entries (Innocent Ranked), ~280k entries total. Also has a kanji frequency version (~6,430 kanji).
- **Data Type:** Japanese novels (fiction).
- **Links:**
  - Original Koohii thread (archived): https://web.archive.org/web/20190309073023/https://forum.koohii.com/thread-9459.html#pid168613
  - Marv's ranked version: https://github.com/MarvNC/yomitan-dictionaries
  - Kuuube's lookup tool: https://kuuuube.github.io/japanese-word-frequency/
- **Notes:** A known weakness is that it does not differentiate based on reading — all readings of a term show the same frequency value. The original corpus is occurrence-based; Marv's "Innocent Ranked" version reorders by rank. The source/provenance of the underlying novels is not fully documented. Widely used in the Yomichan/Yomitan community as a general-purpose fiction frequency reference.

---

## 12. Anacreon's Frequency Dictionaries

- **Description:** A set of frequency dictionaries for Yomichan with a normalized frequency scale (0 = most frequent, 100 = least frequent).
- **Creator:** Anacreon (GitLab: anacreondjt).
- **Date:** ~2019–2020.
- **Size:** Varies per list.
- **Data Type:** Multiple sub-lists:
  - Visual Novels (from vnstats/wareya)
  - Narou (from wareya's analysis of top 300 Narou stories)
  - BCCWJ2 (reprocessed BCCWJ Long Unit Word data)
- **Links:**
  - Documentation: https://anacreondjt.gitlab.io/docs/freq/
  - Marv's collection entry: https://github.com/MarvNC/yomitan-dictionaries#anacreons-frequency-dictionaries
- **Notes:** Uses a distinctive 0–100 scale where the number represents a percentile-like position on a word frequency curve. The VN and Narou lists are derived from wareya's jpstats data (see Shoui/wareya entry below). BCCWJ2 is based on the BCCWJ Long Unit Word list.

---

## 13. Shoui Dictionaries Collection (Misc Frequency Lists)

- **Description:** A collection of miscellaneous frequency dictionaries bundled together, covering various media types.
- **Creator:** Shoui (community member). Underlying data from various sources including wareya (for VN and Narou data).
- **Date:** ~2019–2020.
- **Size:** Varies per list.
- **Data Type:** Includes:
  - Anime & J-drama
  - Narou Freq (top 300 Narou web novels, by wareya)
  - Novels
  - VN Freq v2 (visual novels)
  - Wikipedia v2
  - 国語辞典 (monolingual dictionary-based)
  - Nier (game-specific)
- **Links:**
  - Source collection: https://anacreondjt.gitlab.io/docs/freq/
  - Wareya VN stats: http://wiki.wareya.moe/Stats
  - Wareya Narou stats: http://wiki.wareya.moe/Narou
  - jpstats GitHub (wareya): https://github.com/wareya/jpstats
  - Narou frequency lists: https://github.com/wareya/jpstats/tree/master/narou
- **Notes:** The VN frequency list is based on analysis of 100+ visual novel script dumps (30+ million words total in the VN corpus). Wareya's tools use Kuromoji for word segmentation. Wareya notes these are hobbyist analyses with no quality guarantees. The Narou list covers the top 300 stories from 小説家になろう (Shousetsuka ni Narou), a popular Japanese web novel platform.

---

## 14. Japanese Like a Breeze (Anime Frequency List)

- **Description:** A word frequency list computed from anime subtitle/sentence data.
- **Creator:** Joe (author of the Japanese Like a Breeze / Jlab project).
- **Date:** Published September 2020.
- **Size:** ~2 million sentences from anime/dorama Anki decks (sourced from japanesedecks.blogspot.com).
- **Data Type:** Anime and dorama subtitles/sentences.
- **Links:**
  - Blog post with methodology: https://www.japanese-like-a-breeze.com/computing-a-word-frequency-list-based-on-anime/
  - Project site: https://www.japanese-like-a-breeze.com/
- **Notes:** Uses MeCab + ipadic and a C++ port of Jisho.org's parser for tokenization. The author acknowledges limitations: parsing errors are common with slang/sloppy speech, and the dictionary-based parser sometimes treats multi-word expressions as single entries (e.g., ような instead of よう な). Primarily focused on the top ~2k words for the author's own project needs.

---

## 15. University of Leeds Corpus

- **Description:** Multilingual corpora developed by the Centre for Translation Studies at the University of Leeds, including a Japanese internet corpus and an English-Japanese parallel corpus.
- **Creator:** Centre for Translation Studies, University of Leeds. Notably Serge Sharoff and colleagues.
- **Date:** Corpora collected ~2005 and onward.
- **Size:** Japanese internet corpus size not precisely documented for the Japanese portion. A derived list of ~44,998 most common Japanese words exists (see hingston's GitHub).
- **Data Type:** Web-crawled Japanese text, plus an English-Japanese parallel corpus of Yomiuri newspaper data (in-house only).
- **Links:**
  - Main corpus page: http://corpus.leeds.ac.uk/
  - Resources page: https://www.latl.leeds.ac.uk/resources/corpora-and-corpus-tools/
  - Wiktionary references: https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Japanese
  - Derived word list (hingston): https://github.com/hingston/japanese
  - Corpus tools: http://corpus.leeds.ac.uk/tools/
- **Notes:** The corpora are noted as "temporarily unavailable outside the University of Leeds" as of recent checks. Frequency lists derived from these corpora are available on Wiktionary under CC BY-2.5. The Japanese corpus uses MeCab for tokenization.

---

## 16. JLPT Vocab Frequency

- **Description:** Frequency dictionary based on JLPT (Japanese Language Proficiency Test) vocabulary levels.
- **Creator:** stephenmk (extracted from yomichan-jlpt-vocab dictionary). Distributed via Marv's collection.
- **Date:** Not precisely dated.
- **Size:** Covers JLPT N5 through N1 vocabulary.
- **Data Type:** JLPT test vocabulary organized by level.
- **Links:**
  - Marv's collection: https://github.com/MarvNC/yomitan-dictionaries#jpdicts-frequencies
- **Notes:** Not a corpus-based frequency list in the traditional sense — it reflects vocabulary levels as defined by the JLPT exam rather than naturally observed frequencies. Useful for test preparation and as a rough proficiency-level indicator.

---

## 17. JPDict Frequencies

- **Description:** Frequency data derived from the jiten.moe site, which provides statistics on Japanese media.
- **Creator:** jiten.moe site owner.
- **Date:** Ongoing.
- **Size:** Not precisely documented.
- **Data Type:** Japanese media (stats from jiten.moe's analyzed content).
- **Links:**
  - Marv's collection entry: https://github.com/MarvNC/yomitan-dictionaries#jpdicts-frequencies
  - jiten.moe: https://jiten.moe
- **Notes:** Provides Anki decks and vocab lists in addition to frequency data. A separate resource from JLPT-based frequency.

---

## 18. Novels Frequency List (Kuuube)

- **Description:** A frequency list derived from 10,000+ Japanese novels.
- **Creator:** Available via Kuuube's frequency lookup tool.
- **Date:** Not precisely documented.
- **Size:** ~270k words from 10,000+ novels.
- **Data Type:** Japanese novels (fiction).
- **Links:**
  - Lookup: https://kuuuube.github.io/japanese-word-frequency/
- **Notes:** Distinct from the Innocent Corpus (which uses 5,000+ novels). The larger novel count may provide broader coverage.

---

## 19. Aozora Bunko Frequency

- **Description:** Frequency dictionary based on the Aozora Bunko (青空文庫), Japan's public-domain digital library.
- **Creator:** Data collected by vrtm; Yomitan conversion by Marv (MarvNC).
- **Date:** Not precisely dated.
- **Size:** ~120k words. Also has a kanji frequency version (~8k kanji).
- **Data Type:** Public-domain Japanese literature (Aozora Bunko — primarily pre-1953 works whose copyrights have expired).
- **Links:**
  - Data source: https://vtrm.net/japanese/kanji-jukugo-frequency/en
  - Aozora Bunko: https://www.aozora.gr.jp/
  - Marv's collection: https://github.com/MarvNC/yomitan-dictionaries
- **Notes:** Due to the methodology used, this dictionary does not cover words with kana in them, but it covers many rare 熟語 (jukugo) not found in other frequency lists. Useful as a supplement for classical/literary vocabulary.

---

## 20. chriskempson's Japanese Subtitles Frequency Lists

- **Description:** Word frequency and kanji frequency lists derived from Japanese subtitle files for drama, anime, and films.
- **Creator:** Chris Kempson (GitHub: chriskempson).
- **Date:** Not precisely dated.
- **Size:** Generated from 12,277 subtitle files. Produces both a word frequency report and a kanji frequency report.
- **Data Type:** Japanese subtitles from drama, anime, and films (sourced from Matchoo95/JP-Subtitles).
- **Links:**
  - GitHub: https://github.com/chriskempson/japanese-subtitles-word-kanji-frequency-lists
  - Source subtitles: https://github.com/Matchoo95/JP-Subtitles
- **Notes:** Generated using JParser and cb's Japanese Text Analysis Tool. Word frequency report includes: occurrence count, word, frequency group, frequency rank, percentage, cumulative percentage, and part-of-speech. MIT licensed.

---

## 21. hermitdave/FrequencyWords (OpenSubtitles)

- **Description:** Frequency word lists for many languages generated from the OpenSubtitles corpus.
- **Creator:** Hermit Dave (GitHub: hermitdave). Blog: https://invokeit.wordpress.com/frequency-word-lists/
- **Date:** Lists generated from OpenSubtitles 2016 and 2018 datasets.
- **Size:** Provides top 50k word lists per language. Japanese included.
- **Data Type:** Movie and TV subtitles (OpenSubtitles corpus).
- **Links:**
  - GitHub: https://github.com/hermitdave/FrequencyWords/
  - Blog: https://invokeit.wordpress.com/frequency-word-lists/
  - OpenSubtitles 2018 source: http://opus.nlpl.eu/OpenSubtitles2018.php
- **Notes:** Format is `{word} {occurrence_count}`. Code is MIT licensed; content is CC-BY-SA-4.0. Widely reused by other projects including Wikipedia and autocomplete keyboards. Covers dozens of languages.

---

## 22. IlyaSemenov/wikipedia-word-frequency

- **Description:** Word frequency data generated by processing Wikipedia article dumps using wikiextractor.
- **Creator:** Ilya Semenov (GitHub: IlyaSemenov).
- **Date:** Pre-generated results available; script can be re-run on latest dumps.
- **Size:** For English: ~2.7 million unique words (appearing in at least 3 articles). Japanese results also included.
- **Data Type:** Wikipedia articles (all wiki articles for a given language).
- **Links:**
  - GitHub: https://github.com/IlyaSemenov/wikipedia-word-frequency
  - Cleaned version by adno: https://github.com/adno/wikipedia-word-frequency-clean
- **Notes:** Methodology: strips punctuation, normalizes unicode, discards words containing digits, only includes words appearing in 3+ different articles. Results provided for ~20 languages including Japanese. MIT licensed. The adno fork provides a cleaned version with additional filtering.

---

## Additional Resources

These remaining links are aggregation pages or tools rather than standalone frequency lists:

| Resource                    | Link                                                                     | Notes                                                                                                                   |
| --------------------------- | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| Wiktionary frequency lists  | https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Japanese       | Aggregation page linking to frequency lists from Leeds, wordfreq, Kelly project, and others                             |
| vrtm kanji/jukugo frequency | https://vtrm.net/japanese/kanji-jukugo-frequency/en                      | Kanji and jukugo frequency tool based on Aozora Bunko data (source data for the Aozora Bunko frequency entry #19 above) |
| Google Drive collection     | https://drive.google.com/drive/folders/1g1drkFzokc8KNpsPHoRmDJ4OtMTWFuXi | Community-shared collection of various frequency/dictionary files                                                       |

---

## Master Reference

- **MarvNC's Yomitan Dictionaries Hub:** https://github.com/MarvNC/yomitan-dictionaries — The central community repository for Yomitan frequency dictionaries and other Japanese dictionaries. Best starting point for downloads.
- **Kuuube's Yomitan Dictionaries:** https://github.com/Kuuuube/yomitan-dictionaries — Additional Yomitan dictionaries including JPDBv2 and BCCWJ combined versions.
- **Kuuube's Frequency Lookup Tool:** https://kuuuube.github.io/japanese-word-frequency/ — Web tool for looking up word frequency across multiple lists simultaneously.
