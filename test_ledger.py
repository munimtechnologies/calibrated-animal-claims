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
MD_PATH = os.path.join(HERE, "LEDGER.md")
VERDICTS = ("SURVIVES", "SURVIVES_IN_PART", "NOT_SUPPORTED", "UNDECIDED")
ROW_KEYS = ("id", "claim", "paper", "repo", "procedures", "calibrated",
            "calibrated_source", "verdict", "verdict_note")
PROC_KEYS = ("id", "procedure", "world", "worlds", "hits", "rate",
             "source_file", "source_key")
POWER_KEYS = ("planted", "worlds", "hits", "rate", "source_file", "source_key")
NOFA_KEYS = ("id", "claim", "paper", "repo", "calibrated", "calibrated_source",
             "verdict", "verdict_note")


def load():
    with open(PATH, encoding="utf-8") as f:
        return json.load(f)


class TestLedger(unittest.TestCase):
    def setUp(self):
        self.d = load()
        self.rows = self.d["claims"]
        self.procs = [p for r in self.rows for p in r["procedures"]]

    def test_version(self):
        self.assertEqual(self.d["version"], "calibrated-animal-claims-ledger-16")
        if os.path.exists(MD_PATH):
            with open(MD_PATH, encoding="utf-8") as f:
                self.assertIn("(version 16)", f.read())

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

    def test_stage1_calibration_rows(self):
        # Version 12: stage-1 calibration of the composite verdict (READING-STAGE1.md,
        # results/stage1/calibration.json, keys summary.W2/W3 ... fires_strong).
        row = [r for r in self.rows if r["id"] == "bengalese-mi-hierarchy"][0]
        procs = {p["id"]: p for p in row["procedures"]}
        w2 = procs["mi-composite-pooled-sim"]
        w3 = procs["mi-composite-bouts-sim"]
        self.assertEqual((w2["worlds"], w2["hits"]), (50, 46))
        self.assertEqual((w3["worlds"], w3["hits"]), (50, 50))
        for p in (w2, w3):
            self.assertEqual(p["source_file"], "results/stage1/calibration.json")
            self.assertTrue(p["source_key"].startswith("summary.W"))
            self.assertTrue(p["source_key"].endswith(".fires_strong"))
        self.assertIn("READING-STAGE1.md", row["calibrated_source"])
        for s in ("2 of 50 (detection 0.04)", "UNCALIBRATED_MULTI_TIMESCALE",
                  "Brier 0.212", "28 of 50 recursive worlds and 0 of 250"):
            self.assertIn(s, row["calibrated"])

    def test_stage8_rows(self):
        # Version 14: stage-8 calibration (READING-STAGE8.md, results/stage8/stage8.json).
        row = [r for r in self.rows if r["id"] == "bengalese-mi-hierarchy"][0]
        procs = {p["id"]: p for p in row["procedures"]}
        l1 = procs["mi-composite-heavytail-sim"]
        self.assertEqual((l1["worlds"], l1["hits"]), (50, 50))
        self.assertEqual(l1["source_file"], "results/stage8/stage8.json")
        self.assertEqual(l1["source_key"], "summary.L1_heavy_tailed_bouts.composite_strong_fires")
        self.assertIn("READING-STAGE8.md", row["calibrated_source"])
        for s in ("146 of 350 finite-state worlds", "39 of 250 recursive ones",
                  "5 of 350 finite-state", "133 of 250 recursive", "graded MIXED",
                  "3 of 50 (0.06, limit 0.05)", "Brier 0.2831"):
            self.assertIn(s, row["calibrated"])
        self.assertIn("Stage 8 graded MIXED", row["verdict_note"])
        pending = " ".join(self.d["pending"])
        self.assertNotIn("stage 8", pending)
        if os.path.exists(MD_PATH):
            with open(MD_PATH, encoding="utf-8") as f:
                md = f.read()
            self.assertIn("21 of 27 procedures", md)
            self.assertIn("results/stage8/stage8.json", md)

    def test_stage6_row(self):
        # Version 15: stage-6 human-speech positive control (READING-STAGE6.md,
        # results/stage6/grade6.json headline SPLIT_OR_UNRESOLVED). A detection test, not a
        # false-alarm procedure, so it added no procedure (26 then; 27 since version 16).
        row = [r for r in self.rows if r["id"] == "bengalese-mi-hierarchy"][0]
        self.assertIn("READING-STAGE6.md", row["calibrated_source"])
        for s in ("0 of 4 read-English analyses", "193,644 / 189,327 phones",
                  "0 of 400", "SPLIT_OR_UNRESOLVED", "Brier 0.3653", "20.3%"):
            self.assertIn(s, row["calibrated"])
        self.assertIn("Howard-Spink", row["verdict_note"])
        self.assertNotIn("and speech stages", row["verdict_note"])
        self.assertEqual(len(row["procedures"]), 5)
        self.assertTrue(any("Howard-Spink" in p for p in self.d["prior_art"]))
        pending = " ".join(self.d["pending"])
        self.assertNotIn("speech)", pending)
        self.assertIn("stages 6B and 8B", pending)
        if os.path.exists(MD_PATH):
            with open(MD_PATH, encoding="utf-8") as f:
                md = f.read()
            self.assertIn("READING-STAGE6.md", md)
            self.assertIn("Howard-Spink", md)

    def test_finch_links_row(self):
        # Version 16: finch repeat-number links (finch-repeat-links-test READING-REPEAT-LINKS.md,
        # results/repeat_links_results.json, grade UNCALIBRATED_LINKS_SURVIVE_LOCAL_STATE).
        row = [r for r in self.rows if r["id"] == "finch-repeat-links"][0]
        self.assertEqual(row["verdict"], "UNDECIDED")
        self.assertEqual(row["repo"], "https://github.com/munimtechnologies/finch-repeat-links-test")
        self.assertEqual(row["calibrated_source"], "READING-REPEAT-LINKS.md")
        p = row["procedures"][0]
        self.assertEqual((p["worlds"], p["hits"]), (48, 42))
        self.assertEqual(p["source_file"], "results/repeat_links_results.json")
        self.assertTrue(p["source_key"].startswith("calibration.CD.any_LP"))
        for s in ("92 of 110", "43 of 55", "13 of 48", "0.271", "Brier 0.1668"):
            self.assertIn(s, row["calibrated"])
        self.assertIn("UNCALIBRATED_LINKS_SURVIVE_LOCAL_STATE", row["verdict_note"])
        self.assertEqual(len(self.procs), 27)
        pending = " ".join(self.d["pending"])
        self.assertNotIn("finch-repeat-links-test", pending)
        if os.path.exists(MD_PATH):
            with open(MD_PATH, encoding="utf-8") as f:
                md = f.read()
            self.assertIn("READING-REPEAT-LINKS.md", md)
            self.assertIn("| 48 | 42 | 0.875 |", md)

    def test_parrot_row(self):
        # Version 11: parrot AMENDMENT-2 robustness checks graded (READING-ROBUST.md).
        row = [r for r in self.rows if r["id"] == "parrot-duet-syntax"][0]
        self.assertEqual(row["verdict"], "SURVIVES")
        self.assertIn("READING-ROBUST.md", row["calibrated_source"])
        for s in ("2.2416 against 1.9960", "2.6387 against 2.1943",
                  "2.5450 against 2.2956", "152 of 468", "Brier 0.109"):
            self.assertIn(s, row["calibrated"])
        self.assertNotIn("queued", row["verdict_note"])
        pending = " ".join(self.d["pending"])
        self.assertNotIn("parrot", pending)
        self.assertIn("stage 7 (European starling)", pending)

    def test_graded_without_false_alarm_rate(self):
        rows = self.d["graded_without_false_alarm_rate"]
        ids = [r["id"] for r in rows]
        self.assertEqual(len(ids), len(set(ids)))
        claim_ids = {r["id"] for r in self.rows}
        for r in rows:
            for k in NOFA_KEYS:
                self.assertIn(k, r, r.get("id"))
            self.assertIn(r["verdict"], VERDICTS)
            self.assertNotIn(r["id"], claim_ids)
            self.assertTrue(r["repo"].startswith("https://github.com/munimtechnologies/"))

    def test_tempo_row(self):
        # Version 12: delta-band tempo test graded (animal-tempo-window-test READING-TEMPO.md).
        row = [r for r in self.d["graded_without_false_alarm_rate"]
               if r["id"] == "animal-delta-tempo"][0]
        self.assertEqual(row["verdict"], "SURVIVES")
        self.assertEqual(row["calibrated_source"], "READING-TEMPO.md")
        for s in ("0.5500 (22 of 40) against 0.3899", "p_upper 0.0118", "W 73.4 s",
                  "p 0.1617", "Brier 0.2767", "3.3517 Hz"):
            self.assertIn(s, row["calibrated"])
        self.assertIn("PREFERRED_TEMPO_BEYOND_WINDOW", row["verdict_note"])
        pending = " ".join(self.d["pending"])
        self.assertNotIn("animal-tempo-window-test", pending)
        self.assertIn("stage 7 (European starling)", pending)
        self.assertNotIn("stages 1,", pending)

    def test_delta_rhythm_row(self):
        # Version 13: delta-rhythm-window-test graded (READING-RHYTHM.md, job delta-rhythm-v1).
        row = [r for r in self.rows if r["id"] == "delta-rhythm-optimum"][0]
        self.assertEqual(row["verdict"], "SURVIVES")
        self.assertEqual(row["calibrated_source"], "READING-RHYTHM.md")
        self.assertEqual(row["repo"], "https://github.com/munimtechnologies/delta-rhythm-window-test")
        procs = {p["id"]: p for p in row["procedures"]}
        p = procs["rhythm-ou-aic-window"]
        self.assertEqual((p["worlds"], p["hits"]), (400, 146))
        self.assertEqual(p["source_file"], "results/rhythm/results.json")
        self.assertIn("share_BBM_null_sims_OU_beats_BM_by_AIC", p["source_key"])
        for s in ("28.6538 against 28.4107", "6.9320", "2.8186", "p 0.0025", "power 0.995",
                  "3.123 Hz", "0.0910 tree heights", "p 0.0050", "Brier 0.1486"):
            self.assertIn(s, row["calibrated"])
        self.assertIn("OPTIMUM_SURVIVES_WINDOW", row["verdict_note"])
        pending = " ".join(self.d["pending"])
        self.assertNotIn("delta-rhythm-window-test", pending)
        self.assertNotIn("Piette", pending)


if __name__ == "__main__":
    unittest.main()
