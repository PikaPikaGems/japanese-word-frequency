import csv
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, "..", "..")
EXCLUDE = {"AOZORA_BUNKO", "NIER", "ILYASEMENOV", "DD2_MIGAKU_NOVELS", "HERMITDAVE_2016", "HERMITDAVE_2018"}

# CEJC_anchor/consolidated.csv: words with at least one -1 rank (excluding excluded sources)
with open(os.path.join(DATA_DIR, "CEJC_anchor", "consolidated.csv")) as f:
    reader = csv.reader(f)
    header = next(reader)
    check_indices = [i for i, col in enumerate(header) if i > 0 and col not in EXCLUDE]
    rows = [row for row in reader if any(row[i] == "-1" for i in check_indices)]

with open(os.path.join(BASE, "has_negative_rank.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f"Words with at least one -1 rank (excl. excluded sources): {len(rows)}")

# CEJC_anchor/categorized.csv: words with at least one RARE (1) category (excluding excluded sources)
with open(os.path.join(DATA_DIR, "CEJC_anchor", "categorized.csv")) as f:
    reader = csv.reader(f)
    header = next(reader)
    check_indices = [i for i, col in enumerate(header) if i > 0 and col not in EXCLUDE]
    rows = [row for row in reader if any(row[i] == "1" for i in check_indices)]

with open(os.path.join(BASE, "has_rare_category.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f"Words with at least one RARE/absent category (excl. excluded sources): {len(rows)}")
