import csv
import os

csv.field_size_limit(10_000_000)

# Paths
BASE = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE, "consolidated.csv")
OUTPUT_FILE = os.path.join(BASE, "categorized.csv")

# Category thresholds (rank -> category number)
# 5 = basic   (rank 1–1000)
# 4 = common  (rank 1001–4000)
# 3 = fluent  (rank 4001–10000)
# 2 = advanced (rank 10001–25000)
# 1 = rare    (rank 25001+)
def categorize(rank_str):
    try:
        rank = int(rank_str)
    except (ValueError, TypeError):
        return 1
    if rank == -1:
        return 1
    if rank <= 1000:
        return 5
    elif rank <= 4000:
        return 4
    elif rank <= 10000:
        return 3
    elif rank <= 25000:
        return 2
    else:
        return 1

with open(INPUT_FILE, newline="", encoding="utf-8") as fin, \
     open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as fout:

    reader = csv.DictReader(fin)
    rank_columns = [c for c in reader.fieldnames if c != "word"]

    out_columns = ["word"] + rank_columns
    writer = csv.writer(fout)
    writer.writerow(out_columns)

    for row in reader:
        word = row["word"]
        cat_vals = [categorize(row[c]) for c in rank_columns]
        writer.writerow([word] + cat_vals)

print(f"Written categorized.csv with category values (5=basic, 4=common, 3=fluent, 2=advanced, 1=rare/not-in-source)")
