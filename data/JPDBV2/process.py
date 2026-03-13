import csv

src = '/Users/mithi/Desktop/PikaPikaGems/word-frequency-rankings/data/JPDBV2/jpdb_v2.2_freq_list_2024-10-13.csv'
out1 = '/Users/mithi/Desktop/PikaPikaGems/word-frequency-rankings/data/JPDBV2/task1_top25k.csv'
out2 = '/Users/mithi/Desktop/PikaPikaGems/word-frequency-rankings/data/JPDBV2/task2_kana_higher.csv'

task1_rows = []
task2_rows = []

with open(src, encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        freq = row['frequency']
        kana_freq = row.get('kana_frequency', '').strip()
        if not freq:
            continue
        freq_int = int(freq)
        if freq_int > 25000:
            break
        task1_rows.append((row['term'], freq))
        if kana_freq:
            kana_int = int(kana_freq)
            if kana_int < freq_int:
                task2_rows.append((row['term'], freq, kana_freq))

with open(out1, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['term', 'reading_frequency'])
    writer.writerows(task1_rows)

with open(out2, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['term', 'reading_frequency', 'kana_frequency'])
    writer.writerows(task2_rows)

print(f'Task 1: {len(task1_rows)} rows')
print(f'Task 2: {len(task2_rows)} rows')
