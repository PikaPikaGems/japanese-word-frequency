# Spoken vs. Written Frequency Divergence

Compares CEJC (spontaneous spoken conversation) rankings against the mean normalized rank across 35 external written and media sources. Large positive divergence = word is much more frequent in speech than in writing/media. Large negative divergence = word rarely appears in everyday speech but is common in media/text.

**Methodology:** CEJC combined_rank and each external source rank are each normalized to [0, 1]. Divergence = (mean external normalized rank) − (CEJC normalized rank). Only words present in ≥5 external sources are included.

## Words Much More Frequent in Speech than Written/Media

These words appear frequently in everyday conversation but are rare in written corpora. They represent authentic spoken Japanese vocabulary — often food terms, casual expressions, or local/colloquial vocabulary that doesn't make it into formal text.

| Word  | CEJC rank | Divergence | Ext sources |
| ----- | --------- | ---------- | ----------- |
| コタ    | 2153      | 0.679      | 5           |
| 端っこ   | 1506      | 0.657      | 21          |
| おいしょ  | 1355      | 0.653      | 5           |
| 町会    | 1873      | 0.653      | 5           |
| 中三    | 2153      | 0.652      | 6           |
| 白子    | 4252      | 0.637      | 7           |
| 黴菌    | 4880      | 0.625      | 6           |
| カオ    | 857       | 0.623      | 9           |
| 山葵    | 2944      | 0.622      | 20          |
| 竹の子   | 1998      | 0.615      | 10          |
| 胡瓜    | 1094      | 0.615      | 20          |
| 山の手   | 3322      | 0.607      | 5           |
| 蓮根    | 4442      | 0.607      | 7           |
| 年取る   | 2199      | 0.606      | 11          |
| サク    | 1902      | 0.604      | 15          |
| 高一    | 2090      | 0.601      | 8           |
| 必修    | 2422      | 0.592      | 5           |
| マッシュ  | 2523      | 0.590      | 13          |
| 入稿    | 4442      | 0.590      | 8           |
| 鑢     | 3837      | 0.590      | 12          |
| ユウカ   | 4442      | 0.587      | 5           |
| 盛り合わせ | 4880      | 0.587      | 7           |
| 片栗粉   | 4252      | 0.586      | 13          |
| アロマ   | 1267      | 0.585      | 14          |
| 発泡    | 3837      | 0.581      | 11          |

## Words Much More Frequent in Written/Media than Speech

These words are common in media and text but rarely appear in spontaneous conversation. They represent narrative, formal, or genre-specific vocabulary — typical in anime/novels but absent from everyday talk.

| Word | CEJC rank | Divergence | Ext sources |
| ---- | --------- | ---------- | ----------- |
| よい   | 20704     | -0.983     | 21          |
| こと   | 20704     | -0.972     | 27          |
| 俑    | 20704     | -0.958     | 29          |
| さて   | 20704     | -0.914     | 27          |
| み    | 20704     | -0.911     | 23          |
| 真実   | 20704     | -0.906     | 33          |
| ハ    | 20704     | -0.899     | 14          |
| せい   | 20704     | -0.890     | 27          |
| 死体   | 20704     | -0.880     | 32          |
| 任務   | 20704     | -0.877     | 33          |
| きれい  | 20704     | -0.876     | 24          |
| 兵士   | 20704     | -0.873     | 33          |
| オ    | 20704     | -0.868     | 12          |
| そりゃ  | 20704     | -0.861     | 22          |
| ちゃ   | 20704     | -0.860     | 27          |
| 取り戻す | 20704     | -0.859     | 31          |
| ブウ   | 20704     | -0.856     | 5           |
| 悲鳴   | 20704     | -0.854     | 28          |
| デ    | 20704     | -0.852     | 24          |
| 稿    | 20704     | -0.840     | 33          |
| 盲    | 20704     | -0.840     | 34          |
| うりゃ  | 20704     | -0.835     | 7           |
| そうそう | 20704     | -0.834     | 10          |
| 一族   | 20704     | -0.833     | 33          |
| 竜    | 20704     | -0.827     | 34          |

## Words Exclusive to CEJC (absent from all external sources)

**4,073 words** appear in CEJC but in none of the 35 external sources. Most are proper nouns from the recorded conversations (place names, personal names), very rare spoken-only expressions, or terms too niche for any top-25k word list.

Top 25 by CEJC rank (most frequent among CEJC-only words):

| Word | CEJC rank |
| ---- | --------- |
|      | 9         |
| タチカワ | 1267      |
| ハルヤ  | 1422      |
| ミカミ  | 1629      |
| ハネダ  | 2153      |
| アタミ  | 2376      |
| サチヒコ | 2467      |
| ハスオ  | 2467      |
| ゲンイチ | 2751      |
| とこ祭  | 2809      |
| フウカ  | 3103      |
| オギクボ | 3170      |
| サッポン | 3170      |
| タマガワ | 3322      |
| フチュウ | 3322      |
| マツバラ | 3322      |
| 略々   | 3322      |
| 小啄木鳥 | 3410      |
| クモン  | 3492      |
| ササイ  | 3492      |
| ヤチヨ  | 3492      |
| 岩牡蠣  | 3599      |
| フクマ  | 3704      |
| モギ   | 3704      |
| ユズキ  | 3704      |

## Interpretation

- **Food vocabulary dominates CEJC-dominant words**: 竹の子 (bamboo shoots), 山葵 (wasabi), 生姜 (ginger), 蓮根 (lotus root), 鯵 (horse mackerel), 白子 (cod milt). Conversations about cooking and meals are a large part of everyday Japanese speech.
- **CEJC-only words are mostly proper nouns**: タチカワ (Tachikawa), ハルヤ, ミカミ, ハネダ (Haneda) — place names and personal names from recorded conversations. ＷｉＦｉ is a notable exception: a common spoken term absent from all external top-25k lists.
- **Written/media-dominant words are narrative/action vocabulary**: 真実 (truth), 兵士 (soldier), 任務 (mission), 取り戻す (take back), 死体 (corpse), 竜 (dragon), 一族 (clan), 悲鳴 (scream). These appear constantly in anime and novels but almost never come up in natural everyday conversation.

