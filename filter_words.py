import csv

DATA_DIR = "data/ALL"
EXCLUDE = {"AOZORA_BUNKO", "NIER", "ILYASEMENOV", "DD2_MIGAKU_NOVELS", "HERMITDAVE_2016", "HERMITDAVE_2018"}

# consolidated_anchor_CEJC.csv: words with at least one -1 rank (excluding AOZORA_BUNKO)
with open(f"{DATA_DIR}/consolidated_anchor_CEJC.csv") as f:
    reader = csv.reader(f)
    header = next(reader)
    check_indices = [i for i, col in enumerate(header) if i > 0 and col not in EXCLUDE]
    rows = [row for row in reader if any(row[i] == "-1" for i in check_indices)]

with open(f"{DATA_DIR}/has_negative_rank.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f"Words with at least one -1 rank (excl. AOZORA_BUNKO): {len(rows)}")

# categorized.csv: words with at least one RARE (1) category (excluding AOZORA_BUNKO)
with open(f"{DATA_DIR}/categorized_anchor_CEJC.csv") as f:
    reader = csv.reader(f)
    header = next(reader)
    check_indices = [i for i, col in enumerate(header) if i > 0 and col not in EXCLUDE]
    rows = [row for row in reader if any(row[i] == "1" for i in check_indices)]

with open(f"{DATA_DIR}/has_rare_category.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)

print(f"Words with at least one RARE/absent category (excl. AOZORA_BUNKO): {len(rows)}")
