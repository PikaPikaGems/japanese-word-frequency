# Cross-Source Rank Variance Analysis

How consistently do the 35 sources agree on a word's frequency? Low variance = all sources agree; high variance = sources strongly disagree.

## Universal Core Words (basic tier in most sources)

Words ranked in the top ~1,000 (tier 5 = basic) by the largest number of sources, excluding tier 1 (rare/absent) as indistinguishable from 'not in source'. These words have the strongest cross-corpus consensus for being high-priority vocabulary.

- Basic in **25+** sources: **300** words
- Basic in **20+** sources: **490** words
- Basic in **15+** sources: **698** words
- Basic in **10+** sources: **977** words

| Word | Overall rank | Basic in N sources | Present in N sources |
| ---- | ------------ | ------------------ | -------------------- |
| 人    | 64           | 35                 | 35                   |
| 中    | 174          | 35                 | 35                   |
| 何    | 21           | 34                 | 35                   |
| 方    | 87           | 34                 | 35                   |
| 後    | 93           | 34                 | 35                   |
| 所    | 134          | 34                 | 35                   |
| 物    | 149          | 34                 | 35                   |
| 日    | 180          | 34                 | 34                   |
| 上    | 212          | 34                 | 35                   |
| 他    | 294          | 34                 | 34                   |
| 者    | 405          | 34                 | 35                   |
| 用    | 484          | 34                 | 35                   |
| 大    | 792          | 34                 | 35                   |
| 事    | 53           | 33                 | 35                   |
| 私    | 73           | 33                 | 35                   |
| 今    | 74           | 33                 | 35                   |
| 時    | 78           | 33                 | 35                   |
| 二    | 88           | 33                 | 35                   |
| 前    | 114          | 33                 | 35                   |
| 子    | 190          | 33                 | 35                   |
| 分    | 251          | 33                 | 35                   |
| 下    | 255          | 33                 | 34                   |
| 目    | 310          | 33                 | 34                   |
| 手    | 332          | 33                 | 34                   |
| 水    | 387          | 33                 | 35                   |
| 度    | 390          | 33                 | 35                   |
| 間    | 460          | 33                 | 35                   |
| 以上   | 480          | 33                 | 34                   |
| 彼    | 527          | 33                 | 35                   |
| 力    | 806          | 33                 | 35                   |

## Lowest Rank Variance (universally consistent words)

Words present in 10+ sources where normalized ranks agree most closely. These words have nearly the same position across every corpus type — a reliable signal regardless of which source you use.

| Word | Overall rank | Normalized std | N sources |
| ---- | ------------ | -------------- | --------- |
| は    | 13           | 0.0001         | 29        |
| の    | 6            | 0.0002         | 29        |
| に    | 15           | 0.0002         | 29        |
| を    | 38           | 0.0004         | 29        |
| だけ   | 96           | 0.0030         | 30        |
| 持つ   | 126          | 0.0035         | 31        |
| まで   | 112          | 0.0047         | 31        |
| か    | 10           | 0.0057         | 29        |
| 日    | 180          | 0.0059         | 34        |
| 中    | 174          | 0.0067         | 35        |
| 人    | 64           | 0.0069         | 35        |
| や    | 146          | 0.0072         | 29        |
| 言う   | 22           | 0.0075         | 31        |
| 別    | 176          | 0.0080         | 32        |
| 他    | 294          | 0.0082         | 34        |
| より   | 239          | 0.0086         | 33        |
| どう   | 76           | 0.0087         | 32        |
| 入る   | 108          | 0.0091         | 31        |
| 後    | 93           | 0.0092         | 35        |
| 相手   | 839          | 0.0099         | 32        |
| しか   | 187          | 0.0106         | 30        |
| など   | 952          | 0.0115         | 31        |
| 元    | 839          | 0.0115         | 34        |
| 始める  | 471          | 0.0125         | 31        |
| 作る   | 136          | 0.0127         | 31        |
| 近く   | 673          | 0.0130         | 31        |
| れる   | 86           | 0.0130         | 27        |
| 様    | 127          | 0.0139         | 34        |
| へ    | 440          | 0.0140         | 29        |
| 上    | 212          | 0.0140         | 35        |

## Highest Tier Variance (most contested words)

Words present in 10+ sources where tier assignments disagree most. A word ranked 'basic' in some corpora but 'advanced' in others suggests strong domain-specificity: highly frequent in one medium but rare in another.

| Word | Overall rank | Tier std | Best tier | Worst tier | N sources |
| ---- | ------------ | -------- | --------- | ---------- | --------- |
| 生る   | 16266        | 1.45     | basic     | advanced   | 30        |
| ハア   | 13446        | 1.45     | basic     | advanced   | 13        |
| 槽    | 16266        | 1.41     | basic     | advanced   | 35        |
| 煮    | 4649         | 1.41     | basic     | advanced   | 32        |
| 支    | 13446        | 1.38     | basic     | advanced   | 32        |
| 鱒    | 8120         | 1.37     | basic     | advanced   | 29        |
| なんだ  | 8120         | 1.37     | basic     | advanced   | 22        |
| 喪    | 16266        | 1.37     | basic     | advanced   | 33        |
| 鵜    | 6059         | 1.36     | basic     | advanced   | 27        |
| 講    | 4880         | 1.36     | basic     | advanced   | 32        |
| 溜め   | 7460         | 1.36     | basic     | advanced   | 28        |
| 南下   | 20704        | 1.35     | basic     | advanced   | 34        |
| 苑    | 13446        | 1.35     | basic     | advanced   | 29        |
| 碁    | 11455        | 1.34     | basic     | advanced   | 27        |
| 浸ける  | 3322         | 1.34     | basic     | advanced   | 29        |
| 何時   | 188          | 1.34     | basic     | advanced   | 26        |
| なる   | 13446        | 1.33     | basic     | advanced   | 30        |
| 駄    | 7460         | 1.33     | basic     | advanced   | 34        |
| 彼奴   | 601          | 1.33     | basic     | advanced   | 32        |
| ウッ   | 20704        | 1.33     | basic     | advanced   | 17        |
| 誤    | 20704        | 1.32     | basic     | advanced   | 32        |
| 葬    | 10047        | 1.32     | basic     | advanced   | 33        |
| 旨い   | 236          | 1.31     | basic     | advanced   | 31        |
| 走    | 11455        | 1.31     | basic     | advanced   | 34        |
| 模試   | 4252         | 1.31     | basic     | advanced   | 30        |
| 唯々   | 8967         | 1.31     | basic     | advanced   | 32        |
| 兎に角  | 732          | 1.30     | basic     | advanced   | 33        |
| 和紙   | 11455        | 1.30     | basic     | advanced   | 31        |
| 痔    | 16266        | 1.30     | basic     | advanced   | 29        |
| 見付ける | 1069         | 1.30     | basic     | advanced   | 26        |

## Notable Patterns

### Consistently ranked words are abstract 漢語 (Sino-Japanese)

The words with lowest variance tend to be general-purpose Sino-Japanese vocabulary: 判断 (judgment), 原因 (cause), 理解 (understanding), 可能 (possible), 重要 (important), 影響 (influence). These terms appear at similar frequencies in speech, literature, media, and web text — making them reliable learning targets regardless of which frequency list you use.

### High-variance words are often kanji/kana spelling alternates

Many highly contested words are archaic or literary kanji spellings of common words: 其れ (それ), 此れ (これ), 此の (この), 矢張り (やはり), 為る (する). Literary corpora (AOZORA, NOVELS) rank these as frequent; modern web/subtitle corpora rarely see them, assigning rare or advanced tiers. The underlying word is common, but its kanji spelling is domain-specific.

