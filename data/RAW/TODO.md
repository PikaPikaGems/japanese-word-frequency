I have gotten a data dump (frequency rankings of japanese words based on various corporas) of various datasets (they come in various forms JSON, CSV, TSV, TXT). It is located in `./data/RAW/*` folder

They are from the following sources:

- https://github.com/Kuuuube/yomitan-dictionaries
- https://github.com/MarvNC/yomitan-dictionaries
- https://github.com/IlyaSemenov/wikipedia-word-frequency
- https://github.com/adno/wikipedia-word-frequency-clean
- https://github.com/hermitdave/FrequencyWords/
- https://github.com/chriskempson/japanese-subtitles-word-kanji-frequency-lists
- https://github.com/rspeer/wordfreq
- https://drive.google.com/drive/folders/1g1drkFzokc8KNpsPHoRmDJ4OtMTWFuXi
- https://drive.google.com/drive/folders/1xURpMJN7HTtSLuVs9ZtIbE7MDRCdoU29
- https://drive.google.com/file/d/1qHEfYHXjEp83i6PxxMlSxluFyQg2W8Up

1. You may read the README.md of the above github repositories to understand the structure and content of the datasets.
2. You may also read this consolidated reference markdowns I have compiled for further context. (See markdowns here: notes/consolidated-reference-short.md, notes/consolidated-reference-verbose.md )
3. The files you create should be in './data/RAW/\_\_\_FILTERED' folder. For each data set create create a folder (Name as you see fit) containing 3 files

- README.md
- DATA.csv
- SCRIPT.py

4. The README.md contains a brief description and relevant information about the data corpus
5. SCRIPT.py contains the script that will generate DATA.csv
6. The DATA.csv contains only the top 25,000 words (filter them out) of each dataset. It has only two columns: WORD, FREQUENCY RANKING.
7. Always self verify if what you are doing is correct.
8. If you have questions please let me know.
