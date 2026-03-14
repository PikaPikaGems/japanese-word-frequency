import csv
import matplotlib.pyplot as plt
import numpy as np

DATA = "top_25000_japanese.csv"
OUTPUT = "plot_zipf_histogram.png"

zipf_scores = []

with open(DATA, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        zipf_scores.append(float(row["zipf_frequency"]))

fig, ax = plt.subplots(figsize=(10, 6))

bins = np.arange(0, 8.25, 0.25)
ax.hist(zipf_scores, bins=bins, color="#2563eb", edgecolor="white", linewidth=0.3)

# Mark common cut-off thresholds
for threshold, label in [(3.0, "≥3.0\n(study target)"), (4.0, "≥4.0\n(common)"), (5.0, "≥5.0\n(very common)")]:
    ax.axvline(x=threshold, color="#dc2626", linestyle="--", linewidth=1, alpha=0.8)
    ax.text(threshold + 0.05, ax.get_ylim()[1] * 0.85, label, color="#dc2626", fontsize=8)

ax.set_xlabel("Zipf Frequency Score", fontsize=12)
ax.set_ylabel("Number of Words", fontsize=12)
ax.set_title("Zipf Score Distribution — Top 25,000 Japanese Words (wordfreq)", fontsize=14)
ax.set_xlim(0, 8.5)
ax.xaxis.set_major_locator(plt.MultipleLocator(1))
ax.xaxis.set_minor_locator(plt.MultipleLocator(0.5))
ax.grid(True, axis="y", linestyle="--", linewidth=0.4, alpha=0.5)

# Annotate percentile breakdown
for cutoff in [3.0, 4.0, 5.0]:
    count_above = sum(1 for z in zipf_scores if z >= cutoff)
    pct = count_above / len(zipf_scores) * 100
    print(f"Words with zipf >= {cutoff}: {count_above:,} ({pct:.1f}%)")

plt.tight_layout()
plt.savefig(OUTPUT, dpi=150)
print(f"Saved {OUTPUT}")
