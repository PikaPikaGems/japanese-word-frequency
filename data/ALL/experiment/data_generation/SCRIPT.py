import csv
import glob
import os

csv.field_size_limit(10_000_000)

# Paths
BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
CEJC_FILE = os.path.join(ROOT, "data", "CEJC", "CONSOLIDATED_UNIQUE.csv")
FILTERED_DIR = os.path.join(ROOT, "data", "RAW", "___FILTERED")
JPDB_FILE = os.path.join(ROOT, "data", "JPDBV2", "jpdb_v2.2_freq_list_2024-10-13.csv")
OUTPUT_FILE = os.path.join(BASE, "consolidated_anchor_CEJC.csv")

# Load JPDB v2: term -> kana reading (keep the most frequent reading per term)
# Only store where reading differs from term (i.e. kanji forms that have a kana fallback)
kana_fallback = {}
with open(JPDB_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        term = row["term"]
        reading = row["reading"]
        freq = int(row["frequency"])
        if term == reading:
            continue
        if term not in kana_fallback or freq < kana_fallback[term][1]:
            kana_fallback[term] = (reading, freq)
kana_fallback = {term: reading for term, (reading, _) in kana_fallback.items()}

# Load CEJC data — preserves word order
cejc_rows = []
cejc_columns = []
with open(CEJC_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    cejc_columns = [c for c in reader.fieldnames if c != "word"]
    for row in reader:
        cejc_rows.append(row)

words_in_order = [row["word"] for row in cejc_rows]
word_index = {w: i for i, w in enumerate(words_in_order)}

# Load each DATA.csv source
source_dirs = sorted(glob.glob(os.path.join(FILTERED_DIR, "*", "DATA.csv")))
sources = {}  # source_name -> {word: rank}
source_names = []
for path in source_dirs:
    name = os.path.basename(os.path.dirname(path))
    source_names.append(name)
    word_rank = {}
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            word = row["WORD"]
            rank = int(row["FREQUENCY_RANKING"])
            if word not in word_rank or rank < word_rank[word]:
                word_rank[word] = rank
    sources[name] = word_rank

def lookup(source, word):
    if word in source:
        return source[word]
    reading = kana_fallback.get(word)
    if reading and reading in source:
        return source[reading]
    return -1

# Write consolidated.csv
out_columns = ["word"] + cejc_columns + source_names
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(out_columns)
    for row in cejc_rows:
        word = row["word"]
        cejc_vals = [row[c] for c in cejc_columns]
        source_vals = [lookup(sources[s], word) for s in source_names]
        writer.writerow([word] + cejc_vals + source_vals)

print(f"Written {len(cejc_rows)} rows to {OUTPUT_FILE}")
print(f"Columns: word + {len(cejc_columns)} CEJC ranks + {len(source_names)} source ranks")
print(f"Sources: {', '.join(source_names)}")
