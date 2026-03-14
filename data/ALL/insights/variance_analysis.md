# Cross-Source Rank Variance Analysis

How consistently do the 35 sources agree on a word's frequency? Low variance = all sources agree; high variance = sources strongly disagree.

## Universal Core Words (basic tier in most sources)

Words ranked in the top ~1,000 (tier 5 = basic) by the largest number of sources, excluding tier 1 (rare/absent) as indistinguishable from 'not in source'. These words have the strongest cross-corpus consensus for being high-priority vocabulary.

- Basic in **25+** sources: **114** words
- Basic in **20+** sources: **335** words
- Basic in **15+** sources: **510** words
- Basic in **10+** sources: **764** words

| Word | Overall rank | Basic in N sources | Present in N sources |
| ---- | ------------ | ------------------ | -------------------- |
| 者    | 405          | 32                 | 33                   |
| 何    | 21           | 30                 | 34                   |
| 自分   | 137          | 30                 | 32                   |
| 時間   | 160          | 30                 | 32                   |
| 意味   | 271          | 30                 | 32                   |
| 関係   | 361          | 30                 | 32                   |
| 必要   | 390          | 30                 | 31                   |
| 場所   | 463          | 30                 | 32                   |
| 以上   | 480          | 30                 | 32                   |
| 人間   | 505          | 30                 | 32                   |
| 相手   | 839          | 30                 | 31                   |
| 方    | 87           | 29                 | 32                   |
| だけ   | 96           | 29                 | 29                   |
| まで   | 112          | 29                 | 30                   |
| 最初   | 241          | 29                 | 32                   |
| 仕事   | 261          | 29                 | 32                   |
| 問題   | 380          | 29                 | 32                   |
| 場合   | 399          | 29                 | 32                   |
| 世界   | 585          | 29                 | 32                   |
| 力    | 806          | 29                 | 33                   |
| 存在   | 2153         | 29                 | 32                   |
| 別    | 176          | 28                 | 31                   |
| 考える  | 204          | 28                 | 30                   |
| 子供   | 252          | 28                 | 32                   |
| 同じ   | 266          | 28                 | 32                   |
| 最後   | 318          | 28                 | 32                   |
| 言葉   | 439          | 28                 | 32                   |
| 以外   | 585          | 28                 | 31                   |
| そして  | 784          | 28                 | 30                   |
| 方法   | 1382         | 28                 | 32                   |

## Lowest Rank Variance (universally consistent words)

Words present in 10+ sources where normalized ranks agree most closely. These words have nearly the same position across every corpus type — a reliable signal regardless of which source you use.

| Word | Overall rank | Normalized std | N sources |
| ---- | ------------ | -------------- | --------- |
| だけ   | 96           | 0.0031         | 29        |
| 一    | 65           | 0.0097         | 25        |
| 近く   | 673          | 0.0136         | 30        |
| 判断   | 1607         | 0.0209         | 31        |
| 原因   | 2809         | 0.0211         | 32        |
| 女性   | 944          | 0.0223         | 32        |
| 伝える  | 1226         | 0.0235         | 30        |
| 他    | 294          | 0.0237         | 32        |
| 過去   | 1346         | 0.0238         | 32        |
| 理解   | 1382         | 0.0243         | 31        |
| 二    | 88           | 0.0244         | 25        |
| よい   | 20704        | 0.0255         | 21        |
| 可能   | 829          | 0.0275         | 32        |
| 始める  | 471          | 0.0278         | 30        |
| 重要   | 1945         | 0.0282         | 32        |
| 死    | 6881         | 0.0283         | 32        |
| 効果   | 1844         | 0.0284         | 32        |
| 意見   | 1052         | 0.0291         | 30        |
| 以前   | 3410         | 0.0291         | 32        |
| 全く   | 519          | 0.0292         | 30        |
| 内容   | 898          | 0.0305         | 32        |
| 影響   | 1998         | 0.0307         | 32        |
| 一部   | 2199         | 0.0308         | 32        |
| のみ   | 2688         | 0.0311         | 30        |
| 現在   | 2581         | 0.0311         | 32        |
| 進める  | 1703         | 0.0312         | 30        |
| 短い   | 863          | 0.0318         | 30        |
| 活動   | 1483         | 0.0330         | 32        |
| 性格   | 1873         | 0.0333         | 32        |
| 事実   | 4442         | 0.0341         | 32        |

## Highest Tier Variance (most contested words)

Words present in 10+ sources where tier assignments disagree most. A word ranked 'basic' in some corpora but 'advanced' in others suggests strong domain-specificity: highly frequent in one medium but rare in another.

| Word | Overall rank | Tier std | Best tier | Worst tier | N sources |
| ---- | ------------ | -------- | --------- | ---------- | --------- |
| 其れ   | 36           | 1.50     | basic     | advanced   | 12        |
| 此れ   | 42           | 1.49     | basic     | advanced   | 11        |
| 此の   | 80           | 1.44     | basic     | advanced   | 12        |
| ハア   | 13446        | 1.43     | basic     | advanced   | 12        |
| 一寸   | 51           | 1.41     | basic     | advanced   | 18        |
| 此方   | 130          | 1.38     | basic     | advanced   | 15        |
| 矢張り  | 81           | 1.37     | basic     | advanced   | 10        |
| なんだ  | 8120         | 1.37     | basic     | advanced   | 22        |
| 其処   | 99           | 1.36     | basic     | advanced   | 15        |
| 万    | 223          | 1.35     | basic     | advanced   | 31        |
| 女    | 766          | 1.34     | basic     | advanced   | 33        |
| 成る程  | 162          | 1.34     | basic     | advanced   | 11        |
| 上    | 212          | 1.33     | basic     | advanced   | 33        |
| 兎に角  | 732          | 1.33     | basic     | advanced   | 13        |
| さあ   | 1240         | 1.32     | basic     | advanced   | 29        |
| 若し   | 329          | 1.32     | basic     | advanced   | 16        |
| 為る   | 24           | 1.32     | basic     | advanced   | 14        |
| 明日   | 377          | 1.32     | basic     | advanced   | 32        |
| 頷く   | 20704        | 1.31     | basic     | advanced   | 15        |
| 遣る   | 46           | 1.30     | basic     | advanced   | 19        |
| 呟く   | 8120         | 1.30     | basic     | advanced   | 19        |
| 足    | 491          | 1.30     | basic     | advanced   | 32        |
| 見付かる | 1945         | 1.30     | basic     | advanced   | 12        |
| 口    | 656          | 1.30     | basic     | advanced   | 33        |
| なる   | 13446        | 1.30     | basic     | advanced   | 29        |
| 直ぐ   | 286          | 1.29     | basic     | advanced   | 19        |
| 勿論   | 407          | 1.29     | basic     | advanced   | 25        |
| 筈    | 667          | 1.28     | basic     | advanced   | 24        |
| 貴方   | 356          | 1.28     | basic     | advanced   | 27        |
| 空    | 2581         | 1.28     | basic     | advanced   | 32        |

## Notable Patterns

### Consistently ranked words are abstract 漢語 (Sino-Japanese)

The words with lowest variance tend to be general-purpose Sino-Japanese vocabulary: 判断 (judgment), 原因 (cause), 理解 (understanding), 可能 (possible), 重要 (important), 影響 (influence). These terms appear at similar frequencies in speech, literature, media, and web text — making them reliable learning targets regardless of which frequency list you use.

### High-variance words are often kanji/kana spelling alternates

Many highly contested words are archaic or literary kanji spellings of common words: 其れ (それ), 此れ (これ), 此の (この), 矢張り (やはり), 為る (する). Literary corpora (AOZORA, NOVELS) rank these as frequent; modern web/subtitle corpora rarely see them, assigning rare or advanced tiers. The underlying word is common, but its kanji spelling is domain-specific.

