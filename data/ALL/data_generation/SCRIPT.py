import csv
import glob
import os
import sys

csv.field_size_limit(10_000_000)

# Paths
BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
sys.path.insert(0, ROOT)

from utils import JapaneseLookup  # noqa: E402

CEJC_FILE = os.path.join(ROOT, "data", "CEJC", "CONSOLIDATED_UNIQUE.csv")
FILTERED_DIR = os.path.join(ROOT, "data", "RAW", "___FILTERED")
JPDB_FILE = os.path.join(ROOT, "data", "JPDBV2", "jpdb_v2.2_freq_list_2024-10-13.csv")
CEJC_TSV  = os.path.join(ROOT, "data", "CEJC", "2_cejc_frequencylist_suw_token.tsv")
RSPEER_FILE = os.path.join(ROOT, "data", "RSPEER", "top_25000_japanese.csv")
OUTPUT_FILE = os.path.join(BASE, "..", "CEJC_anchor", "consolidated.csv")

jlookup = JapaneseLookup(JPDB_FILE, CEJC_TSV)

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

EXCLUDED_SOURCES = {"KOKUGOJITEN", "MONODICTS", "DD2_MIGAKU_NOVELS", "BCCWJ"}

# Load each DATA.csv source
source_dirs = sorted(glob.glob(os.path.join(FILTERED_DIR, "*", "DATA.csv")))
sources = {}  # source_name -> {word: rank}
source_names = []
for path in source_dirs:
    name = os.path.basename(os.path.dirname(path))
    if name in EXCLUDED_SOURCES:
        continue
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

# Load RSPEER (row position = rank; higher zipf_frequency = more frequent = earlier row)
rspeer_ranks = {}
with open(RSPEER_FILE, newline="", encoding="utf-8") as f:
    for rank, row in enumerate(csv.DictReader(f), start=1):
        word = row["word"]
        if word not in rspeer_ranks:
            rspeer_ranks[word] = rank
source_names.append("RSPEER")
sources["RSPEER"] = rspeer_ranks

# Write consolidated.csv
out_columns = ["word", "hiragana", "katakana"] + cejc_columns + source_names
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(out_columns)
    for row in cejc_rows:
        word = row["word"]
        hira, kata = jlookup.get_reading(word)
        cejc_vals = [row[c] for c in cejc_columns]
        source_vals = [jlookup.lookup(sources[s], word) for s in source_names]
        writer.writerow([word, hira, kata] + cejc_vals + source_vals)

print(f"Written {len(cejc_rows)} rows to {OUTPUT_FILE}")
print(f"Columns: word + hiragana + katakana + {len(cejc_columns)} CEJC ranks + {len(source_names)} source ranks")
print(f"Sources: {', '.join(source_names)}")

def _report_kana_coverage(output_file):
    missing = 0
    total   = 0
    with open(output_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            if row["hiragana"] == "-":
                missing += 1
    pct = missing / total * 100 if total else 0
    print(f"Kana coverage: {total - missing}/{total} words have a reading ({missing} missing, {pct:.1f}%)")

_report_kana_coverage(OUTPUT_FILE)
