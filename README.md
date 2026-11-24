# calibrated-animal-claims

A running ledger of MV2's pre-registered, calibrated re-tests of headline animal-communication claims: how often each published-style test reports an effect in worlds with no effect, and whether the effect survives a test that is calibrated. Claims that an effect is absent are tested for power instead.

- [LEDGER.md](LEDGER.md): the tables and a short reading.
- [results/ledger.json](results/ledger.json): every number with the repository, file and key it was copied from.
- [test_ledger.py](test_ledger.py): stdlib consistency checks (`python -m unittest -v test_ledger`).

Headline as of 2026-11-24: 8 of 10 published-style procedures reported an effect in at least 30% of worlds with none. Yet of the 7 claims a calibrated test could decide, 6 held in full or in part (orangutan rhythm, fruit bat addressee, mangabey call order, sperm whale tempo types, Eastern chimpanzee drum alternation, and the absence of a clan signature in spotted hyena whoops). Chimpanzee "additive" call pairs did not hold, and 3 claims remain undecided.

Each underlying test has its own repository with its pre-registration, code, results and grader, all linked from the ledger. The claims were chosen because we suspected their tests, so the rates are not an estimate for the field.

Made with AI agents working in MV2's name; no human expert has checked this yet. MV2, Munim, Inc., mv2@munimtech.com.

License: code Apache-2.0; text and data CC BY 4.0.
