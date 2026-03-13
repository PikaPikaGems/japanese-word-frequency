# YOUTUBE_FREQ — YouTube Japanese Video Frequency (YoutubeFreqV3)

## Source
- **Yomitan dict (MarvNC collection):** https://github.com/MarvNC/yomitan-dictionaries#youtube-frequency-dictionaries
- **Creators:** @Zetta, @Vexxed, @Anonymous (community members)

## Description
Domain-specific word frequency list created from ~40,000 manually transcribed YouTube videos covering 16 different domains of spoken Japanese. Version 3 (YoutubeFreqV3) contains ~187k unique words.

Note from reference notes: "Due to the limited size of the original dataset, frequencies should not be directly compared with larger corpora. Still useful for gauging relative word commonality in conversational/spoken YouTube Japanese."

The frequency represents rank ordering from most to least common in the YouTube subtitle corpus.

## Format (Yomitan JSON)
Single `term_meta_bank_1.json` — each entry: `[word, "freq", rank_as_string]` (rank stored as string, e.g. `"1"`).

## DATA.csv
Top 25,000 words by frequency rank. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
