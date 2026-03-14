# Spoken vs. Written Frequency Divergence

Compares CEJC (spontaneous spoken conversation) rankings against the mean normalized rank across 35 external written and media sources. Large positive divergence = word is much more frequent in speech than in writing/media. Large negative divergence = word rarely appears in everyday speech but is common in media/text.

**Methodology:** CEJC combined_rank and each external source rank are each normalized to [0, 1]. Divergence = (mean external normalized rank) − (CEJC normalized rank). Only words present in ≥5 external sources are included.

## Words Much More Frequent in Speech than Written/Media

These words appear frequently in everyday conversation but are rare in written corpora. They represent authentic spoken Japanese vocabulary — often food terms, casual expressions, or local/colloquial vocabulary that doesn't make it into formal text.

| Word | CEJC rank | Divergence | Ext sources |
| ---- | --------- | ---------- | ----------- |
| 竹の子  | 1998      | 0.668      | 9           |
| 端っこ  | 1506      | 0.666      | 20          |
| おいしょ | 1355      | 0.653      | 5           |
| 町会   | 1873      | 0.653      | 5           |
| 中三   | 2153      | 0.652      | 6           |
| 山葵   | 2944      | 0.651      | 10          |
| 下手糞  | 2944      | 0.639      | 10          |
| 鑢    | 3837      | 0.637      | 8           |
| 白子   | 4252      | 0.637      | 7           |
| 桜ん坊  | 4442      | 0.637      | 5           |
| サク   | 1902      | 0.629      | 14          |
| 鯵    | 2199      | 0.629      | 9           |
| 黴菌   | 4880      | 0.625      | 6           |
| 蓮根   | 4442      | 0.624      | 6           |
| 萌やし  | 3966      | 0.618      | 6           |
| マッシュ | 2523      | 0.610      | 11          |
| アロマ  | 1267      | 0.608      | 13          |
| 山の手  | 3322      | 0.608      | 5           |
| サド   | 4442      | 0.604      | 9           |
| 生姜   | 1333      | 0.600      | 17          |
| カワサキ | 2523      | 0.599      | 5           |
| 煎餅   | 1567      | 0.597      | 18          |
| 必修   | 2422      | 0.592      | 5           |
| 入稿   | 4442      | 0.590      | 8           |
| カオ   | 857       | 0.590      | 8           |

## Words Much More Frequent in Written/Media than Speech

These words are common in media and text but rarely appear in spontaneous conversation. They represent narrative, formal, or genre-specific vocabulary — typical in anime/novels but absent from everyday talk.

| Word | CEJC rank | Divergence | Ext sources |
| ---- | --------- | ---------- | ----------- |
| よい   | 20704     | -0.985     | 19          |
| こと   | 20704     | -0.970     | 23          |
| 真実   | 20704     | -0.909     | 30          |
| み    | 20704     | -0.903     | 21          |
| ハ    | 20704     | -0.902     | 10          |
| せい   | 20704     | -0.892     | 23          |
| 兵士   | 20704     | -0.882     | 30          |
| そりゃ  | 20704     | -0.881     | 19          |
| きれい  | 20704     | -0.880     | 21          |
| 任務   | 20704     | -0.877     | 30          |
| 死体   | 20704     | -0.873     | 30          |
| さて   | 20704     | -0.873     | 23          |
| 悲鳴   | 20704     | -0.861     | 26          |
| 竜    | 20704     | -0.859     | 30          |
| 一族   | 20704     | -0.849     | 30          |
| 取り戻す | 20704     | -0.838     | 29          |
| 望み   | 20704     | -0.836     | 27          |
| デ    | 20704     | -0.832     | 21          |
| オ    | 20704     | -0.831     | 9           |
| ブウ   | 20704     | -0.824     | 5           |
| 地位   | 20704     | -0.824     | 30          |
| 行方   | 20704     | -0.820     | 30          |
| 決意   | 20704     | -0.819     | 30          |
| 背後   | 20704     | -0.818     | 30          |
| そうそう | 20704     | -0.816     | 7           |

## Words Exclusive to CEJC (absent from all external sources)

**4,177 words** appear in CEJC but in none of the 35 external sources. Most are proper nouns from the recorded conversations (place names, personal names), very rare spoken-only expressions, or terms too niche for any top-25k word list.

Top 25 by CEJC rank (most frequent among CEJC-only words):

| Word | CEJC rank |
| ---- | --------- |
|      | 9         |
| タチカワ | 1267      |
| いしょ  | 1319      |
| ハルヤ  | 1422      |
| ミカミ  | 1629      |
| ハネダ  | 2153      |
| ＷｉＦｉ | 2153      |
| アタミ  | 2376      |
| サチヒコ | 2467      |
| ハスオ  | 2467      |
| ゲンイチ | 2751      |
| とこ祭  | 2809      |
| 空豆   | 2883      |
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

## Interpretation

- **Food vocabulary dominates CEJC-dominant words**: 竹の子 (bamboo shoots), 山葵 (wasabi), 生姜 (ginger), 蓮根 (lotus root), 鯵 (horse mackerel), 白子 (cod milt). Conversations about cooking and meals are a large part of everyday Japanese speech.
- **CEJC-only words are mostly proper nouns**: タチカワ (Tachikawa), ハルヤ, ミカミ, ハネダ (Haneda) — place names and personal names from recorded conversations. ＷｉＦｉ is a notable exception: a common spoken term absent from all external top-25k lists.
- **Written/media-dominant words are narrative/action vocabulary**: 真実 (truth), 兵士 (soldier), 任務 (mission), 取り戻す (take back), 死体 (corpse), 竜 (dragon), 一族 (clan), 悲鳴 (scream). These appear constantly in anime and novels but almost never come up in natural everyday conversation.

