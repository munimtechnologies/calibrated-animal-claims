# Ledger: calibrated re-tests of headline animal-communication claims

MV2, Munim, Inc. (mv2@munimtech.com). Compiled on 2026-11-22, updated 2026-11-25, with AI agents working in MV2's name; not yet checked by a human expert. Text and data CC BY 4.0. The machine-readable version, with the exact source file and key of every number, is [results/ledger.json](results/ledger.json); `python -m unittest -v test_ledger` checks it.

**What this is.** Each row is a published claim that one of MV2's open projects re-tested with a pre-registered, calibrated test on the authors' own public data. "Published-style procedure" is the published test, or our closest reconstruction of it. "False-alarm rate" is how often that procedure reported the effect in worlds built from the real data with the effect removed but the suspected structure (bouts, days, callers, social groups, recording sessions, rhythm mixtures, unequal button use, pair repertoires) kept. Claims that an effect is **absent** are listed separately, with the power of the calibrated test.

**Selection warning.** We picked these claims because we suspected their tests. The rates say nothing about the field as a whole, and each world embodies one specific confound.

## Published-style procedures in worlds with no effect

| claim | procedure | worlds with no effect | reported an effect | rate | source |
|---|---|---|---|---|---|
| Chimpanzee drumming (Eleuteri et al. 2025) | Welch t, bouts as units | 200 | 192 | 0.960 | chimp-drum-test: results/drum/drum_results.json |
| Orangutan rhythm (Lameira et al. 2024) | uniform-null isochrony declaration | 1,999 | 1,999 | 1.000 | orangutan-rhythm-test: results/rhythm_results.json |
| Sperm whale vowel length (Begus et al.) | a vs i within whale, codas as units | 200 | 71 | 0.355 | whale-vowel-test: RESULTS-DUR.md |
| Sperm whale coarticulation (Begus et al.) | first-click mismatch, codas as units | 200 | 152 | 0.760 | whale-vowel-test: results/coart/vowel3_results.json |
| Fruit bat addressee (Prat et al. 2016) | classifier, free label shuffle | 4 | 4 | 1.000 | bat-addressee-test: results/bat/bat_results.json |
| Elephant names (Pardo et al. 2024) | receiver shuffle across dates | 20 | 20 | 1.000 | elephant-names-test: results/elephant/elephant_results.json |
| Chimpanzee additive pairs (Girard-Buttoz et al. 2025) | closest-single-calls criterion | 1,600 | 1,132 | 0.7075 | chimp-bigram-test: results/chimp/chimp_results.json |
| Mangabey call order (Le Floch et al. 2026) | caller-blind pooled test (our stand-in) | 2,000 | 105 | 0.0525 | mangabey-order-test: results/mangabey_results.json |
| Sperm whale tempo types (Sharma et al. 2024) | five pooled duration peaks | 999 | 0 | 0.000 | coda-tempo-test: results/tempo/tempo_results.json |
| Sperm whale tempo types (Sharma et al. 2024) | count of rhythm-tempo combinations | 999 | 999 | 1.000 | coda-tempo-test: results/tempo/tempo_results.json |
| Magpie second-order sequences (Mason et al. 2026, preprint) | order 2 vs order 1 by AIC on pooled types (our stand-in) | 999 | 999 | 1.000 | magpie-order-test: results/order/order_results.json |
| Soundboard dog button networks (Bastos et al. 2024) | Randomness Index at least 0.2 below Erdos-Renyi (authors' per-dog criterion) | 139 (one popularity-only network per dog) | 127 | 0.914 | dog-button-test: results/per_dog.csv |
| Parrot duet syntax (Dahlin et al. 2026) | pooled permutation test of adjacent calls (our stand-in) | 200 | 200 | 1.000 | parrot-duet-syntax-test: results/syntax/syntax_results.json |
| Marmoset second-order sequences (Bosshard et al. 2024) | order 2 beats order 1 in leave-one-sequence-out cross-validation at every smoothing constant (authors' reading) | 499 | 0 | 0.000 | marmoset-order-test: results/marmoset_results.json |

11 of 14 procedures reported an effect in at least 30% of worlds that had none; 3 stayed at or below 10%.

## Negative claims: calibrated test and its power

| claim | calibrated test (registered) | planted effect found | verdict |
|---|---|---|---|
| Hyena whoops carry no clan signature (Lehmann et al. 2022) | leave-one-hyena-out clan accuracy 0.2403 against a relabeling null of 0.2207, p 0.34; handheld only p 0.1767; the authors' scheme reproduced, excess p 0.09 | 40 of 40 worlds with a clan offset half the size of individual differences (hyena-clan-signature-test: results/hyena_results.json) | SURVIVES |

The paper reported this negative without a significance test or power analysis. It holds: no clan signal under a calibrated test that would have found a whole-whoop clan offset even a quarter the size of individual differences (40 of 40 worlds at every planted size).

## Calibrated tests and verdicts

| claim | calibrated test (registered) | verdict |
|---|---|---|
| Chimpanzee drumming | Eastern alternation beyond each bout's own gaps p 0.0001; subspecies difference with 11 communities as units p 0.103 (power 0.275) | SURVIVES_IN_PART |
| Orangutan rhythm | full pulses beyond within-train shuffles p 0.0005, beyond local shuffles p 0.0010 | SURVIVES |
| Sperm whale vowel length | within-bout D +0.1136 s, p 0.0001, but the test's own size was 0.190 | UNDECIDED |
| Sperm whale coarticulation | first and last clicks both mismatch; asymmetry test size 0.205 | UNDECIDED |
| Fruit bat addressee | shuffles within each bat's day: 0.526 against 0.447, p 0.005 | SURVIVES |
| Elephant names | shuffles within caller, date and relationship: p 0.383, power 0.05 | UNDECIDED |
| Chimpanzee additive pairs | per-utterance conjunction test: mixture rejected for 0 of 8 pairs (3 powered) | NOT_SUPPORTED |
| Mangabey call order | exact test within 15 females: p 0.0002, size 0.021 | SURVIVES |
| Sperm whale tempo types | 0 of 999 tempo-free surrogates show all five peaks; 1+1+3 multimodal p 0.001 | SURVIVES |
| Hyena: no clan signature (negative) | relabeling null p 0.34, power 1.0 at half the individual spread | SURVIVES |
| Magpie second-order sequences | cross-validated group-aware gain of order 2: 0.0000 nats, p 1.0 against group first-order worlds; power 0.935 (type level only) | NOT_SUPPORTED |
| Soundboard dog button networks | popularity-only null over 133 dogs: real RI -0.564, popularity -0.766, Erdos-Renyi -0.209; popularity explains 1.566 of the gap; p 1.0 | NOT_SUPPORTED |
| Parrot duet syntax | order within duet and sex: 2.2416 bits against 1.8916, p 0.0001 (size 0.030); co-occurrence beyond each pair's repertoire p 0.0001 (size 0.045) | SURVIVES |
| Marmoset second-order sequences | held-out gain of order 2: 303.20 nats (297.35 holding out whole sessions); largest in 499 session first-order worlds 22.62, with looped chunks 52.40; p 0.0020 each; power 1.0 | SURVIVES |

Verdicts: 7 SURVIVES, 1 SURVIVES_IN_PART, 3 NOT_SUPPORTED, 3 UNDECIDED.

## Reading

Unsafe tests were the rule in this set, but most of the effects they reported were real anyway. Of the eleven claims a calibrated test could decide, eight held in full or in part, including the one negative claim (hyena clans). Three failed. The chimpanzee additive pairs failed because their criterion cannot tell "A and B at once" from "sometimes A, sometimes B". The magpie second-order claim failed at the level of sequence types: an in-sample order test prefers order 2 in every world built from each group's first-order chain, and in the real data the call two back adds nothing once each group's own transitions are known (the preprint's token-level data are not public, and its own procedures are re-built in a queued amendment). The marmoset second-order claim, which the magpie preprint names as its benchmark, is the mirror image: its cross-validated test never fired in 1,996 worlds without second-order rules, and the real order-2 gain is about six times the largest gain in any of them. Whether part of that gain is a positional template rather than a dependency on the call two back is registered as the next test. The soundboard dogs' network evidence failed because the comparison graphs give every button the same chance of use: when each dog's own pairings are re-drawn keeping only how often each concept is used, the index comes out even more negative than in the real networks (the paper's other analyses of the dogs are not tested). The parrot duets show a third case: the effect is real but the published evidence is not. Calibrated tests find call order inside the duets. The paper's "syntactic rules", however, are reproduced as correlations of call-type counts across ten equal slices of the data file, and most of them vanish when whole duets are put in random order. Three claims stay undecided: two because our own registered test failed its calibration, one because the public data are too thin.

## Prior art

Pooling and pseudoreplication in animal-communication statistics are well documented: Mundry and Sommer 2007 (Animal Behaviour, doi:10.1016/j.anbehav.2006.12.028), Waller et al. 2013 (Animal Behaviour, doi:10.1016/j.anbehav.2013.05.038), Whitehouse et al. 2023 (International Journal of Primatology, doi:10.1007/s10764-023-00399-y), Jadoul et al. 2025 on the uniform null behind integer-ratio rhythm analyses (Annals of the New York Academy of Sciences, doi:10.1111/nyas.70037), and for one headline claim, Wartel et al. 2026 on bonobo compositionality (PeerJ, doi:10.7717/peerj.21651). That clustering falling with degree can come from degree structure rather than hierarchy is Soffer and Vazquez 2005 (Physical Review E 71:057101). A defined order of sex-specific notes in yellow-naped amazon duets was described by Wright and Dahlin 2007 (Behaviour 144:207-228, doi:10.1163/156853907779947346). What this ledger adds is a measured false-alarm rate, claim by claim, for recent headline results, next to a calibrated verdict on the effect itself.

## Pending

dolphin-coercion-test, whale-clan-marking-test, molerat-dialect-test, magpie-dialect-test, amendment 1 of magpie-order-test, amendment 1 of marmoset-order-test (position), amendment 2 of parrot-duet-syntax-test (robustness checks), and the tests of chimpanzee raspberry conventions, the zebra finch semantic magnet, shared human-animal taste in sounds and the 'universal' delta rhythm of animal calls are pre-registered and waiting for compute. Each will be added when graded.
