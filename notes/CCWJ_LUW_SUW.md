# BCCWJ_LUW vs BCCWJ_SUW — What's the Difference?

Both datasets come from the exact same corpus: the BCCWJ (Balanced Corpus of Contemporary Written Japanese), Japan's 104.3-million-word reference corpus of written text spanning books, magazines, newspapers, blogs, legal documents, and more. Both datasets have 25,000 entries. Both were packaged from the same source by toasted-nutbread.

So why do their rankings look so different?

The answer is one decision made during tokenization: **how long is a "word"?**

---

## The Core Idea: Short vs Long Units

**SUW (Short Unit Word)** is the smallest unit that still functions grammatically. Think of it like splitting at every possible morpheme boundary. Every particle, every auxiliary verb, every numeral component is its own token.

**LUW (Long Unit Word)** is larger — it groups together compound expressions and verb+auxiliary chains that function as a single semantic unit. Think of it like "what would a native speaker consider one 'thing' to look up or learn?"

Both are defined by NINJAL and used in official BCCWJ annotation. Neither is more "correct" — they answer different questions.

---

## Dictionary Forms: What Gets Counted?

Both datasets list entries in **lemma (dictionary) form**. You will see `食べる`, not `食べた` or `食べて` or `食べました` as separate entries. When the corpus contains a sentence like `昨日すしを食べました`, the occurrence of `食べました` is counted toward `食べる`'s frequency total. Same for `食べられない`, `食べてみた`, `食べ終わった` — all fold back into `食べる`.

You can confirm this by checking either DATA.csv: neither contains `食べた` or `食べて` as standalone entries. What you do find separately is genuinely distinct vocabulary built with `食べ` as a prefix: `食べ物` (food), `食べ方` (way of eating), `食べ過ぎる` (overeat) — these are different lexical items, not inflected forms of `食べる`.

So: **yes, `食べました` and `食べられない` count toward `食べる`** in both datasets. The frequency rank reflects usage of the word in all its inflected forms.

That said, there is an important difference in what happens to the *rest* of a verb phrase when it passes through each tokenizer:

- In **SUW**: `食べている` splits into three units — `食べる` (+1), `て` (+1), `居る` (+1, the lemma for いる). Each morpheme gets its own tally.
- In **LUW**: `食べている` splits at the boundary between the content verb and the compound auxiliary — `食べる` (+1) and `ている` (+1, as a fused grammatical unit). The `て` doesn't get counted separately; it fuses with `いる` to form `ている`.

For `食べました`, LUW treats the whole form as a single token — the polite past suffix `ました` fuses directly with `食べ` into one unit — and lemmatizes it to `食べる`. In SUW, `食べました` is split into `食べる`, `ます`, and `た`, so both `ます` and `た` also each get a count.

This is exactly why `ている` has such a high LUW rank (13th most frequent) — every verb phrase in the progressive form credits it. And why `ます` and `た` are also very high in both lists — they're counted separately every time any polite or past verb appears.

---

## What This Looks Like in Practice

### 1. Compound verb+auxiliary forms

This is the most striking difference for language learners.

In Japanese, verbs frequently attach auxiliaries that change the temporal or aspectual meaning:
- `食べている` — is eating (progressive)
- `食べてくる` — goes and eats, comes back having eaten
- `食べてしまう` — ends up eating, finishes eating (often with regret)

Under **SUW**, these are split. `て` is one token. `いる`, `くる`, `しまう` are separate tokens. The individual components get counted each time they appear with *any* verb.

Under **LUW**, the `て` fuses with the following auxiliary to form compound tokens like `ている`, `てくる`, `てしまう`. These appear in the LUW list as independent high-frequency entries:

| Compound form | LUW rank | In SUW top 25k? |
|---------------|----------|-----------------|
| ている         | 13       | No — split into `て` + `いる` |
| てくる         | 66       | No |
| てしまう       | 72       | No |
| ていく         | 90       | No |
| てみる         | 97       | No |
| てくれる       | 101      | No |
| てくださる     | 115      | No |
| ておく         | 175      | No |
| てもらう       | 205      | No |
| ていただく     | 316      | No |

These are very common grammatical constructions that every learner encounters constantly. LUW surfaces them directly. SUW spreads their frequency across the component morphemes.

Similarly, LUW has entries like `について` (rank 61), `によって` (rank 99), `ではない` (rank 65), `という` (rank 27), `のだ` (rank 28), `のです` (rank 34), `である` (rank 26). None of these appear as distinct entries in SUW — they get split into their constituent particles.

### 2. Numbers and counters

This difference is dramatic.

In compound numbers like 三十 (30), 百五十 (150), or 二千 (2,000), the individual numerals appear many times. Under SUW, `一`, `十`, `百`, `千` are each counted every single time they appear in any compound. Under LUW, the larger compound number is treated as one unit, so the individual digits don't inflate as much.

The result: numbers are ranked much higher (more frequent) in SUW than in LUW.

| Word | LUW rank | SUW rank | Difference |
|------|----------|----------|------------|
| 一 (one)      | 74   | 22  | +52 places higher in SUW |
| 十 (ten)      | 703  | 30  | +673 |
| 百 (hundred)  | 2366 | 116 | +2,250 |
| 千 (thousand) | 7376 | 81  | +7,295 |

`千` is rank 81 in SUW — placed between common particles and basic verbs. In LUW it's rank 7,376. That's not because `千` appears less often in the corpus; it's because in LUW, `三千五百` is one unit and `千` doesn't get counted in isolation within it.

SUW also has entries like `二十` (20), `三十` (30), `五十` (50), `九百` (900) — compound numbers treated as single tokens. LUW would absorb these into even larger number units or count the full numeral string.

### 3. Compound nouns with very different standing

Some compound nouns behave unexpectedly across the two lists. Consider `弁護士` (lawyer) vs its components:

- `弁護士` — LUW rank: **2134** | SUW: **not in top 25k**
- `弁護` — LUW rank: **24,615** | SUW rank: **1,451**

`弁護` (defense, legal defense) is ranked 1,451 in SUW — surprisingly high — but sits near the bottom of LUW at 24,615. This is a direct consequence of the split: in SUW, `弁護士` is broken into components, so `弁護` gets counted every time `弁護士` appears in the corpus. In LUW, `弁護士` is treated as one unit, so the bare `弁護` component is rarely seen on its own.

Similar pattern with `国際` (international):
- LUW rank: **21,895** | SUW rank: **396**

In SUW, `国際` appears as a component of many compound nouns (`国際社会`, `国際的`, `国際連合`, etc.) and gets counted separately each time. In LUW those compounds are often treated as wholes, so the bare `国際` token is much rarer.

And `日本語` (Japanese language):
- LUW rank: **1,152** | Not in SUW top 25k

In SUW, `日本語` is presumably split into `日本` + `語`, so the compound word `日本語` itself doesn't appear as a unit in the frequency data. `日本` appears in both lists (LUW: 105, SUW: 73), but the full word `日本語` only shows up in LUW.

### 4. The verb する

This one surprises many people. The ubiquitous verb `する` (to do) appears differently:

- LUW has `する` at rank **14**
- SUW has `為る` at rank **8** (the UniDic lemma form of する)

In LUW, `する` appears as the surface form. In SUW, the underlying lemma `為る` is used. This is the same word written differently — it's a tokenization+lemmatization artifact, not a real vocabulary difference. But it means if you search for `する` in SUW, you won't find it under that spelling at the same rank.

---

## Overlap Between the Two Lists

Only about **60.9% of the 25,000 entries are shared** between LUW and SUW — roughly 15,200 words appear in both top-25k lists. Around 9,800 entries are unique to each.

Words unique to LUW tend to be:
- Compound verb+auxiliary forms (`ている`, `てくる`, `ていく`, etc.)
- Multi-word grammatical constructions (`という`, `について`, `のだ`, etc.)
- Compound nouns that get split in SUW (`弁護士`, `日本語`, etc.)

Words unique to SUW tend to be:
- Component morphemes of LUW compounds (`弁護`, `国際`, `語`)
- Numerals that inflate in frequency from compound numbers
- Auxiliary verbs counted in isolation (`仕舞う`, `於く`, etc.)

---

## Which List Should You Use?

**Use LUW if:**
- You're building vocabulary for reading or comprehension. LUW entries more closely match what you'd look up in a dictionary — you'd look up `ていく` as a grammar pattern, not split it.
- You want frequency data that aligns with how learners encounter Japanese. LUW rank 13 for `ている` correctly signals "you will see this constantly."
- You want compound expressions to have meaningful ranks rather than being dissolved.

**Use SUW if:**
- You're doing morphological analysis or NLP research. SUW is the default BCCWJ annotation unit and what most academic work references.
- You want to know how often each morpheme appears regardless of context. This matters for things like pitch accent lookup or phonological frequency.
- You're comparing to other NINJAL datasets (e.g., CEJC also uses SUW), so SUW gives you a more apples-to-apples comparison.

**Use both if you want to cross-validate:** a word that ranks highly in both lists is very robustly common. A word that ranks highly in LUW but is absent from SUW likely means it's a compound that SUW splits — worth investigating what it's made of.

---

## Quick Reference: Top 20 Comparison

| Rank | LUW | SUW |
|------|-----|-----|
| 1  | の  | の  |
| 2  | は  | に  |
| 3  | を  | て  |
| 4  | に  | は  |
| 5  | た  | だ  |
| 6  | が  | を  |
| 7  | だ  | た  |
| 8  | と  | 為る |
| 9  | て  | が  |
| 10 | で  | と  |
| 11 | も  | で  |
| 12 | ます | も  |
| 13 | ている | 居る |
| 14 | する | ます |
| 15 | 事  | 有る |
| 16 | れる | です |
| 17 | です | 言う |
| 18 | ない | 事  |
| 19 | 成る | ない |
| 20 | 有る | れる |

Notice: LUW rank 13 is `ている` — a compound that doesn't exist at all in the SUW list. SUW rank 8 is `為る` (する) — which in LUW appears as `する` at rank 14. The top few ranks are broadly similar (particles dominate both), but the divergence begins quickly.
