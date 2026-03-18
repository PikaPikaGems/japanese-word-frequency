## Setup

### Requirements

- Python 3.10+
- For plotting scripts: `matplotlib`, `numpy`
- For RSPEER generation: `wordfreq`

### Install dependencies

```bash
# To get RSPeer dataset
pip install wordfreq
# For generating graphs and insights
pip install matplotlib numpy
```

### Running scripts

Scripts under `data/ALL/___experiments0/` and `data/ALL/___experiments1/` can be run from the repo root. CEJC, RSPEER, and JPDB scripts must be run from their own directories.

The full pipeline has the following dependency order: RAW/\_\_\_FILTERED → CEJC + RSPEER preprocessing → data/ALL consolidation → analysis.

#### Step 1 — Generate standardized DATA.csv for each RAW source

Each source under `data/RAW/___FILTERED/` has a `SCRIPT.py` that reads the raw upstream file and outputs a normalized `DATA.csv` (columns: `WORD`, `FREQUENCY_RANKING`, top 25k entries). Run each from the repo root:

```bash
python data/RAW/___FILTERED/ADNO/SCRIPT.py
python data/RAW/___FILTERED/ANIME_JDRAMA/SCRIPT.py
python data/RAW/___FILTERED/AOZORA_BUNKO/SCRIPT.py
# ... repeat for all subdirectories under data/RAW/___FILTERED/
```

#### Step 2 — Preprocess CEJC, RSPEER, and JPDBV2

These outputs are consumed by the data/ALL consolidation scripts.

```bash
# CEJC: generate JSON and CSV breakdowns from the source TSV, then deduplicate
cd data/CEJC
python3 scripts/tsv_to_json.py 2_cejc_frequencylist_suw_token.tsv json 25000
python3 scripts/tsv_to_csv.py 2_cejc_frequencylist_suw_token.tsv csv 25000
python3 scripts/make_consolidated_unique.py   # reads CONSOLIDATED.csv → writes CONSOLIDATED_UNIQUE.csv

# RSPEER: generate top_25000_japanese.csv via the wordfreq library
cd data/RSPEER
python generate_top_japanese.py

# JPDBV2: generate task1_top25k.csv and task2_kana_higher.csv
cd data/JPDBV2
python process.py
```

#### Step 3 — Generate consolidated.csv and categorized.csv

Run from the repo root. Reads CEJC `CONSOLIDATED_UNIQUE.csv`, all `DATA.csv` files from `RAW/___FILTERED`, and RSPEER `top_25000_japanese.csv`.

```bash
# Check for duplicate rank columns across all consolidated.csv files
# (exits with code 1 if any two columns have identical values — catches accidentally duplicated sources)
python data/ALL/___data_generation/check_duplicate_rank_columns.py

# Check that every word in every consolidated.csv has hiragana and katakana readings
# (exits with code 1 if any readings are missing)
python data/ALL/___data_generation/check_missing_reading.py

# Generate CEJC_anchor/consolidated.csv (CEJC as the anchor word list)
python data/ALL/___data_generation/SCRIPT.py

# Generate CEJC_anchor/categorized.csv (vocab tier categories from consolidated.csv)
python data/ALL/___data_generation/CATEGORIZED.py

# Generate consolidated.csv + categorized.csv for all non-CEJC anchors
python data/ALL/___data_generation/make_more_anchors.py
```

#### Step 4 — Analysis Reports (optional)

Coverage and threshold analysis

> These steps reproduce the analysis in `___experiments0/` and `___experiments1/`. They are not required when adding new frequency sources — only re-run if you want updated coverage statistics or reports.

```bash
# experiments0: coverage and threshold analysis
python data/ALL/___experiments0/coverage_analysis/analyze_coverage.py
python data/ALL/___experiments0/coverage_analysis/filter_words.py
python data/ALL/___experiments0/threshold_analysis/threshold_analysis.py

# experiments1: coverage, threshold, top-12k analysis
python data/ALL/___experiments1/coverage_analysis/analyze_coverage.py
python data/ALL/___experiments1/coverage_analysis/threshold_analysis.py
python data/ALL/___experiments1/top12k/generate_12k.py
python data/ALL/___experiments1/top12k/analyze_coverage.py
python data/ALL/___experiments1/top12k/threshold_analysis.py
python data/ALL/___experiments1/top12k/n_leq3_by_rank_band.py
python data/ALL/___experiments1/anchor_pairwise_overlap.py
```

CEJC analysis reports

```bash
cd data/CEJC/scripts
python vocab_tier_breakdown.py ../json
python domain_profiles.py ../json
python demographic_analysis.py ../json
# ... (see data/CEJC/scripts/ for all scripts — all take ../json as the first argument)
```

RSPEER plots

```bash
cd data/RSPEER
python plot_coverage_curve.py
python plot_zipf_distribution.py
# ... (see data/RSPEER/ for all 6 plotting scripts)
```
