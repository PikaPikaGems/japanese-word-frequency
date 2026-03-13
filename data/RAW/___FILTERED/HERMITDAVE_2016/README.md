# HERMITDAVE 2016 — OpenSubtitles Japanese Word Frequency

## Source
- **GitHub:** https://github.com/hermitdave/FrequencyWords/
- **Blog:** https://invokeit.wordpress.com/frequency-word-lists/
- **OpenSubtitles 2016 source:** http://opus.nlpl.eu/OpenSubtitles2016.php

## Description
Japanese word frequency list generated from the OpenSubtitles 2016 corpus — a large collection of movie and TV subtitles. Provides top 50,000 most common Japanese words by occurrence count.

Format: `word occurrence_count` (space-separated, no header, pre-sorted by count descending).

Two files are available:
- `ja_50k.txt`: Top 50,000 words (50,000 entries)
- `ja_full.txt`: Complete list (~93,652 entries)

The `ja_50k.txt` file is used here as it already covers the top 50k and our target is the top 25,000.

## License
Code: MIT. Content: CC-BY-SA-4.0.

## DATA.csv
Top 25,000 words by occurrence count. Columns: `WORD`, `FREQUENCY_RANKING` (1 = most frequent).
