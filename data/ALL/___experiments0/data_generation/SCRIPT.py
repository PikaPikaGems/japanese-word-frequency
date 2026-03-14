import csv
import glob
import os

csv.field_size_limit(10_000_000)

# Paths
BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, "..", "..", "..", ".."))
CEJC_FILE = os.path.join(ROOT, "data", "CEJC", "CONSOLIDATED_UNIQUE.csv")
FILTERED_DIR = os.path.join(ROOT, "data", "RAW", "___FILTERED")
JPDB_FILE = os.path.join(ROOT, "data", "JPDBV2", "jpdb_v2.2_freq_list_2024-10-13.csv")
CEJC_TSV  = os.path.join(ROOT, "data", "CEJC", "2_cejc_frequencylist_suw_token.tsv")
RSPEER_FILE = os.path.join(ROOT, "data", "RSPEER", "top_25000_japanese.csv")
OUTPUT_FILE = os.path.join(BASE, "..", "..", "CEJC_anchor", "consolidated.csv")

# ── Kana conversion ───────────────────────────────────────────────────────────
def _hira_to_kata(text):
    return "".join(chr(ord(c) + 0x60) if 0x3041 <= ord(c) <= 0x3096 else c for c in text)

def _kata_to_hira(text):
    return "".join(chr(ord(c) - 0x60) if 0x30A1 <= ord(c) <= 0x30F6 else c for c in text)

def _is_pure_kana(word):
    return bool(word) and all(0x3040 <= ord(c) <= 0x30FF for c in word)

# ── Build reading lookup: word -> hiragana (JPDBV2 primary, CEJC TSV fallback) ─
# JPDBV2: term -> hiragana reading (most frequent reading per term)
_jpdb_reading = {}
with open(JPDB_FILE, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f, delimiter="\t"):
        term, reading, freq = row["term"], row["reading"], int(row["frequency"])
        if term not in _jpdb_reading or freq < _jpdb_reading[term][1]:
            _jpdb_reading[term] = (reading, freq)
_jpdb_reading = {t: r for t, (r, _) in _jpdb_reading.items()}

# CEJC TSV: 語彙素 -> katakana reading
_cejc_reading = {}
with open(CEJC_TSV, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f, delimiter="\t"):
        word, kata = row.get("語彙素", "").strip(), row.get("語彙素読み", "").strip()
        if word and kata and word not in _cejc_reading:
            _cejc_reading[word] = kata

def get_reading(word):
    """Return (hiragana, katakana) for word, or ('-', '-') if unknown."""
    if word in _jpdb_reading:
        hira = _jpdb_reading[word]
        return hira, _hira_to_kata(hira)
    if word in _cejc_reading:
        kata = _cejc_reading[word]
        return _kata_to_hira(kata), kata
    if _is_pure_kana(word):
        return _kata_to_hira(word), _hira_to_kata(word)
    return "-", "-"

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

# Load RSPEER (row position = rank; higher zipf_frequency = more frequent = earlier row)
rspeer_ranks = {}
with open(RSPEER_FILE, newline="", encoding="utf-8") as f:
    for rank, row in enumerate(csv.DictReader(f), start=1):
        word = row["word"]
        if word not in rspeer_ranks:
            rspeer_ranks[word] = rank
source_names.append("RSPEER")
sources["RSPEER"] = rspeer_ranks

def lookup(source, word):
    if word in source:
        return source[word]
    reading = kana_fallback.get(word)
    if reading and reading in source:
        return source[reading]
    return -1

# Write consolidated.csv
out_columns = ["word", "hiragana", "katakana"] + cejc_columns + source_names
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(out_columns)
    for row in cejc_rows:
        word = row["word"]
        hira, kata = get_reading(word)
        cejc_vals = [row[c] for c in cejc_columns]
        source_vals = [lookup(sources[s], word) for s in source_names]
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
