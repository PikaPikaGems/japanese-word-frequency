import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

DATA = "top_25000_japanese.csv"
OUTPUT = "plot_coverage_curve.png"

frequencies = []

with open(DATA, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        frequencies.append(float(row["frequency"]))

total = sum(frequencies)
cumulative = []
running = 0.0
for f in frequencies:
    running += f
    cumulative.append(running / total * 100)

ranks = list(range(1, len(cumulative) + 1))

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(ranks, cumulative, linewidth=1.2, color="#2563eb")

thresholds = [80, 90, 95, 98]
colors = ["#f59e0b", "#10b981", "#8b5cf6", "#dc2626"]
for pct, color in zip(thresholds, colors):
    # find first rank that hits this threshold
    for i, c in enumerate(cumulative):
        if c >= pct:
            ax.axhline(y=pct, color=color, linestyle="--", linewidth=0.8, alpha=0.8)
            ax.axvline(x=i + 1, color=color, linestyle="--", linewidth=0.8, alpha=0.8)
            ax.annotate(
                f"{pct}% @ {i + 1:,} words",
                xy=(i + 1, pct),
                xytext=(i + 1 + 500, pct - 2),
                fontsize=8,
                color=color,
                arrowprops=dict(arrowstyle="-", color=color, lw=0.6),
            )
            break

ax.set_xlabel("Number of Words Known", fontsize=12)
ax.set_ylabel("Cumulative Text Coverage (%)", fontsize=12)
ax.set_title("Frequency Coverage Curve — Top 25,000 Japanese Words (wordfreq)", fontsize=14)
ax.set_ylim(0, 101)
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.grid(True, linestyle="--", linewidth=0.4, alpha=0.5)

plt.tight_layout()
plt.savefig(OUTPUT, dpi=150)
print(f"Saved {OUTPUT}")
