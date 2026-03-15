# YOUTUBE_FREQ_V3 — YouTube Japanese Video Frequency V3 (MarvNC)

## Source
- **MarvNC collection:** https://github.com/MarvNC/yomitan-dictionaries#youtube-frequency-dictionaries
- **Creators:** @Zetta, @Vexxed, @Anonymous (community members)

## Description
Version 3 of the YouTube Japanese word frequency list, created from ~40,000 manually transcribed YouTube videos covering 16 different domains of spoken Japanese. Available via the MarvNC Yomitan dictionaries collection. Contains ~187k unique word entries in the upstream source; DATA.csv is capped at the top 25,000.

Note: "Due to the limited size of the original dataset, frequencies should not be directly compared with larger corpora. Still useful for gauging relative word commonality in conversational/spoken YouTube Japanese."

See also: `YOUTUBE_FREQ` — the older, smaller version (56k entries) from the Shoui collection.

## Format (Yomitan JSON)
Single `term_meta_bank_1.json` — each entry: `[word, "freq", rank_as_string]` (rank stored as string, e.g. `"1"`).

## DATA.csv
Top 25,000 words by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
