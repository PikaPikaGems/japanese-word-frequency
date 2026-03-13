# TODO:

## First Task

Rerun the following to get top 25,000 words instead

1. Run: `python3 scripts/tsv_to_json.py <input.tsv> <output_dir> [top_n]`
2. Run: `python3 scripts/tsv_to_csv.py <input.tsv> <output_dir> [top_n]`
3. Run: all the other scripts in ./data/CEJC/scripts folder to generate the data insights
4. Update the markdown files in ./data/CEJC/insights/ accordingly

## Second Task

Create a CSV file with the top 25,000 words (use combined.csv to get the frequency ranking). Name it CONSOLIDATED.csv
Update this README accordingly.

**These are tha columns (use better names)**

- Word
- combined frequency ranke
- `combined.csv`
- `domain.small_talk.csv`
- `domain.consultation.csv`
- `domain.meeting.csv`
- `domain.class.csv`
- `domain.outdoors.csv`
- `domain.school.csv`
- `domain.transportation.csv`
- `domain.public_commercial.csv`
- `domain.home.csv`
- `domain.indoors.csv`
- `domain.workplace.csv`
- `demographics.m.csv`
- `demographics.f.csv`

# Source

- https://github.com/forsakeninfinity/CEJC_yomichan_freq_dict
- https://github.com/forsakeninfinity/CEJC_yomichan_freq_dict/blob/main/2_cejc_frequencylist_suw_token.tsv

# Example (raw) data

```
rank	語彙素読み	語彙素	品詞	語彙素細分類	語種	frequency	pmw	雑談_rank	雑談_frequency	雑談_pmw	用談・相談_rank	用談・相談_frequency	用談・相談_pmw	会議・会合_rank	会議・会合_frequency	会議・会合_pmw	授業・レッスン_rank	授業・レッスン_frequency	授業・レッスン_pmw	屋外_rank	屋外_frequency	屋外_pmw	学校_rank	学校_frequency	学校_pmw	交通機関_rank	交通機関_frequency	交通機関_pmw	公共商業施設_rank	公共商業施設_frequency	公共商業施設_pmw	自宅_rank	自宅_frequency	自宅_pmw	室内_rank	室内_frequency	室内_pmw	職場_rank	職場_frequency	職場_pmw	男性_rank	男性_frequency	男性_pmw	女性_rank	女性_frequency	女性_pmw	0-4歳_rank	0-4歳_frequency	0-4歳_pmw	5-9歳_rank	5-9歳_frequency	5-9歳_pmw	10-14歳_rank	10-14歳_frequency	10-14歳_pmw	15-19歳_rank	15-19歳_frequency	15-19歳_pmw	20-24歳_rank	20-24歳_frequency	20-24歳_pmw	25-29歳_rank
```

## How to use

1. Download this file: https://github.com/forsakeninfinity/CEJC_yomichan_freq_dict/blob/main/2_cejc_frequencylist_suw_token.tsv
2. Run: `python3 scripts/tsv_to_json.py <input.tsv> <output_dir> [top_n]`
3. Run: `python3 scripts/tsv_to_csv.py <input.tsv> <output_dir> [top_n]`

`top_n` is optional and defaults to 12,000.

# Generated JSON Files

## Introduction

Three files are output by `scripts/tsv_to_json.py`, all covering the top `top_n` words (default: 12,000) by overall frequency rank. Each word key maps to an **array of entries** — one per POS — because the same surface form can appear multiple times with different grammatical categories (e.g. の as 助詞-格助詞, 助詞-準体助詞, 助詞-終助詞). All leaf values are `[rank, freq, pmw]` arrays.

The three files share the same word keys and array indices: entry `word[i]` in `cejc.json` corresponds to entry `word[i]` in `cejc.cross.json` and `cejc.gender_age.json`.

## `cejc.json`

Core data: combined stats, domain breakdown, and full demographic breakdown.

```json
{
  "読む": [
    {
      "reading": "ヨム",
      "pos": "動詞",
      "subcategory": "一般",
      "origin": "和",
      "combined": [150, 1234, 567.8],
      "domains": {
        "small_talk":        [140, 300, 450.1],
        "consultation":      [200, 100, 210.5],
        "meeting":           [180,  80, 190.3],
        "class":             [ 90, 250, 600.0],
        "outdoors":          [300,  50, 120.0],
        "school":            [ 85, 270, 620.0],
        "transportation":    [400,  20,  80.0],
        "public_commercial": [350,  30,  95.0],
        "home":              [160, 200, 400.0],
        "indoors":           [155, 210, 410.0],
        "workplace":         [170, 180, 380.0]
      },
      "demographics": {
        "m":       [145, 600, 540.0],
        "f":       [155, 634, 590.0],
        "0_4":     [500,  10,  30.0],
        "5_9":     [300,  40,  90.0],
        "10_14":   [200,  80, 150.0],
        "15_19":   [120, 150, 400.0],
        "20_24":   [130, 140, 380.0],
        "25_29":   [135, 135, 370.0],
        "30_34":   [...],
        "35_39":   [...],
        "40_44":   [...],
        "45_49":   [...],
        "50_54":   [...],
        "55_59":   [...],
        "60_64":   [...],
        "65_69":   [...],
        "70_74":   [...],
        "75_79":   [...],
        "80_84":   [...],
        "85_89":   [...],
        "90_94":   [...],
        "unknown": [...]
      }
    }
  ]
}
```

## `cejc.cross.json`

Conversation-type × location cross-tabulations.

```json
{
  "読む": [
    {
      "small_talk": {
        "outdoors":          [r, f, p],
        "school":            [r, f, p],
        "transportation":    [r, f, p],
        "public_commercial": [r, f, p],
        "home":              [r, f, p],
        "indoors":           [r, f, p],
        "workplace":         [r, f, p]
      },
      "consultation": {
        "outdoors":          [r, f, p],
        "school":            [r, f, p],
        "transportation":    [r, f, p],
        "public_commercial": [r, f, p],
        "home":              [r, f, p],
        "indoors":           [r, f, p],
        "workplace":         [r, f, p]
      },
      "meeting": {
        "outdoors":          [r, f, p],
        "school":            [r, f, p],
        "transportation":    [r, f, p],
        "public_commercial": [r, f, p],
        "home":              [r, f, p],
        "indoors":           [r, f, p],
        "workplace":         [r, f, p]
      },
      "class": {
        "outdoors":          [r, f, p],
        "school":            [r, f, p],
        "transportation":    [r, f, p],
        "public_commercial": [r, f, p],
        "home":              [r, f, p],
        "indoors":           [r, f, p],
        "workplace":         [r, f, p]
      }
    }
  ]
}
```

## `cejc.gender_age.json`

Gender × age group cross-tabulations. Age keys match `demographics` in `cejc.json` (0_4 through 90_94 plus unknown).

```json
{
  "読む": [
    {
      "m": {
        "0_4":     [r, f, p],
        "5_9":     [r, f, p],
        "10_14":   [r, f, p],
        "15_19":   [r, f, p],
        "20_24":   [r, f, p],
        "25_29":   [r, f, p],
        "30_34":   [r, f, p],
        "35_39":   [r, f, p],
        "40_44":   [r, f, p],
        "45_49":   [r, f, p],
        "50_54":   [r, f, p],
        "55_59":   [r, f, p],
        "60_64":   [r, f, p],
        "65_69":   [r, f, p],
        "70_74":   [r, f, p],
        "75_79":   [r, f, p],
        "80_84":   [r, f, p],
        "85_89":   [r, f, p],
        "90_94":   [r, f, p],
        "unknown": [r, f, p]
      },
      "f": {
        "0_4":     [r, f, p],
        "5_9":     [r, f, p],
        "10_14":   [r, f, p],
        "15_19":   [r, f, p],
        "20_24":   [r, f, p],
        "25_29":   [r, f, p],
        "30_34":   [r, f, p],
        "35_39":   [r, f, p],
        "40_44":   [r, f, p],
        "45_49":   [r, f, p],
        "50_54":   [r, f, p],
        "55_59":   [r, f, p],
        "60_64":   [r, f, p],
        "65_69":   [r, f, p],
        "70_74":   [r, f, p],
        "75_79":   [r, f, p],
        "80_84":   [r, f, p],
        "85_89":   [r, f, p],
        "90_94":   [r, f, p],
        "unknown": [r, f, p]
      }
    }
  ]
}
```

## Generated CSV Data

Generated by `scripts/tsv_to_csv.py`. Each file covers the top `top_n` words (default: 12,000) by overall frequency rank, with columns `word, rank, freq, pmw`, sorted ascending by the rank column of that breakdown.

### CSV files

- `combined.csv`
- `domain.small_talk.csv`
- `domain.consultation.csv`
- `domain.meeting.csv`
- `domain.class.csv`
- `domain.outdoors.csv`
- `domain.school.csv`
- `domain.transportation.csv`
- `domain.public_commercial.csv`
- `domain.home.csv`
- `domain.indoors.csv`
- `domain.workplace.csv`
- `demographics.m.csv`
- `demographics.f.csv`
- `demographics.0_4.csv`
- `demographics.5_9.csv`
- `demographics.10_14.csv`
- `demographics.15_19.csv`
- `demographics.20_24.csv`
- `demographics.25_29.csv`
- `demographics.30_34.csv`
- `demographics.35_39.csv`
- `demographics.40_44.csv`
- `demographics.45_49.csv`
- `demographics.50_54.csv`
- `demographics.55_59.csv`
- `demographics.60_64.csv`
- `demographics.65_69.csv`
- `demographics.70_74.csv`
- `demographics.75_79.csv`
- `demographics.80_84.csv`
- `demographics.85_89.csv`
- `demographics.90_94.csv`
- `demographics.unknown.csv`

**Conversation-type × location cross-tabulations** (28 files — one per pair):

- `cross.{conv}.{location}.csv` where conv ∈ `{small_talk, consultation, meeting, class}` and location ∈ `{outdoors, school, transportation, public_commercial, home, indoors, workplace}`

**Gender × age cross-tabulations** (40 files — one per pair):

- `gender_age.{gender}.{age}.csv` where gender ∈ `{m, f}` and age ∈ `{0_4, 5_9, 10_14, 15_19, 20_24, 25_29, 30_34, 35_39, 40_44, 45_49, 50_54, 55_59, 60_64, 65_69, 70_74, 75_79, 80_84, 85_89, 90_94, unknown}`

# Data Insights

**1. `vocab_tier_breakdown.py`** — The one you originally described. For each tier (top 1500, 4000, 10000, 20000), generate:

- POS distribution (% 動詞, 名詞, 形容詞, etc.)
- Word origin distribution (和, 漢, 外, 混)
- Subcategory distribution
- Cross-tabulations (e.g. origin × POS per tier)
- Output: Markdown tables + ASCII bar charts + Mermaid pie charts

**2. `domain_profiles.py`** — For each domain (school, workplace, home, etc.):

- Top N words unique to that domain (high domain rank, low overall rank)
- Domain-defining words (biggest rank gap vs. overall)
- Domain vocabulary overlap matrix
- Output: Markdown tables + Mermaid heatmap-style diagrams

**3. `demographic_analysis.py`** — Gender and age group patterns:

- Words with biggest male/female skew (by PMW ratio)
- Age-acquisition curve: at what tier does a word enter each age group's vocabulary?
- Age-group vocabulary size estimates
- Output: Markdown tables + ASCII line charts for age progression

**4. `domain_similarity.py`** — Clustering and comparison:

- Pairwise domain correlation (based on rank vectors)
- Which domains share the most top-N vocabulary?
- Output: Mermaid graph showing domain clusters

**5. `learning_priority.py`** — Practical word lists for learners:

- "High value" words: frequent + broad domain coverage
- "Specialist" words: frequent but domain-concentrated
- Words sorted by domain coverage breadth × frequency
- Output: Ranked markdown tables with coverage scores

**6. `origin_trends.py`** — How word origin composition shifts across frequency tiers:

- Stacked proportion of 和/漢/外/混 at each tier cutoff
- Which origins dominate at high vs. low frequency?
- Output: ASCII stacked bar chart + Mermaid chart

**7. `pmw_variance.py`** — Context-sensitivity analysis:

- Words with highest PMW variance across domains
- Words with highest PMW variance across demographics
- "Universal" words (low variance) vs. "contextual" words (high variance)
- Output: Markdown tables with variance scores

# Common Utility Functions

- JSON loader
- Tier slicer (top N by rank)
- ASCII chart renderer
- Mermaid diagram generator
- Markdown table formatter

# Meaning of each field

**Top-level word identification fields:**

- **rank** — Overall frequency rank across the entire corpus (1 = most frequent)
- **reading** (語彙素読み) — The reading of the lexeme in kana
- **word** (語彙素) — The lexeme / dictionary headword form
- **part_of_speech** (品詞) — Part of speech (noun, verb, adjective, etc.)
- **word_subcategory** (語彙素細分類) — Subcategory/subclass of the lexeme
- **word_origin** (語種) — Word origin type (native Japanese / Sino-Japanese / foreign loanword / mixed)

**Overall corpus statistics:**

- **frequency** — Raw token count across the entire corpus
- **pmw** — Per-million-words frequency across the entire corpus

**Per-domain breakdown** — each domain has three values bundled as an object with `rank`, `frequency`, and `pmw`. The domains are:

_Conversation type:_

- **small_talk** (雑談) — Casual chat / small talk
- **consultation** (用談・相談) — Business talk / consultation
- **meeting** (会議・会合) — Conferences & meetings
- **class** (授業・レッスン) — Classes / lessons

_Location:_

- **outdoors** (屋外) — Outdoors
- **school** (学校) — School
- **transportation** (交通機関) — Public transportation
- **public_commercial** (公共商業施設) — Public commercial facilities
- **home** (自宅) — At home
- **indoors** (室内) — Indoors (general)
- **workplace** (職場) — Workplace

_Speaker gender:_

- **m** (男性) — Male speakers
- **f** (女性) — Female speakers

_Speaker age group:_

- **0_4** (0-4歳) — Ages 0–4
- **5_9** (5-9歳) — Ages 5–9
- **10_14** (10-14歳) — Ages 10–14
- **15_19** (15-19歳) — Ages 15–19
- **20_24** (20-24歳) — Ages 20–24
- **25_29** (25-29歳) — Ages 25–29
- **30_34** (30-34歳) — Ages 30–34
- **35_39** (35-39歳) — Ages 35–39
- **40_44** (40-44歳) — Ages 40–44
- **45_49** (45-49歳) — Ages 45–49
- **50_54** (50-54歳) — Ages 50–54
- **55_59** (55-59歳) — Ages 55–59
- **60_64** (60-64歳) — Ages 60–64
- **65_69** (65-69歳) — Ages 65–69
- **70_74** (70-74歳) — Ages 70–74
- **75_79** (75-79歳) — Ages 75–79
- **80_84** (80-84歳) — Ages 80–84
- **85_89** (85-89歳) — Ages 85–89
- **90_94** (90-94歳) — Ages 90–94
- **unknown** (年齢不明) — Age unknown

# What does PWM mean?

PMW stands for "per million words." It's a normalized frequency measure — it tells you how many times a word appears for every one million words of text in the corpus.

Raw frequency counts aren't great for comparison because they depend on corpus size. If a corpus has 2 million words total and a word appears 100 times, that's different from appearing 100 times in a 200-million-word corpus. PMW normalizes this: `pmw = (raw_frequency / total_words_in_corpus) × 1,000,000`.

So for うん with `pmw: 47581.59`, that means roughly 47,582 occurrences per million words — which makes sense given it's the #1 ranked word in a corpus of everyday spoken Japanese conversation. People say "うん" constantly.

It's especially useful for comparing across the different domains in this dataset, since each domain (small talk, workplace, school, etc.) has a different total word count. The raw frequency numbers aren't directly comparable between domains, but PMW values are.

# Discussion `toon` vs `tsv` format

TSV

```

rank reading word part_of_speech word_subcategory word_origin frequency pmw small_talk_rank small_talk_frequency small_talk_pmw consultation_rank consultation_frequency consultation_pmw meeting_rank meeting_frequency meeting_pmw class_lesson_rank class_lesson_frequency class_lesson_pmw
1 ウン うん 感動詞-一般 -1 和 115108 47581.5888997 2 80709 48623.0136521 2 18837 41850.5138835 1 13785 53135.7206183 2 1777 35721.4650424
2 ダ だ 助動詞 -1 和 115059 47561.3340272 1 80969 48779.6502546 1 21283 47284.837659 2 10893 41988.2049108 1 1914 38475.455313
3 ネ ね 助詞-終助詞 -1 和 62223 25720.7944374 3 44214 26636.6567002 3 10966 24363.3665258 5 6014 23181.5904097 5 1029 20685.0802075

```

TOON

```

[3 ]{rank reading word part_of_speech word_subcategory word_origin frequency pmw small_talk_rank small_talk_frequency small_talk_pmw consultation_rank consultation_frequency consultation_pmw meeting_rank meeting_frequency meeting_pmw class_lesson_rank class_lesson_frequency class_lesson_pmw}:
1 ウン うん 感動詞-一般 -1 和 115108 47581.5888997 2 80709 48623.0136521 2 18837 41850.5138835 1 13785 53135.7206183 2 1777 35721.4650424
2 ダ だ 助動詞 -1 和 115059 47561.3340272 1 80969 48779.6502546 1 21283 47284.837659 2 10893 41988.2049108 1 1914 38475.455313
3 ネ ね 助詞-終助詞 -1 和 62223 25720.7944374 3 44214 26636.6567002 3 10966 24363.3665258 5 6014 23181.5904097 5 1029 20685.0802075

```
