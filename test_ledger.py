# Copyright 2026 MV2, Munim, Inc. Licensed under the Apache License, Version 2.0 (Apache-2.0).
# Made with AI agents working in MV2's name.
"""Consistency checks for results/ledger.json (stdlib only).

Checks that every claim row is complete, every false-alarm rate equals hits / worlds,
every verdict is one of four labels, and the summary counts match the rows.
Rows of kind "negative" (a published claim that an effect is ABSENT) carry a power block
instead of false-alarm procedures; its rate must equal hits / worlds too.
Run: python -m unittest -v test_ledger
"""
import json
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "results", "ledger.json")
VERDICTS = ("SURVIVES", "SURVIVES_IN_PART", "NOT_SUPPORTED", "UNDECIDED")
ROW_KEYS = ("id", "claim", "paper", "repo", "procedures", "calibrated",
            "calibrated_source", "verdict", "verdict_note")
PROC_KEYS = ("id", "procedure", "world", "worlds", "hits", "rate",
             "source_file", "source_key")
POWER_KEYS = ("planted", "worlds", "hits", "rate", "source_file", "source_key")


def load():
    with open(PATH, encoding="utf-8") as f:
        return json.load(f)


class TestLedger(unittest.TestCase):
    def setUp(self):
        self.d = load()
        self.rows = self.d["claims"]
        self.procs = [p for r in self.rows for p in r["procedures"]]

    def test_rows_complete(self):
        ids = [r["id"] for r in self.rows]
        self.assertEqual(len(ids), len(set(ids)))
        for r in self.rows:
            for k in ROW_KEYS:
                self.assertIn(k, r, r.get("id"))
            self.assertIn(r["verdict"], VERDICTS)
            self.assertTrue(r["repo"].startswith("https://github.com/munimtechnologies/"))
            if r.get("kind") == "negative":
                self.assertIn("power", r, r["id"])
            else:
                self.assertGreaterEqual(len(r["procedures"]), 1)

    def test_rates_match_counts(self):
        pids = [p["id"] for p in self.procs]
        self.assertEqual(len(pids), len(set(pids)))
        for p in self.procs:
            for k in PROC_KEYS:
                self.assertIn(k, p, p.get("id"))
            self.assertGreater(p["worlds"], 0)
            self.assertGreaterEqual(p["hits"], 0)
            self.assertLessEqual(p["hits"], p["worlds"])
            self.assertAlmostEqual(p["rate"], p["hits"] / p["worlds"], places=9)
            self.assertTrue(p["source_file"])

    def test_power_blocks(self):
        for r in self.rows:
            if r.get("kind") != "negative":
                continue
            pw = r["power"]
            for k in POWER_KEYS:
                self.assertIn(k, pw, r["id"])
            self.assertGreater(pw["worlds"], 0)
            self.assertLessEqual(pw["hits"], pw["worlds"])
            self.assertAlmostEqual(pw["rate"], pw["hits"] / pw["worlds"], places=9)

    def test_summary(self):
        s = self.d["summary"]
        self.assertEqual(s["claims"], len(self.rows))
        self.assertEqual(s["procedures"], len(self.procs))
        self.assertEqual(s["fired_at_least_0.30"],
                         sum(1 for p in self.procs if p["rate"] >= 0.30))
        self.assertEqual(s["calibrated_at_most_0.10"],
                         sum(1 for p in self.procs if p["rate"] <= 0.10))
        self.assertEqual(s["negative_claims"],
                         sum(1 for r in self.rows if r.get("kind") == "negative"))
        for v in VERDICTS:
            self.assertEqual(s["verdicts"][v],
                             sum(1 for r in self.rows if r["verdict"] == v))
        self.assertEqual(sum(s["verdicts"].values()), len(self.rows))

    def test_exact_clan_row(self):
        # Version 9: the clan Mantel row is an exact enumeration over all 7! relabelings.
        row = [r for r in self.rows if r["id"] == "whale-clan-marking"][0]
        for p in row["procedures"]:
            self.assertEqual(p["worlds"], 5040)

    def test_bengalese_row(self):
        # Version 10: Bengalese finch MI-decay row (birdsong-mi-decay-test stage 4).
        row = [r for r in self.rows if r["id"] == "bengalese-mi-hierarchy"][0]
        self.assertEqual(row["verdict"], "NOT_SUPPORTED")
        procs = {p["id"]: p for p in row["procedures"]}
        self.assertEqual((procs["bf-composite-kgram"]["worlds"],
                          procs["bf-composite-kgram"]["hits"]), (100, 100))
        self.assertEqual((procs["bf-composite-phrase"]["worlds"],
                          procs["bf-composite-phrase"]["hits"]), (12, 11))
        self.assertEqual(self.d["version"], "calibrated-animal-claims-ledger-10")


if __name__ == "__main__":
    unittest.main()
