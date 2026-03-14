import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

DATA = "top_25000_japanese.csv"
OUTPUT = "plot_zipf_distribution.png"

ranks = []
zipf_scores = []

with open(DATA, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, start=1):
        ranks.append(i)
        zipf_scores.append(float(row["zipf_frequency"]))

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(ranks, zipf_scores, linewidth=0.8, color="#2563eb")

# Mark tier boundaries
tiers = [(1000, "top 1k"), (5000, "top 5k"), (10000, "top 10k")]
for rank, label in tiers:
    ax.axvline(x=rank, color="#dc2626", linestyle="--", linewidth=0.8, alpha=0.7)
    ax.text(rank + 100, zipf_scores[rank - 1] + 0.05, label, color="#dc2626", fontsize=8)

ax.set_xscale("log")
ax.set_xlabel("Rank (log scale)", fontsize=12)
ax.set_ylabel("Zipf Frequency", fontsize=12)
ax.set_title("Zipf Distribution — Top 25,000 Japanese Words (wordfreq)", fontsize=14)
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.grid(True, which="both", linestyle="--", linewidth=0.4, alpha=0.5)

plt.tight_layout()
plt.savefig(OUTPUT, dpi=150)
print(f"Saved {OUTPUT}")
