import csv
import matplotlib.pyplot as plt
import numpy as np

DATA = "top_25000_japanese.csv"
OUTPUT = "plot_script_breakdown.png"

HIRAGANA = set(range(0x3040, 0x30A0))
KATAKANA = set(range(0x30A0, 0x3100))
KANJI = set(range(0x4E00, 0xA000)) | set(range(0x3400, 0x4DC0)) | set(range(0xF900, 0xFB00))


def classify(word):
    scripts = set()
    for ch in word:
        cp = ord(ch)
        if cp in HIRAGANA:
            scripts.add("Hiragana")
        elif cp in KATAKANA:
            scripts.add("Katakana")
        elif cp in KANJI:
            scripts.add("Kanji")
    if len(scripts) == 0:
        return "Other"
    if len(scripts) == 1:
        return scripts.pop()
    return "Mixed"


TIERS = [
    ("Top 1k", 0, 1000),
    ("1k–5k", 1000, 5000),
    ("5k–10k", 5000, 10000),
    ("10k–25k", 10000, 25000),
]
SCRIPT_TYPES = ["Hiragana", "Katakana", "Kanji", "Mixed", "Other"]
COLORS = ["#60a5fa", "#f472b6", "#fb923c", "#a78bfa", "#94a3b8"]

overall_counts = {s: 0 for s in SCRIPT_TYPES}
tier_counts = {label: {s: 0 for s in SCRIPT_TYPES} for label, *_ in TIERS}

with open(DATA, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        script = classify(row["word"])
        overall_counts[script] += 1
        for label, lo, hi in TIERS:
            if lo <= i < hi:
                tier_counts[label][script] += 1
                break

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Pie chart — overall
labels = [s for s in SCRIPT_TYPES if overall_counts[s] > 0]
sizes = [overall_counts[s] for s in labels]
ax1.pie(sizes, labels=labels, colors=[COLORS[SCRIPT_TYPES.index(l)] for l in labels],
        autopct="%1.1f%%", startangle=140, textprops={"fontsize": 10})
ax1.set_title("Script Type Distribution (All 25,000 words)", fontsize=12)

# Stacked bar chart — by tier
tier_labels = [label for label, *_ in TIERS]
bottoms = np.zeros(len(TIERS))
for script, color in zip(SCRIPT_TYPES, COLORS):
    values = [tier_counts[label][script] for label in tier_labels]
    totals = [sum(tier_counts[label].values()) for label in tier_labels]
    pcts = [v / t * 100 if t > 0 else 0 for v, t in zip(values, totals)]
    ax2.bar(tier_labels, pcts, bottom=bottoms, label=script, color=color)
    bottoms += np.array(pcts)

ax2.set_xlabel("Frequency Tier", fontsize=11)
ax2.set_ylabel("Share (%)", fontsize=11)
ax2.set_title("Script Type Share by Frequency Tier", fontsize=12)
ax2.legend(loc="upper right", fontsize=9)
ax2.set_ylim(0, 105)
ax2.grid(True, axis="y", linestyle="--", linewidth=0.4, alpha=0.5)

fig.suptitle("Script Type Breakdown — wordfreq Japanese", fontsize=14)
plt.tight_layout()
plt.savefig(OUTPUT, dpi=150)
print(f"Saved {OUTPUT}")
