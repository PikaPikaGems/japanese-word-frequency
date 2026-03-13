# PMW Variance — Context-Sensitivity Analysis

**Source:** CEJC — Corpus of Everyday Japanese Conversation

**PMW (per-million-words)** measures how often a word appears per million words of text. Because different domains and demographic groups have different total word counts, PMW is the right measure for cross-context comparison.

This analysis uses the **coefficient of variation (CV = σ/μ)** across PMW values to measure context-sensitivity:
- **Low CV** → the word appears at roughly the same rate everywhere — it is *universal*
- **High CV** → the word's frequency spikes in certain contexts and is rare in others — it is *contextual*

Analysis covers the top 5,000 words by overall rank.

## Domain Context-Sensitivity

How much does a word's frequency vary across the 11 conversation domains (small talk, meeting, school, workplace, etc.)? High-variance words are strongly tied to specific settings; low-variance words are used equally everywhere.

### Most Contextual Words (highest domain CV — appear unevenly across domains)

| Word     | Reading    | POS                    | Overall Rank | Domain CV | Dominant Domain |
| -------- | ---------- | ---------------------- | ------------ | --------- | --------------- |
| 吐く     | ハク       | 動詞-一般              | 933          | 2.58      | Class/Lesson    |
| 息       | イキ       | 名詞-普通名詞-一般     | 1422         | 2.48      | Class/Lesson    |
| 光る     | ヒカル     | 動詞-一般              | 2422         | 2.39      | Class/Lesson    |
| 縦       | タテ       | 名詞-普通名詞-一般     | 1873         | 2.27      | Class/Lesson    |
| 両手     | リョウテ   | 名詞-普通名詞-一般     | 3599         | 2.26      | Class/Lesson    |
| 爪       | ツメ       | 名詞-普通名詞-一般     | 1382         | 2.25      | Class/Lesson    |
| 現われる | アラワレル | 動詞-一般              | 3103         | 2.24      | Class/Lesson    |
| 吸う     | スウ       | 動詞-一般              | 561          | 2.23      | Class/Lesson    |
| どきどき | ドキドキ   | 副詞                   | 2523         | 2.19      | Class/Lesson    |
| 酸化     | サンカ     | 名詞-普通名詞-サ変可能 | 4649         | 2.18      | Outdoors        |
| 出口     | デグチ     | 名詞-普通名詞-一般     | 3599         | 2.18      | Transportation  |
| 牛蒡     | ゴボウ     | 名詞-普通名詞-一般     | 3966         | 2.17      | Outdoors        |
| アニマル | アニマル   | 名詞-普通名詞-一般     | 4252         | 2.14      | Transportation  |
| 触り     | サワリ     | 名詞-普通名詞-一般     | 3966         | 2.14      | Class/Lesson    |
| 伸ばす   | ノバス     | 動詞-一般              | 1128         | 2.13      | Class/Lesson    |
| 蛍       | ホタル     | 名詞-普通名詞-一般     | 2199         | 2.12      | Outdoors        |
| 白       | ハク       | 接頭辞                 | 4649         | 2.11      | Outdoors        |
| 糞       | クソ       | 名詞-普通名詞-一般     | 1902         | 2.11      | Class/Lesson    |
| 曲がる   | マガル     | 動詞-一般              | 1094         | 2.10      | Transportation  |
| 鑢       | ヤスリ     | 名詞-普通名詞-一般     | 3837         | 2.10      | Class/Lesson    |
| コストコ | コストコ   | 名詞-固有名詞-一般     | 2246         | 2.10      | Transportation  |
| 尻       | シリ       | 名詞-普通名詞-一般     | 1587         | 2.09      | Class/Lesson    |
| 磨く     | ミガク     | 動詞-一般              | 1629         | 2.09      | Class/Lesson    |
| 国語     | コクゴ     | 名詞-普通名詞-一般     | 749          | 2.09      | Class/Lesson    |
| ミニ     | ミニ       | 名詞-普通名詞-一般     | 1902         | 2.08      | Outdoors        |

### Most Universal Words (lowest domain CV — appear evenly across all domains)

These words are the true backbone of spoken Japanese — they appear at similar rates whether you're at work, school, home, or on a train.

| Word   | Reading | POS                    | Overall Rank | Domain CV |
| ------ | ------- | ---------------------- | ------------ | --------- |
| で     | デ      | 助詞-格助詞            | 11           | 0.04      |
| も     | モ      | 助詞-係助詞            | 14           | 0.04      |
| 有る   | アル    | 動詞-非自立可能        | 37           | 0.06      |
| けれど | ケレド  | 助詞-接続助詞          | 34           | 0.07      |
| の     | ノ      | 助詞-格助詞            | 8            | 0.07      |
| の     | ノ      | 助詞-準体助詞          | 6            | 0.07      |
| ね     | ネ      | 助詞-終助詞            | 3            | 0.08      |
| だ     | ダ      | 助動詞                 | 2            | 0.08      |
| られる | ラレル  | 助動詞                 | 196          | 0.08      |
| ない   | ナイ    | 助動詞                 | 23           | 0.09      |
| に     | ニ      | 助詞-格助詞            | 15           | 0.09      |
|        |         | 言いよどみ             | 9            | 0.10      |
| って   | ッテ    | 助詞-副助詞            | 19           | 0.10      |
| か     | カ      | 助詞-副助詞            | 10           | 0.10      |
| が     | ガ      | 助詞-格助詞            | 12           | 0.10      |
| 成る   | ナル    | 動詞-非自立可能        | 49           | 0.11      |
| 上     | ジョウ  | 名詞-普通名詞-一般     | 10047        | 0.11      |
| 人     | ヒト    | 名詞-普通名詞-一般     | 64           | 0.11      |
| 分かる | ワカル  | 動詞-一般              | 67           | 0.11      |
| 直ぐ   | スグ    | 副詞                   | 286          | 0.11      |
| て     | テ      | 助詞-接続助詞          | 5            | 0.11      |
| レバー | レバー  | 名詞-普通名詞-一般     | 11455        | 0.12      |
| 為る   | スル    | 動詞-非自立可能        | 24           | 0.12      |
| 日焼け | ヒヤケ  | 名詞-普通名詞-サ変可能 | 4649         | 0.12      |
| は     | ハ      | 助詞-係助詞            | 13           | 0.12      |

## Demographic Context-Sensitivity

How much does a word's frequency vary across speaker demographics (gender + age groups)? High-variance words are strongly associated with particular speaker profiles.

### Most Demographically Skewed Words (highest demographic CV)

| Word       | Reading    | POS                          | Overall Rank | Demo CV |
| ---------- | ---------- | ---------------------------- | ------------ | ------- |
| 致す       | イタス     | 動詞-非自立可能              | 610          | 3.78    |
| 失礼       | シツレイ   | 名詞-普通名詞-サ変形状詞可能 | 452          | 3.66    |
| センチ     | センチ     | 名詞-普通名詞-助数詞可能     | 801          | 3.43    |
| 組         | クミ       | 名詞-普通名詞-助数詞可能     | 944          | 3.21    |
| ばっ       | バッ       | 副詞                         | 2636         | 3.10    |
| ムサシ     | ムサシ     | 名詞-固有名詞-地名-一般      | 3250         | 3.08    |
| ちまう     | チマウ     | 助動詞                       | 2422         | 3.06    |
| 餡         | アン       | 名詞-普通名詞-一般           | 1162         | 3.03    |
| 放す       | ハナス     | 動詞-一般                    | 2422         | 2.97    |
| 額         | ガク       | 名詞-普通名詞-一般           | 3492         | 2.94    |
| ヤッ       | ヤッ       | 名詞-固有名詞-人名-一般      | 905          | 2.93    |
| ヤマト     | ヤマト     | 名詞-固有名詞-地名-一般      | 2199         | 2.90    |
| 東南       | トウナン   | 名詞-普通名詞-一般           | 4442         | 2.88    |
| ショウナン | ショウナン | 名詞-固有名詞-地名-一般      | 3026         | 2.85    |
| べい       | ベイ       | 助詞-終助詞                  | 1587         | 2.84    |
| 孫         | マゴ       | 名詞-普通名詞-一般           | 2278         | 2.82    |
| ほれ       | ホレ       | 感動詞-一般                  | 2319         | 2.82    |
| 玉         | タマ       | 名詞-普通名詞-助数詞可能     | 1967         | 2.81    |
| 持ち帰る   | モチカエル | 動詞-一般                    | 3492         | 2.81    |
| 伺う       | ウカガウ   | 動詞-一般                    | 2523         | 2.80    |
| 線         | セン       | 接尾辞-名詞的-一般           | 627          | 2.80    |
| 処分       | ショブン   | 名詞-普通名詞-サ変可能       | 4649         | 2.78    |
| 宜しい     | ヨロシイ   | 形容詞-一般                  | 1014         | 2.78    |
| 西瓜       | スイカ     | 名詞-普通名詞-一般           | 2422         | 2.78    |
| どーん     | ドーン     | 副詞                         | 3170         | 2.77    |

### Most Demographically Universal Words (lowest demographic CV)

These words appear at consistent rates across all age groups and both genders — they are part of every Japanese speaker's core vocabulary.

| Word | Reading | POS                    | Overall Rank | Demo CV |
| ---- | ------- | ---------------------- | ------------ | ------- |
| に   | ニ      | 助詞-格助詞            | 15           | 0.09    |
| だ   | ダ      | 助動詞                 | 2            | 0.11    |
| は   | ハ      | 助詞-係助詞            | 13           | 0.13    |
| た   | タ      | 助動詞                 | 4            | 0.14    |
| 為る | スル    | 動詞-非自立可能        | 24           | 0.14    |
| てる | テル    | 助動詞                 | 18           | 0.14    |
| だけ | ダケ    | 助詞-副助詞            | 96           | 0.14    |
| が   | ガ      | 助詞-格助詞            | 12           | 0.15    |
| て   | テ      | 助詞-接続助詞          | 5            | 0.16    |
| で   | デ      | 助詞-格助詞            | 11           | 0.16    |
| 今   | イマ    | 名詞-普通名詞-副詞可能 | 74           | 0.16    |
| 有る | アル    | 動詞-非自立可能        | 37           | 0.17    |
| も   | モ      | 助詞-係助詞            | 14           | 0.17    |
| の   | ノ      | 助詞-準体助詞          | 6            | 0.17    |
| の   | ノ      | 助詞-格助詞            | 8            | 0.18    |
| 前   | マエ    | 名詞-普通名詞-副詞可能 | 114          | 0.19    |
| って | ッテ    | 助詞-副助詞            | 19           | 0.19    |
| 中   | チュウ  | 接尾辞-名詞的-副詞可能 | 463          | 0.19    |
| 良い | ヨイ    | 形容詞-非自立可能      | 33           | 0.20    |
| 無い | ナイ    | 形容詞-非自立可能      | 29           | 0.20    |
| 成る | ナル    | 動詞-非自立可能        | 49           | 0.20    |
| 其処 | ソコ    | 代名詞                 | 99           | 0.21    |
| 未だ | マダ    | 副詞                   | 143          | 0.21    |
| と   | ト      | 助詞-格助詞            | 17           | 0.21    |
| 同じ | オナジ  | 連体詞                 | 266          | 0.21    |

## Most Universal Words Overall (low variance across both domains AND demographics)

Words ranked by combined context-sensitivity score (domain CV + demographic CV). These are the most reliably high-frequency words regardless of *where* or *by whom* a conversation is taking place. A language learner prioritising these words will be prepared for virtually any spoken context.

| Word   | Reading | POS                    | Overall Rank | Overall PMW | Domain CV | Demo CV |
| ------ | ------- | ---------------------- | ------------ | ----------- | --------- | ------- |
| に     | ニ      | 助詞-格助詞            | 15           | 14766.2     | 0.09      | 0.09    |
| だ     | ダ      | 助動詞                 | 2            | 47561.3     | 0.08      | 0.11    |
| で     | デ      | 助詞-格助詞            | 11           | 15667.8     | 0.04      | 0.16    |
| も     | モ      | 助詞-係助詞            | 14           | 14929.1     | 0.04      | 0.17    |
| 有る   | アル    | 動詞-非自立可能        | 37           | 6115.7      | 0.06      | 0.17    |
| の     | ノ      | 助詞-準体助詞          | 6            | 22336.6     | 0.07      | 0.17    |
| は     | ハ      | 助詞-係助詞            | 13           | 15066.7     | 0.12      | 0.13    |
| の     | ノ      | 助詞-格助詞            | 8            | 16468.5     | 0.07      | 0.18    |
| が     | ガ      | 助詞-格助詞            | 12           | 15593.4     | 0.10      | 0.15    |
| 為る   | スル    | 動詞-非自立可能        | 24           | 10999.2     | 0.12      | 0.14    |
| て     | テ      | 助詞-接続助詞          | 5            | 22529.2     | 0.11      | 0.16    |
| てる   | テル    | 助動詞                 | 18           | 13216.5     | 0.13      | 0.14    |
| た     | タ      | 助動詞                 | 4            | 23261.3     | 0.14      | 0.14    |
| って   | ッテ    | 助詞-副助詞            | 19           | 12453.0     | 0.10      | 0.19    |
| 今     | イマ    | 名詞-普通名詞-副詞可能 | 74           | 2059.8      | 0.13      | 0.16    |
| だけ   | ダケ    | 助詞-副助詞            | 96           | 1359.1      | 0.16      | 0.14    |
| ない   | ナイ    | 助動詞                 | 23           | 11062.5     | 0.09      | 0.22    |
| 成る   | ナル    | 動詞-非自立可能        | 49           | 3879.8      | 0.11      | 0.20    |
| 良い   | ヨイ    | 形容詞-非自立可能      | 33           | 6925.5      | 0.12      | 0.20    |
| 無い   | ナイ    | 形容詞-非自立可能      | 29           | 8179.7      | 0.13      | 0.20    |
| ね     | ネ      | 助詞-終助詞            | 3            | 25720.8     | 0.08      | 0.25    |
| けれど | ケレド  | 助詞-接続助詞          | 34           | 6860.2      | 0.07      | 0.27    |
| と     | ト      | 助詞-格助詞            | 17           | 14232.6     | 0.14      | 0.21    |
| 前     | マエ    | 名詞-普通名詞-副詞可能 | 114          | 1061.5      | 0.17      | 0.19    |
| 言う   | イウ    | 動詞-一般              | 22           | 11759.0     | 0.15      | 0.22    |

## Key Insights

- **Most contextual words** (highest domain CV): 吐く (Class/Lesson), 息 (Class/Lesson), 光る (Class/Lesson). These words spike in their dominant domain and are rarely used elsewhere.

- **Most universal words** (lowest domain CV): で (デ), も (モ), 有る (アル). These appear at the same rate regardless of conversational context.

- **Domain variance tends to be higher than demographic variance** for most words. This suggests that *what you're talking about* (domain) has more influence on word choice than *who you are* (gender/age).

- **Low-rank (high-frequency) words are generally more universal.** Function words, auxiliaries, and core verbs appear everywhere. Content words (especially nouns) are much more context-dependent.
