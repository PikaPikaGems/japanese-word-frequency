# Dataset Catalog

> **Column IDs** match column names in `consolidated.csv` and folder names under `data/RAW/___FILTERED/`.
> CEJC columns are lowercase (`cejc_*`). All other source columns are uppercase.
> `-1` in any cell means the word was absent or ranked outside the dataset's top entries.
> All datasets are capped at top 25,000 entries.

---

## ⭐ Highlighted (Shortlisted)

| Column ID              | Source          | Description                                                                                                    |
| ---------------------- | --------------- | -------------------------------------------------------------------------------------------------------------- |
| `RSPEER`               | rspeer/wordfreq | Multi-source aggregate (Wikipedia, subtitles, news, books, web, Twitter/Reddit). Discontinued 2021; data frozen. |
| `cejc_combined_rank`   | NINJAL CEJC     | Everyday spoken Japanese — all conversations combined.                                                         |
| `cejc_small_talk_rank` | NINJAL CEJC     | Everyday spoken Japanese — casual small talk only (雑談).                                                      |
| `BCCWJ_LUW`            | NINJAL BCCWJ    | Japan's official balanced written corpus (104M words, 1976–2006), Long Unit Word tokenization. Compound words treated as single units. |
| `BCCWJ_SUW`            | NINJAL BCCWJ    | Same BCCWJ corpus, Short Unit Word tokenization. Top ranks dominated by particles and auxiliaries.             |
| `CC100`                | CommonCrawl     | Filtered Japanese web text (~2020, ~70 GB). Broad contemporary vocabulary.                                     |
| `MALTESAA_NWJC`        | NINJAL NWJC     | Web Japanese Corpus (~25.8B tokens, crawled 2014–2017). More informal than BCCWJ_LUW.                          |
| `MALTESAA_CSJ`         | NINJAL CSJ      | Corpus of Spontaneous Japanese — all sub-corpora combined (~7M words). Recorded 1999–2003. Primarily formal academic speech. |
| `JITEN_GLOBAL`         | jiten.moe       | All jiten.moe media categories combined (~430k source entries).                                                |
| `JITEN_DRAMA`          | jiten.moe       | Japanese drama frequency (~217k source entries). Live-action drama register.                                   |
| `ANIME_JDRAMA`         | Shoui           | Anime and J-drama subtitles (~100k entries). Widely cited in the community (TheMoeWay, Refold).                |
| `YOUTUBE_FREQ_V3`      | MarvNC          | Manually transcribed YouTube videos across 16 spoken domains (~187k entries). Supersedes `YOUTUBE_FREQ`.       |
| `NETFLIX`              | Shoui           | Netflix Japan subtitles, anime + drama + live-action (~129k entries). Broad coverage, includes proper names.   |
| `DD2_MORPHMAN_NETFLIX` | Dave Doebrick 2 | Netflix subtitles, Morphman/UniDic format, **proper names excluded** (~105k entries). Cleaner lemmatization.   |
| `WIKIPEDIA_V2`         | MarvNC / Shoui  | Community-built Wikipedia frequency dictionary (~850k source entries). Broad coverage.                         |
| `ADNO`                 | ADNO project    | Wikipedia (Oct 2022 dump), carefully filtered. Well-maintained fork of IlyaSemenov's project.                  |
| `DD2_MORPHMAN_SOL`     | Dave Doebrick 2 | Slice-of-Life anime, Morphman/UniDic format (~45k entries).                                                    |

---

## Academic / Research Corpora

### CEJC — Corpus of Everyday Japanese Conversation

Recorded daily conversations by 1,675 speakers (April 2016–2020). ~2.4M words across 577 conversations.
**Note:** Below rank ~5,000 rankings become noisy (8,831 words tie at rank 20,704).

| Column ID                     | Japanese       | Description                                     |
| ----------------------------- | -------------- | ----------------------------------------------- |
| `cejc_combined_rank`          | 全体           | All conversations combined. ✅ **Shortlisted.** |
| `cejc_small_talk_rank`        | 雑談           | Casual small talk. ✅ **Shortlisted.**          |
| `cejc_consultation_rank`      | 相談           | Counseling / advice conversations               |
| `cejc_meeting_rank`           | 会議           | Formal meetings                                 |
| `cejc_class_rank`             | 授業           | Classroom and lesson settings                   |
| `cejc_outdoors_rank`          | 屋外活動       | Outdoor activity conversations                  |
| `cejc_school_rank`            | 学校生活       | School life                                     |
| `cejc_transportation_rank`    | 交通機関       | Conversations on public transportation          |
| `cejc_public_commercial_rank` | 公共・商業施設 | Shops, public facilities, service interactions  |
| `cejc_home_rank`              | 家庭生活       | Home and domestic conversations                 |
| `cejc_indoors_rank`           | 屋内施設       | Indoor non-home settings                        |
| `cejc_workplace_rank`         | 職場           | Workplace conversations                         |
| `cejc_male_rank`              | —              | Speech produced by male speakers                |
| `cejc_female_rank`            | —              | Speech produced by female speakers              |

### CSJ — Corpus of Spontaneous Japanese

~652 hours of speech, ~7M words. Recorded 1999–2003. Primarily **academic monologues and formal presentations** — not casual speech.

| Column ID                    | Japanese     | Description                                                 |
| ---------------------------- | ------------ | ----------------------------------------------------------- |
| `MALTESAA_CSJ`               | 全体         | Overall CSJ — all sub-corpora combined. ✅ **Shortlisted.** |
| `MALTESAA_CSJ_DOKWA_GAKKAI`  | 独話・学会   | Academic conference presentations (monologue)               |
| `MALTESAA_CSJ_DOKWA_MOGI`    | 独話・模擬   | Simulated / practice speeches (monologue)                   |
| `MALTESAA_CSJ_DOKWA_ROUDOKU` | 独話・朗読   | Prepared text read aloud — first reading (monologue)        |
| `MALTESAA_CSJ_DOKWA_SAIRO`   | 独話・再朗読 | Prepared text read aloud — second reading (monologue)       |
| `MALTESAA_CSJ_DOKWA_SONOTA`  | 独話・その他 | Other monologue types                                       |
| `MALTESAA_CSJ_TAIKA_JIYU`    | 対話・自由   | Unstructured free-form dialogue                             |
| `MALTESAA_CSJ_TAIKA_KADAI`   | 対話・課題   | Task-based structured dialogue                              |
| `MALTESAA_CSJ_TAIKA_MOGI`    | 対話・模擬   | Simulated / role-play dialogue                              |

### Other Academic

| Column ID             | Source                | Description                                                                                                                                                                   |
| --------------------- | --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `RSPEER`              | rspeer/wordfreq       | Multi-source aggregate (Wikipedia, subtitles, news, books, web, Twitter/Reddit). ~2021 snapshot, project discontinued. Robust to single-corpus bias. ✅ **Shortlisted.**      |
| `BCCWJ_LUW`           | NINJAL BCCWJ          | Balanced written corpus (104.3M words, 1976–2006), Long Unit Word tokenization. Compound words treated as single units. ✅ **Shortlisted.**                                   |
| `BCCWJ_SUW`           | NINJAL BCCWJ          | Same BCCWJ corpus, Short Unit Word tokenization. Particles and auxiliaries dominate top ranks. ✅ **Shortlisted.**                                                            |
| `CC100`               | CommonCrawl           | Filtered Japanese web text (~2020). Tokenized with both SudachiPy and MeCab. ✅ **Shortlisted.**                                                                              |
| `MALTESAA_NWJC`       | NINJAL NWJC           | Web Japanese Corpus (~25.8B tokens, crawled 2014–2017). Ranks extend to ~106,762. ✅ **Shortlisted.**                                                                         |
| `HINGSTON`            | Leeds Internet Corpus | Leeds internet corpus from mid-2000s. Severely outdated; internet language has changed dramatically. Low priority compared to CC100 or MALTESAA_NWJC. ⚠️ **Not Recommended.** |
| `KUUUUBE_JMDICT_FREQ` | JMdict / Kuuube       | Derived from JMdict's newspaper frequency annotations, not a raw corpus count. Reflects JMdict editorial decisions about newspaper prominence. ⚠️ **Not Recommended.**        |

---

## JITEN Breakdown

All jiten.moe frequency lists. Regularly maintained and updated.

| Column ID            | Source entries | Description                                                                                                                                                                           |
| -------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `JITEN_GLOBAL`       | ~430k          | All media categories combined. ✅ **Shortlisted.**                                                                                                                                    |
| `JITEN_DRAMA`        | ~217k          | Japanese drama. ✅ **Shortlisted.**                                                                                                                                                   |
| `JITEN_ANIME_V2`     | ~215k          | Anime — direct CSV export. Most recent jiten.moe anime list; use `JITEN_GLOBAL` for broader cross-media coverage.                                                                     |
| `JITEN_ANIME`        | ~257k          | Anime — Yomitan JSON export. Older format.                                                                                                                                            |
| `JITEN_MOVIE`        | ~142k          | Movies                                                                                                                                                                                |
| `JITEN_MANGA`        | ~264k          | Manga                                                                                                                                                                                 |
| `JITEN_NOVEL`        | ~285k          | Novels                                                                                                                                                                                |
| `JITEN_VISUAL_NOVEL` | ~224k          | Visual novels                                                                                                                                                                         |
| `JITEN_WEB_NOVEL`    | ~60k           | Web novels                                                                                                                                                                            |
| `JITEN_NON_FICTION`  | ~89k           | Non-fiction / documentary / educational                                                                                                                                               |
| `JITEN_VIDEO_GAME`   | ~159k          | Video games                                                                                                                                                                           |
| `JITEN_AUDIO`        | ~8,370         | Audio / podcasts. Only ~8,370 entries — very limited signal outside the audio/podcast niche. ⚠️ **Not Recommended.**                                                                  |

---

## Wikipedia

| Column ID            | Source                | Description                                                                                                                                          |
| -------------------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `WIKIPEDIA_V2`       | MarvNC / Shoui        | Community-built Wikipedia frequency dictionary (~850k source entries). Broad coverage. ✅ **Shortlisted.**                                           |
| `ADNO`               | ADNO project          | Wikipedia (Oct 2022 dump), carefully filtered. Well-maintained fork of IlyaSemenov's project. ✅ **Shortlisted.**                                    |
| `HLORENZI_WIKIPEDIA` | hlorenzi / jisho-open | Wikipedia word rankings used by the jisho-open dictionary (~20k entries, all included).                                                              |
| `ILYASEMENOV`        | IlyaSemenov           | Wikipedia (Aug 2022 dump) — uses **document frequency**, not term frequency. Contains HTML entity noise (`amp`, `gt`, `lt`). ⚠️ **Not Recommended.** |

---

## Subtitles and Media

### YouTube

| Column ID         | Description                                                                               |
| ----------------- | ----------------------------------------------------------------------------------------- |
| `YOUTUBE_FREQ_V3` | Manually transcribed YouTube across 16 spoken domains (~187k source). ✅ **Shortlisted.** |
| `YOUTUBE_FREQ`    | Older YouTube transcription dataset (~56k entries). Superseded by V3.                     |

### Netflix

| Column ID              | Format / Tool                    | Description                                                                                                                                       |
| ---------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `NETFLIX`              | cb's Japanese Text Analysis Tool | Shoui's Netflix Japan collection (~129k entries, anime + drama + live-action). Includes proper names. ✅ **Shortlisted.**                         |
| `DD2_MORPHMAN_NETFLIX` | Morphman / UniDic                | Dave Doebrick 2 — Netflix, **proper names excluded** (~105k entries). Cleaner lemmatization. ✅ **Shortlisted.**                                  |
| `DAVE_DOEBRICK`        | cb's Japanese Text Analysis Tool | Dave Doebrick's Netflix collection (2019, ~53M kanji occurrences). Older.                                                                         |
| `DD2_MIGAKU_NETFLIX`   | Migaku                           | Dave Doebrick 2 — Netflix, Migaku format (~102k entries). Same corpus as `DD2_MORPHMAN_NETFLIX`, different format.                                |
| `HERMITDAVE_2016`      | MeCab                            | OpenSubtitles 2016. Known tokenization bug: MeCab splits verbs into morphemes — dictionary-form verbs essentially absent. ⚠️ **Not Recommended.** |
| `HERMITDAVE_2018`      | MeCab                            | OpenSubtitles 2018, combined from two split source files. Same morpheme-splitting issue as `HERMITDAVE_2016`. ⚠️ **Not Recommended.**             |

### Slice of Life

| Column ID          | Format            | Description                                                                            |
| ------------------ | ----------------- | -------------------------------------------------------------------------------------- |
| `DD2_MORPHMAN_SOL` | Morphman / UniDic | Slice-of-Life anime (~45k entries). More consistent lemmatization. ✅ **Shortlisted.** |
| `DD2_YOMICHAN_SOL` | Yomichan          | Slice-of-Life top 100 (~43k entries).                                                  |

### Anime & Drama

| Column ID             | Source                | Description                                                                                                                                                                              |
| --------------------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `JITEN_DRAMA`         | jiten.moe             | Japanese drama frequency (~217k source entries). Live-action drama register. ✅ **Shortlisted.**                                                                                         |
| `ANIME_JDRAMA`        | Shoui                 | Anime and J-drama subtitles (~100k entries). Widely cited in the community. ✅ **Shortlisted.**                                                                                          |
| `HLORENZI_ANIMEDRAMA` | hlorenzi / jisho-open | Anime & drama subtitle rankings used by jisho-open (~100k source, top 25k included). Lightweight cross-check for entertainment subtitle vocabulary.                                      |
| `JITEN_ANIME_V2`      | jiten.moe             | Anime — direct CSV export. Most recent jiten.moe anime list; use `JITEN_GLOBAL` for broader cross-media coverage.                                                                       |
| `JPDB`                | JPDB                  | Anime and games vocabulary from JPDB. Uses surface/inflected forms — conjugated verb forms appear as separate entries. Heavy bias toward JPDB's content catalog. ⚠️ **Not Recommended.** |
| `JLAB`                | JLAB                  | Anime-only source built from ~1.85M Anki flashcards. Parser (Jisho.org C++ + MeCab/ipadic) struggles with slang; rankings below ~2,000 unreliable. ⚠️ **Not Recommended.**               |
| `CHRISKEMPSON`        | Community             | Subtitle corpus (12,277 files) built with older tools. Less curated than Shoui collections, not actively maintained. ⚠️ **Not Recommended.**                                             |

### Shonen

| Column ID                   | Format                  | Description                           |
| --------------------------- | ----------------------- | ------------------------------------- |
| `DD2_MORPHMAN_SHONEN`       | Morphman / UniDic       | Shonen manga/anime (~60k entries).    |
| `DD2_YOMICHAN_SHONEN`       | Yomichan (integer rank) | Shonen top 100 titles (~56k entries). |
| `DD2_YOMICHAN_SHONEN_STARS` | Yomichan (stars format) | Shonen manga/anime (~56k entries).    |

### Other / Miscellaneous

| Column ID | Source    | Description                                                                                  |
| --------- | --------- | -------------------------------------------------------------------------------------------- |
| `H_FREQ`  | Community | Adult (18+) content corpus (~44.7k entries). Highly domain-specific. ⚠️ **Not Recommended.** |

---

## Fiction and Literary

### Novels

| Column ID             | Source                     | Description                                                                                                                      |
| --------------------- | -------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `NOVELS`              | Kuuube                     | 10,000+ contemporary Japanese novels. Largest novel corpus here. Note: punctuation (、。) not filtered — rank 1 is `、`.         |
| `JITEN_NOVEL`         | jiten.moe                  | Novel frequency (~285k source). Compare with `NOVELS` and `INNOCENT_RANKED`.                                                     |
| `DD2_MORPHMAN_NOVELS` | Dave Doebrick 2 / Morphman | Novels from Kindle (~126k entries).                                                                                              |
| `DD2_YOMICHAN_NOVELS` | Dave Doebrick 2 / Yomichan | Novels (~89k entries).                                                                                                           |
| `INNOCENT_RANKED`     | Innocent Corpus            | 5,000+ novels reordered by rank. Older (~2010s). Does not differentiate readings — all kanji variants share one frequency value. |

### Visual Novels and Web Novels

| Column ID            | Source                     | Description                                                                                                                |
| -------------------- | -------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `VN_FREQ`            | Community                  | 100+ visual novel scripts (~30M words). Uses UniDic lemma forms (為る for する).                                           |
| `JITEN_VISUAL_NOVEL` | jiten.moe                  | Visual novels (~224k source).                                                                                              |
| `DD2_YOMICHAN_VN`    | Dave Doebrick 2 / Yomichan | Visual novels (~85k entries).                                                                                              |
| `JITEN_WEB_NOVEL`    | jiten.moe                  | Web novels (~60k source).                                                                                                  |
| `NAROU`              | Hobbyist (Kuromoji)        | Top 300 stories on 小説家になろう. Isekai/fantasy-heavy — genre-specific terms (ギルド, 転生, 異世界) rank unusually high. |

### Miscellaneous Literary

| Column ID           | Source       | Description                                                                                                                                                             |
| ------------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `JITEN_MANGA`       | jiten.moe    | Manga (~264k source). Includes narration text, closer to written style than pure dialogue.                                                                              |
| `JITEN_NON_FICTION` | jiten.moe    | Non-fiction, documentary, educational content (~89k source).                                                                                                            |
| `AOZORA_BUNKO`      | Aozora Bunko | Pre-1953 public-domain literature (Soseki, Akutagawa). **Contains zero hiragana entries by design** — archaic vocabulary and classical grammar. ⚠️ **Not Recommended.** |

### Video Games

| Column ID | Source    | Description                                                                                                                                                                                        |
| --------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `NIER`    | Community | Single game series script (~10,077 entries, entire vocabulary of the NieR games). A `-1` here simply means the word doesn't appear in NieR — no general vocabulary signal. ⚠️ **Not Recommended.** |

---

## ⚠️ Not Recommended

These datasets are included in `consolidated.csv` for completeness but should not be featured or recommended to users on the website.

| Column ID             | Reason not recommended                                                                                                                                                                                                                                           |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `JPDB`                | Uses **surface / inflected forms**, not dictionary-form lemmas — inflected verb forms and conjugations appear as separate "words". Heavy bias toward anime and games (JPDB's content catalog). Poor signal for general vocabulary.                               |
| `AOZORA_BUNKO`        | Pre-1953 public-domain literature (Soseki, Akutagawa). **Contains zero hiragana entries by design** — the dataset only covers kanji compounds. Archaic vocabulary and classical grammar. Misleading `-1` for any kana-form word.                                 |
| `CHRISKEMPSON`        | Subtitle corpus (12,277 files) built with older tools. Less curated than Shoui collections, not actively maintained.                                                                                                                                             |
| `JLAB`                | Anime-only source built from ~1.85M Anki flashcards. The parser (Jisho.org C++ parser + MeCab/ipadic) struggles with slang and informal speech — treats multi-word expressions as single tokens. Rankings below ~2,000 are unreliable.                           |
| `ILYASEMENOV`         | Wikipedia by **document frequency** (how many articles contain the word), not term frequency. Also contains HTML entity noise (`amp`, `gt`, `lt` appear as "words").                                                                                             |
| `HINGSTON`            | Leeds internet corpus from **mid-2000s**. Severely outdated; internet language has changed dramatically. Low priority compared to CC100 or MALTESAA_NWJC.                                                                                                        |
| `KUUUUBE_JMDICT_FREQ` | Derived from JMdict's **newspaper frequency annotations**, not a raw corpus count. Reflects JMdict editorial decisions about newspaper prominence.                                                                                                               |
| `JITEN_AUDIO`         | Only ~8,370 entries — the smallest dataset here. Audio/podcast domain with very limited signal outside that niche.                                                                                                                                               |
| `HERMITDAVE_2016`     | OpenSubtitles 2016. **Known tokenization bug**: MeCab split verbs into morphemes, so dictionary-form verbs (思う, 分かる) essentially don't exist as entries. Single characters like い, っ, て, る appear as "words". `-1` here may be a tokenization artifact. |
| `HERMITDAVE_2018`     | Same morpheme-splitting issue as `HERMITDAVE_2016`. OpenSubtitles 2018, combined from two split source files.                                                                                                                                                    |
| `H_FREQ`              | Adult (18+) content corpus (~44.7k entries). Highly domain-specific; vocabulary skews heavily toward adult content tropes and register.                                                                                                                          |
| `NIER`                | Single game series script (~10,077 entries, entire vocabulary of the NieR games). A `-1` here simply means the word doesn't appear in NieR — no general vocabulary signal.                                                                                       |
