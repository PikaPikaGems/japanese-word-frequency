import csv
from wordfreq import top_n_list, word_frequency, zipf_frequency

OUTPUT = "top_25000_japanese.csv"
LANG = "ja"
N = 25000

words = top_n_list(LANG, N)

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["word", "frequency", "zipf_frequency"])
    for word in words:
        freq = word_frequency(word, LANG)
        zipf = zipf_frequency(word, LANG)
        writer.writerow([word, freq, zipf])

print(f"Wrote {len(words)} words to {OUTPUT}")
