import csv
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

RSPEER_DATA = "top_25000_japanese.csv"
JPDB_DATA = "../JPDBV2/task1_top25k.csv"
CEJC_DATA = "../CEJC/CONSOLIDATED_UNIQUE.csv"
OUTPUT = "plot_cross_dataset_comparison.png"

# Load wordfreq (RSPEER) ranks
rspeer_ranks = {}
with open(RSPEER_DATA, encoding="utf-8") as f:
    for i, row in enumerate(csv.DictReader(f), start=1):
        rspeer_ranks[row["word"]] = i

# Load JPDB ranks
jpdb_ranks = {}
with open(JPDB_DATA, encoding="utf-8") as f:
    for row in csv.DictReader(f):
        jpdb_ranks[row["term"]] = int(row["reading_frequency"])

# Load CEJC ranks
cejc_ranks = {}
with open(CEJC_DATA, encoding="utf-8") as f:
    for row in csv.DictReader(f):
        cejc_ranks[row["word"]] = int(row["cejc_combined_rank"])

# Find overlaps
common_rspeer_jpdb = set(rspeer_ranks) & set(jpdb_ranks)
common_rspeer_cejc = set(rspeer_ranks) & set(cejc_ranks)

print(f"wordfreq total: {len(rspeer_ranks):,}")
print(f"JPDB total: {len(jpdb_ranks):,}")
print(f"CEJC total: {len(cejc_ranks):,}")
print(f"wordfreq ∩ JPDB: {len(common_rspeer_jpdb):,}")
print(f"wordfreq ∩ CEJC: {len(common_rspeer_cejc):,}")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Scatter: wordfreq rank vs JPDB rank (sample if large)
words_wf_jpdb = sorted(common_rspeer_jpdb, key=lambda w: rspeer_ranks[w])
sample_wf = words_wf_jpdb[::max(1, len(words_wf_jpdb) // 3000)]
x_wf = [rspeer_ranks[w] for w in sample_wf]
y_jpdb = [jpdb_ranks[w] for w in sample_wf]

# Color points by rank divergence
divergence_jpdb = [abs(rspeer_ranks[w] - jpdb_ranks[w]) for w in sample_wf]
sc1 = axes[0].scatter(x_wf, y_jpdb, c=divergence_jpdb, cmap="RdYlGn_r",
                      s=2, alpha=0.5, norm=mcolors.LogNorm(vmin=1, vmax=max(divergence_jpdb)))
axes[0].plot([1, 25000], [1, 25000], color="black", linewidth=0.8, linestyle="--", alpha=0.5, label="Perfect agreement")
axes[0].set_xlabel("wordfreq rank", fontsize=11)
axes[0].set_ylabel("JPDB rank", fontsize=11)
axes[0].set_title("wordfreq vs JPDB", fontsize=12)
axes[0].set_xscale("log")
axes[0].set_yscale("log")
plt.colorbar(sc1, ax=axes[0], label="Rank divergence")
axes[0].legend(fontsize=8)
axes[0].grid(True, which="both", linestyle="--", linewidth=0.3, alpha=0.4)

# Scatter: wordfreq rank vs CEJC rank
words_wf_cejc = sorted(common_rspeer_cejc, key=lambda w: rspeer_ranks[w])
sample_cejc = words_wf_cejc[::max(1, len(words_wf_cejc) // 3000)]
x_wf2 = [rspeer_ranks[w] for w in sample_cejc]
y_cejc = [cejc_ranks[w] for w in sample_cejc]

divergence_cejc = [abs(rspeer_ranks[w] - cejc_ranks[w]) for w in sample_cejc]
sc2 = axes[1].scatter(x_wf2, y_cejc, c=divergence_cejc, cmap="RdYlGn_r",
                      s=2, alpha=0.5, norm=mcolors.LogNorm(vmin=1, vmax=max(divergence_cejc)))
axes[1].plot([1, 25000], [1, 25000], color="black", linewidth=0.8, linestyle="--", alpha=0.5, label="Perfect agreement")
axes[1].set_xlabel("wordfreq rank", fontsize=11)
axes[1].set_ylabel("CEJC rank", fontsize=11)
axes[1].set_title("wordfreq vs CEJC", fontsize=12)
axes[1].set_xscale("log")
axes[1].set_yscale("log")
plt.colorbar(sc2, ax=axes[1], label="Rank divergence")
axes[1].legend(fontsize=8)
axes[1].grid(True, which="both", linestyle="--", linewidth=0.3, alpha=0.4)

# Highlight top outliers (words with huge rank divergence in wordfreq vs JPDB)
outliers_jpdb = sorted(common_rspeer_jpdb, key=lambda w: abs(rspeer_ranks[w] - jpdb_ranks[w]), reverse=True)[:10]
print("\nTop 10 rank-divergent words (wordfreq vs JPDB):")
print(f"{'Word':<12} {'wordfreq':>10} {'JPDB':>10} {'|diff|':>10}")
for w in outliers_jpdb:
    print(f"{w:<12} {rspeer_ranks[w]:>10,} {jpdb_ranks[w]:>10,} {abs(rspeer_ranks[w]-jpdb_ranks[w]):>10,}")

fig.suptitle("Cross-Dataset Rank Comparison (wordfreq vs JPDB / CEJC)", fontsize=14)
plt.tight_layout()
plt.savefig(OUTPUT, dpi=150)
print(f"\nSaved {OUTPUT}")
