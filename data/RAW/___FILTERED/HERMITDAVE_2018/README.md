# HERMITDAVE 2018 — OpenSubtitles Japanese Word Frequency

## Source
- **GitHub:** https://github.com/hermitdave/FrequencyWords/
- **Blog:** https://invokeit.wordpress.com/frequency-word-lists/
- **OpenSubtitles 2018 source:** http://opus.nlpl.eu/OpenSubtitles2018.php

## Description
Japanese word frequency list generated from the OpenSubtitles 2018 corpus — a large collection of movie and TV subtitles.

The 2018 dataset is split into two files:
- `ja_ignored.txt` (~81,698 entries): High-frequency words (filtered/separated during generation). Starts with い (749k occurrences), の, は, て, た...
- `ja_full.txt` (~34,504 entries): Remaining words not captured in ignored. Starts with 、(148k), 。, 何...

Both files are combined and sorted by count descending to produce the full ranked list.

Format of each file: `word occurrence_count` (space-separated, no header).

## License
Code: MIT. Content: CC-BY-SA-4.0.

## DATA.csv
Top 25,000 words by occurrence count (combining both source files). Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
