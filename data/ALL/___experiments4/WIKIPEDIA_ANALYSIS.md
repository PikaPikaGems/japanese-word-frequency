# Wikipedia Dataset Comparison: WIKIPEDIA_V2 vs ADNO

**Primary reference:** `BCCWJ_LUW_rank` (anchor, BCCWJ_LUW_anchor/consolidated.csv)  
**Secondary reference:** `RSPEER`  
**Rows loaded:** 25,000

---

## 1. Spearman Rank Correlation

| Dataset | n vs BCCWJ_LUW | ρ vs BCCWJ_LUW | n vs RSPEER | ρ vs RSPEER |
|---|---|---|---|---|
| `WIKIPEDIA_V2` | 11,640 | 0.4108 | 10,368 | 0.6761 |
| `ADNO` | 10,364 | 0.3954 | 9,486 | 0.6728 |

Spearman ρ between WIKIPEDIA_V2 and ADNO (shared 9,830 words): **0.8745**

---

## 2. Top-N Jaccard Overlap

| Top-N | WIKIPEDIA_V2 ∩ BCCWJ_LUW | ADNO ∩ BCCWJ_LUW | WIKIPEDIA_V2 ∩ ADNO |
|---|---|---|---|
| 100 | 0.210 | 0.200 | 0.470 |
| 500 | 0.201 | 0.174 | 0.623 |
| 1,000 | 0.227 | 0.187 | 0.640 |
| 5,000 | 0.319 | 0.289 | 0.711 |

---

## 3. Top-500 Discrepancies

### In WIKIPEDIA_V2 top 500, absent from ADNO (19 words)

| WIKIPEDIA_V2 rank | Word | Reading |
|---|---|---|
| 24 | として | として |
| 47 | という | という |
| 69 | により | により |
| 76 | による | による |
| 87 | によって | によって |
| 138 | について | について |
| 143 | において | において |
| 178 | 株式会社 | かぶしきがいしゃ |
| 195 | 小学校 | しょうがっこう |
| 226 | における | における |
| 302 | 中学校 | ちゅうがっこう |
| 339 | 所在地 | しょざいち |
| 370 | に対して | にたいして |
| 395 | でも | でも |
| 416 | に関する | - |
| 447 | 自動車 | じどうしゃ |
| 453 | とともに | とともに |
| 494 | 一つ | ひとつ |
| 496 | アメリカ合衆国 | アメリカがっしゅうこく |

### In ADNO top 500, absent from WIKIPEDIA_V2 (3 words)

| ADNO rank | Word | Reading |
|---|---|---|
| 26 | なっ | なっ |
| 375 | 関する | かんする |
| 477 | 本作 | ほんさく |
