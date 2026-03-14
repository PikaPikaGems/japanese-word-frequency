import csv
import matplotlib.pyplot as plt
import numpy as np

DATA = "top_25000_japanese.csv"
OUTPUT = "plot_word_length_by_tier.png"

TIERS = [
    ("Top 1k", 0, 1000, "#2563eb"),
    ("1k–5k", 1000, 5000, "#10b981"),
    ("5k–10k", 5000, 10000, "#f59e0b"),
    ("10k–25k", 10000, 25000, "#dc2626"),
]

tier_lengths = {label: [] for label, *_ in TIERS}

with open(DATA, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        word = row["word"]
        length = len(word)
        for label, lo, hi, _ in TIERS:
            if lo <= i < hi:
                tier_lengths[label].append(length)
                break

max_len = max(l for lengths in tier_lengths.values() for l in lengths)
bins = np.arange(1, max_len + 2) - 0.5

fig, axes = plt.subplots(2, 2, figsize=(12, 8), sharex=True, sharey=False)
axes = axes.flatten()

for ax, (label, lo, hi, color) in zip(axes, TIERS):
    lengths = tier_lengths[label]
    ax.hist(lengths, bins=bins, color=color, edgecolor="white", linewidth=0.4)
    mean_len = np.mean(lengths)
    ax.axvline(mean_len, color="black", linestyle="--", linewidth=1)
    ax.text(mean_len + 0.1, ax.get_ylim()[1] * 0.9, f"mean={mean_len:.2f}", fontsize=8)
    ax.set_title(f"{label} ({hi - lo:,} words)", fontsize=11)
    ax.set_xlabel("Word Length (characters)", fontsize=9)
    ax.set_ylabel("Count", fontsize=9)
    ax.set_xticks(range(1, max_len + 1))
    ax.grid(True, axis="y", linestyle="--", linewidth=0.4, alpha=0.5)

fig.suptitle("Word Length Distribution by Frequency Tier — wordfreq Japanese", fontsize=14, y=1.01)
plt.tight_layout()
plt.savefig(OUTPUT, dpi=150, bbox_inches="tight")
print(f"Saved {OUTPUT}")
