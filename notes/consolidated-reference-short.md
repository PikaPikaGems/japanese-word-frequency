**CEJC (Corpus of Everyday Japanese Conversation)**

- **Short Description**: Balanced corpus of real everyday spoken Japanese (audio/video).
- **Creator**: NINJAL (Hanae Koiso et al.).
- **Publish/Collection Date**: Recorded Apr 2016–2020; paper Mar 2022.
- **Data Analyzed**: 200 hours, 577 conversations, ~2.4M words, 1,675 speakers.
- **Dataset Type**: Naturally occurring conversations (balanced demographics).
- **Links**: Paper https://aclanthology.org/2022.lrec-1.599/; Yomitan dict https://github.com/forsakeninfinity/CEJC_yomichan_freq_dict; NINJAL context via BCCWJ.
- **Notes**: Includes video; first large-scale with social context.

**rspeer/wordfreq**

- **Short Description**: Aggregated multi-source word frequencies (40+ languages).
- **Creator**: Robyn Speer (Luminoso).
- **Publish/Collection Date**: Snapshot to ~2021.
- **Data Analyzed**: Large aggregated corpora (Japanese: millions of tokens).
- **Dataset Type**: Wikipedia, subtitles, news, books (Google Ngrams), web (OSCAR), Twitter, Reddit.
- **Links**: https://github.com/rspeer/wordfreq; Exquisite Corpus https://github.com/LuminosoInsight/exquisite-corpus.
- **Notes**: MeCab tokenized; Zipf-scaled; 'large' Japanese list available. (Verified; no LREC 2022 link.)

**JPDBv2**

- **Short Description**: Media immersion frequency list (readings separated).
- **Creator**: JPDB.io (Yomitan conversion: Kuuube).
- **Publish/Collection Date**: Scraped May 2022; updated May 2024.
- **Data Analyzed**: ~497k words (JPDB base ~183k entries).
- **Dataset Type**: Light novels, visual novels, anime, J-dramas, web novels.
- **Links**: https://kuuuube.github.io/japanese-word-frequency/; JPDB https://jpdb.io/; MarvNC repo.
- **Notes**: JMDict-limited; strong for immersion media.

**CC-100 Japanese**

- **Short Description**: Broad web-crawled frequency list.
- **Creator**: Facebook (CC-100); Yomitan by Seikou (arujisho)/MarvNC.
- **Publish/Collection Date**: ~2020.
- **Data Analyzed**: ~70GB raw → ~900k words filtered to ~160k.
- **Dataset Type**: CommonCrawl web text.
- **Links**: https://data.statmt.org/cc-100/; MarvNC Yomitan.
- **Notes**: MeCab/Sudachi tokenized; primary sort dict for broad coverage.

**Corpus of Spontaneous Japanese (CSJ)**

- **Short Description**: Annotated spontaneous spoken Japanese.
- **Creator**: NINJAL + NICT + Tokyo Tech.
- **Publish/Collection Date**: 1999–2004 (freq lists later).
- **Data Analyzed**: ~7.5M words / 652 hours (Core: ~0.5M).
- **Dataset Type**: Monologues, academic speech (standard Japanese).
- **Links**: https://clrd.ninjal.ac.jp/csj/; MarvNC/Malte conversion.
- **Notes**: POS/prosody annotated; basis for spoken benchmarks.

**BCCWJ (Balanced Corpus of Contemporary Written Japanese)**

- **Short Description**: Japan’s official balanced written corpus.
- **Creator**: NINJAL.
- **Publish/Collection Date**: Texts 1976–2006; released ~2011.
- **Data Analyzed**: 104.3M words.
- **Dataset Type**: Books, magazines, newspapers, blogs, forums, textbooks, legal (balanced).
- **Links**: https://clrd.ninjal.ac.jp/bccwj/en/; Freq lists https://clrd.ninjal.ac.jp/bccwj/en/freq-list.html; MarvNC (LUW recommended).
- **Notes**: LUW/SUW; excellent reading differentiation.

**YouTube Frequency Dictionaries**

- **Short Description**: 16 domain-specific lists from transcribed videos.
- **Creator**: @Zetta, @Vexxed, @Anonymous (via MarvNC).
- **Publish/Collection Date**: ~2020s.
- **Data Analyzed**: 40k manually transcribed YouTube videos.
- **Dataset Type**: YouTube (Vlogs, Gaming, Film/Anime, News, etc.).
- **Links**: MarvNC https://github.com/MarvNC/yomitan-dictionaries (YoutubeFreqV3).
- **Notes**: Separate from OhTalkWho; domain-focused spoken data.

**OhTalkWho オタク Frequency Dictionaries** (Dave Doebrick)

- **Short Description**: Media-specific spoken frequency lists.
- **Creator**: OhTalkWho オタク (Dave Doebrick).
- **Publish/Collection Date**: Netflix list: 30 Apr 2019.
- **Data Analyzed**: Netflix Japan subtitles (~80k files / thousands of episodes; ~53M kanji occurrences per original notes).
- **Dataset Type**: Netflix subtitles + subsets (Top 100 Shonen, Top 100 Slice of Life, Novel 5k, Visual Novels).
- **Links**: Video https://www.youtube.com/watch?v=DwJWld8hW0M; Original lists (MediaFire via video); MarvNC conversion; Drive (original note).
- **Notes**: Text analyzer on subtitles; casual TV speech; covers ~95% at 12k words. Distinct from main YouTube lists.

**NINJAL Web Japanese Corpus (NWJC)**

- **Short Description**: Web-based written corpus.
- **Creator**: NINJAL (Malte conversion).
- **Publish/Collection Date**: Post-BCCWJ.
- **Data Analyzed**: Large web crawl (~106k freq max).
- **Dataset Type**: Japanese websites.
- **Links**: MarvNC repo.
- **Notes**: Complements BCCWJ.

**Tsukuba Web Corpus (TWC)**

- **Short Description**: Massive web corpus + search tool.
- **Creator**: University of Tsukuba + NINJAL.
- **Publish/Collection Date**: Ongoing.
- **Data Analyzed**: 1.1B words.
- **Dataset Type**: Japanese websites.
- **Links**: https://tsukubawebcorpus.jp/en/; https://www.intersc.tsukuba.ac.jp/~kyoten/en/twc/.
- **Notes**: Lexical profiling focus.

**Japanese Like a Breeze**

- **Short Description**: Anime subtitle frequency list.
- **Creator**: Japanese Like a Breeze blog.
- **Publish/Collection Date**: Sep 2020.
- **Data Analyzed**: ~2M anime sentences.
- **Dataset Type**: Anime subtitles (Anki decks).
- **Links**: https://www.japanese-like-a-breeze.com/computing-a-word-frequency-list-based-on-anime/.
- **Notes**: MeCab parsing; slang/name caveats.

**Shoui Dictionaries Collection Misc.**

- **Short Description**: Miscellaneous media frequency lists.
- **Creator**: Shoui (via learnjapanese.moe).
- **Publish/Collection Date**: ~2020s.
- **Data Analyzed**: Varies (e.g., VN Freq v2 from games; Narou top stories).
- **Dataset Type**: Anime & J-drama, Narou web novels, Novels, Wikipedia v2, 国語辞典, Nier.
- **Links**: https://anacreondjt.gitlab.io/docs/freq/; https://learnjapanese.moe/resources/#dictionaries; Wareya http://wiki.wareya.moe/Stats + Narou https://github.com/wareya/jpstats.
- **Notes**: Distinct from Anacreon; includes VN Freq v2.

**Anacreon's Frequency Dictionaries**

- **Short Description**: Percentage-based coverage lists (0–100).
- **Creator**: Anacreon (Shoui site).
- **Publish/Collection Date**: ~2020s.
- **Data Analyzed**: VN >100 games; Narou top 300; BCCWJ2.
- **Dataset Type**: Visual Novels (vnstats), Narou, BCCWJ2.
- **Links**: https://anacreondjt.gitlab.io/docs/freq/; MarvNC; Wareya vnstats http://wiki.wareya.moe/.
- **Notes**: Coverage % (not rank); 95% = mine ≤95; separate from Shoui misc.

**University of Leeds Corpus**

- **Short Description**: Representative written/spoken corpora.
- **Creator**: University of Leeds (Centre for Translation Studies).
- **Publish/Collection Date**: Ongoing.
- **Data Analyzed**: Large scale (unspecified).
- **Dataset Type**: Multi-language incl. Japanese.
- **Links**: https://www.latl.leeds.ac.uk/resources/corpora-and-corpus-tools/.
- **Notes**: Some access-restricted.

**JLPT Vocab Frequency**

- **Short Description**: JLPT level tags as frequency proxy.
- **Creator**: Unofficial lists (Yomitan: yomichan-jlpt-vocab).
- **Publish/Collection Date**: Lists ~10 years old (~2014).
- **Data Analyzed**: Unofficial JLPT vocab.
- **Dataset Type**: JLPT exam guidelines.
- **Links**: MarvNC repo.
- **Notes**: No official JLPT lists; guideline only. Separate from jpDicts.

**jpDicts Frequencies** (JPDict Frequencies)

- **Short Description**: Dictionary-definition corpus frequency.
- **Creator**: Avratzzz.
- **Publish/Collection Date**: Recent (Yomitan).
- **Data Analyzed**: Multiple monolingual dictionaries.
- **Dataset Type**: Dictionary entries (e.g., 大辞林, 広辞苑).
- **Links**: MarvNC repo.
- **Notes**: Not true corpus; useful for dictionary readers. Separate from JLPT.

**Innocent Corpus**

- **Short Description**: Ranked novel frequency.
- **Creator**: Koohii forum (5000+ novels); MarvNC ranked version.
- **Publish/Collection Date**: ~2010s.
- **Data Analyzed**: 5000+ novels.
- **Dataset Type**: Fiction novels.
- **Links**: MarvNC; Archive https://web.archive.org/web/20190309073023/https://forum.koohii.com/thread-9459.html.
- **Notes**: Occurrence-based; no reading split.

All verified/expanded via primary sources (MarvNC GitHub README, YouTube video, Anacreon gitlab, official NINJAL sites, papers). No incorrect merges; each collection now distinct. Prioritize BCCWJ/CSJ for general use, JPDB/YouTube/OhTalkWho for media immersion.
