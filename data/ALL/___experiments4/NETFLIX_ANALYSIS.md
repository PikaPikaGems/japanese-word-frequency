# Netflix Dataset Comparison: NETFLIX vs DD2_MORPHMAN_NETFLIX

**Reference:** `ANIME_JDRAMA_rank` (anchor, ANIME_JDRAMA_anchor/consolidated.csv)  
**Rows loaded:** 25,000

---

## 1. Spearman Rank Correlation vs ANIME_JDRAMA

| Dataset | Valid pairs with ANIME_JDRAMA | Spearman ρ |
|---|---|---|
| `NETFLIX` | 19,513 | 0.7247 |
| `DD2_MORPHMAN_NETFLIX` | 12,004 | 0.6929 |

Spearman ρ between NETFLIX and DD2_MORPHMAN_NETFLIX (shared 11,205 words): **0.7958**

---

## 2. Top-N Jaccard Overlap

| Top-N | NETFLIX ∩ ANIME_JDRAMA | DD2 ∩ ANIME_JDRAMA | NETFLIX ∩ DD2 |
|---|---|---|---|
| 100 | 0.636 | 0.400 | 0.506 |
| 500 | 0.640 | 0.413 | 0.513 |
| 1,000 | 0.635 | 0.422 | 0.534 |
| 5,000 | 0.608 | 0.425 | 0.508 |

---

## 3. Words Netflix Ranks in Top 300 That DD2 Filtered Out

These are words NETFLIX ranks in its top 300 but DD2_MORPHMAN_NETFLIX either
removed entirely (absent) or ranked far lower (>2000). DD2 excludes proper names
using a UniDic name filter — words appearing here are likely character/person names
or other noise entries.

**Total:** 71 words

| NETFLIX rank | Word | Reading | DD2 rank |
|---|---|---|---|
| 9 | する | する | 10,746 |
| 17 | ん | ん | absent |
| 25 | う | う | absent |
| 25 | 卯 | う | absent |
| 25 | 鵜 | う | absent |
| 31 | いい | いい | 16,719 |
| 33 | なる | なる | 17,060 |
| 47 | くれる | くれる | 5,997 |
| 48 | それ | それ | 8,431 |
| 50 | でも | でも | absent |
| 54 | 久留 | くる | absent |
| 54 | 繰る | くる | 22,158 |
| 55 | お前 | おまえ | absent |
| 57 | けど | けど | absent |
| 58 | お | お | 8,595 |
| 68 | 僕 | ぼく | 10,587 |
| 75 | よう | よう | 5,298 |
| 77 | あ | あ | 3,741 |
| 92 | く | く | 3,231 |
| 94 | ため | ため | 20,164 |
| 106 | ぬ | ぬ | absent |
| 109 | 是 | ぜ | 22,101 |
| 110 | のに | のに | absent |
| 113 | 佳い | よい | absent |
| 122 | やめる | やめる | 22,476 |
| 124 | かも | かも | 6,148 |
| 129 | 一 | いち | absent |
| 131 | だって | だって | absent |
| 140 | 了 | りょう | absent |
| 142 | ダメ | ダメ | absent |
| 146 | なんだ | なんだ | 21,486 |
| 148 | 帰る | かえる | absent |
| 150 | だから | だから | absent |
| 152 | ら | ら | 9,055 |
| 156 | よく | よく | 5,055 |
| 167 | じゃあ | じゃあ | absent |
| 173 | という | という | absent |
| 175 | 老い | おい | 14,213 |
| 176 | 本当に | ほんとうに | absent |
| 178 | あんた | あんた | absent |
| 180 | とか | とか | absent |
| 184 | ほう | ほう | 2,073 |
| 194 | バカ | バカ | absent |
| 195 | だが | だが | absent |
| 200 | 信じる | しんじる | absent |
| 209 | 好 | こう | 4,005 |
| 211 | 私たち | わたしたち | absent |
| 212 | お願い | おねがい | absent |
| 213 | 一緒に | いっしょに | absent |
| 221 | として | として | absent |
| 222 | どうも | どうも | absent |
| 224 | ママ | ママ | absent |
| 226 | 有 | ゆう | 8,103 |
| 234 | うち | うち | 6,225 |
| 240 | ウソ | ウソ | absent |
| 241 | そこ | そこ | 2,708 |
| 247 | 万 | まん | 19,316 |
| 248 | 俺たち | おれたち | absent |
| 254 | 何だ | なんだ | 21,486 |
| 255 | うる | うる | 14,489 |
| 261 | いつも | いつも | absent |
| 262 | もん | もん | 2,338 |
| 270 | せい | せい | 21,378 |
| 272 | ま | ま | 2,512 |
| 273 | 在 | ざい | 23,069 |
| 275 | 翔ける | かける | absent |
| 278 | パパ | パパ | absent |
| 283 | 美味い | うまい | absent |
| 284 | それで | それで | absent |
| 293 | 我々 | われわれ | absent |
| 295 | ので | ので | absent |
