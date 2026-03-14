# YOUTUBE_FREQ — YouTube Japanese Video Frequency (Shoui)

## Source
- **Shoui's collection:** https://anacreondjt.gitlab.io/docs/freq/
- **MarvNC collection:** https://github.com/MarvNC/yomitan-dictionaries#youtube-frequency-dictionaries
- **Creators:** @Zetta, @Vexxed, @Anonymous (community members)

## Description
Word frequency list created from manually transcribed Japanese YouTube videos. Part of the Shoui frequency dictionaries collection. Contains ~56k unique word entries.

Note: "Due to the limited size of the original dataset, frequencies should not be directly compared with larger corpora. Still useful for gauging relative word commonality in conversational/spoken YouTube Japanese."

See also: `YOUTUBE_FREQ_V3` — a newer, larger version (187k entries) from the MarvNC collection.

## Format (Yomitan JSON)
Single `term_meta_bank_1.json` — each entry: `[word, "freq", rank_as_string]` (rank stored as string, e.g. `"1"`).

## DATA.csv
Top 25,000 words by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
