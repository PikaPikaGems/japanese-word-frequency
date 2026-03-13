# Task 1

- Your INPUTS
  --> ./data/CEJC/csv/consolidated.csv
  ---> You also have many DATA.csv files in RAW/\_\_\_FILTERED/\*
- Create a new folder CSV ./data/ALL/ with three files
  -- SCRIPT.py
  -- consolidated.csv
  -- README.md
- The task is create a file where all these inputs will be merged... all the rankings in one CSV file
- Given the input Create a SCRIPT.py that will output ./data/ALL/consolidated.csv
  where the rows are the words as sorted in consolidated.csv
- WORD, RANK_A, RANK_B, RANK_C, ... and so on and so forth given consolidated.csv, and all the DATA.csv in RAW/\_\_\_FILTERED
- Update the ./data/all/README.md accordingly

# Task 2

-- Now that you have ./data/all/consolidated.csv, you will use the data here to create a file ./data/all/categorized.csv . create a script called ./data/ALL/CATEGORIZE.py
-- So basically you will map WORD, RANK_A, RANK_B, RANK_C, ... (etc)
to WORD, CATEGORY_A, CATEGORY_B, CATEGORY_C, ... (etc)
-- These are the categories ('basic, 'common', 'fluent', 'advanced', 'rare'). use
NUMBERS instead 5 is basic, 1 is rare
a. 5 🌱 basic: Top ~1,000 – Foundational and essential vocabulary.
b 4 ☘️ common: Top ~1,001–4,000 — Frequent in everyday speech and writing.
c. 3 🌷 fluent: Top ~4,001–10,000 – Expansive vocabulary for natural expression across contexts.
d. 2 📚 advanced: Top ~10,001–25,000 — Formal, academic, technical or specialized terms.
e. 1 🦉 rare: Top 25,000+ — Archaic, obscure, uncommon, or invalid terms.
--- Update the readme accordingly
