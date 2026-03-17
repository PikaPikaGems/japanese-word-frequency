import csv
import os

csv.field_size_limit(10_000_000)

# Paths
BASE = os.path.dirname(os.path.abspath(__file__))
INPUT_FILE = os.path.join(BASE, "..", "CEJC_anchor", "consolidated.csv")
OUTPUT_FILE = os.path.join(BASE, "..", "CEJC_anchor", "categorized.csv")


# Category thresholds (rank -> category number)
# 5 = basic
# 4 = common
# 3 = fluent
# 2 = advanced
# 1 = rare
def categorize(rank_str):
    try:
        rank = int(rank_str)
    except (ValueError, TypeError):
        return 1
    if rank == -1:
        return 1
    if rank <= 1800:
        return 5
    elif rank <= 5000:
        return 4
    elif rank <= 12000:
        return 3
    elif rank <= 25000:
        return 2
    else:
        return 1


PASSTHROUGH = {"hiragana", "katakana"}

with open(INPUT_FILE, newline="", encoding="utf-8") as fin, open(
    OUTPUT_FILE, "w", newline="", encoding="utf-8"
) as fout:

    reader = csv.DictReader(fin)
    other_columns = [c for c in reader.fieldnames if c not in {"word"} | PASSTHROUGH]

    out_columns = ["word"] + [c for c in reader.fieldnames if c != "word"]
    writer = csv.writer(fout)
    writer.writerow(out_columns)

    for row in reader:
        word = row["word"]
        passthrough_vals = {c: row[c] for c in PASSTHROUGH if c in row}
        out_row = [word]
        for c in reader.fieldnames:
            if c == "word":
                continue
            elif c in PASSTHROUGH:
                out_row.append(row[c])
            else:
                out_row.append(categorize(row[c]))
        writer.writerow(out_row)

print(
    f"Written categorized.csv with category values (5=basic, 4=common, 3=fluent, 2=advanced, 1=rare/not-in-source)"
)
