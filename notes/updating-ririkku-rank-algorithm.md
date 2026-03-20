# Updating the RIRIKKU_RANK Algorithm

This guide describes what to change when you want to modify which sources are included in the `RIRIKKU_RANK` computation.

See [SINGLE_RANK.md](SINGLE_RANK.md) for the algorithm rationale and [dataset-catalog.md](dataset-catalog.md) for descriptions of all available sources.

---

## Step 1 — Edit `make_ririkku.py`

Open [data/ALL/___data_generation/make_ririkku.py](../data/ALL/___data_generation/make_ririkku.py).

### To add a new source to RIRIKKU_RANK computation

1. Confirm the source has a `DATA.csv` under `data/RAW/___FILTERED/<SOURCE_NAME>/DATA.csv`.
2. Add its column ID to the `SHORTLISTED` list.
3. Update the docstring to list the new column.

### To remove a source from RIRIKKU_RANK computation (but keep it as an output column)

1. Remove it from `SHORTLISTED`.
2. Add it to `EXTRA_COLS`. It will still appear in `RIRIKKU_CONSOLIDATED.csv` for reference, but will not affect rank computation.

### To remove a source entirely (from both rank and output)

Simply remove it from both `SHORTLISTED` and `EXTRA_COLS`. It will no longer appear in `RIRIKKU_CONSOLIDATED.csv`.

---

## Step 2 — Re-run the script

From the repo root:

```bash
python data/ALL/___data_generation/make_ririkku.py
```

This regenerates `data/ALL/RIRIKKU_CONSOLIDATED.csv`.

---

## Step 3 — Regenerate the category tables

```bash
python data/ALL/___experiments3/category_tables.py
```

Copy the output tables into [SINGLE_RANK.md](SINGLE_RANK.md) under the **Category Breakdown and Threshold Selection** section:
- Replace the **Category Rank Ranges** tables (Type A and Type B).
- Replace the **Threshold Comparison** tables (≥2 / ≥3 / ≥4 rows).

---

## Step 4 — Update `SINGLE_RANK.md`

- **Included Sources table**: add or remove the source row.
- **Excluded Sources table**: if removing a source from ranking but keeping it as a column, add a row explaining why.
- **Threshold rationale paragraph**: if the count of media/subtitle sources changes, update the sentence that explains why ≥3 was chosen.
- **Numbers**: paste in the new tables from Step 3.

---

## Step 5 — Update `dataset-catalog.md`

- **Highlighted (Shortlisted) section**: add the new source if it is now shortlisted, or remove it if it is no longer used for ranking.
- **JITEN Breakdown / relevant section**: update the source's description row to reflect its new status (e.g., add or remove the ✅ shortlisted note).

---

## Step 6 — Verify

Check the output looks sane:

```bash
head -5 data/ALL/RIRIKKU_CONSOLIDATED.csv
```

Confirm the new source appears as a column header, and that `RIRIKKU_RANK` values look reasonable (top words should have rank 1–100).
