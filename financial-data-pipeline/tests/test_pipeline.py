"""Unit tests for ingestion validation, deduplication, returns and database."""
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pipeline import clean_prices, run
from make_sample import make_sample


class PipelineTests(unittest.TestCase):
    def test_clean_duplicates_and_invalid_rows(self):
        raw = pd.DataFrame([
            ["2024-01-02", "aaa", 10, 11, 9, 10, 100],
            ["2024-01-02", "aaa", 10, 12, 9, 11, 150],
            ["2024-01-03", "aaa", 10, 8, 9, 10, 100],
        ], columns=["date", "symbol", "open", "high", "low", "close", "volume"])
        cleaned, report = clean_prices(raw)
        self.assertEqual(report["duplicate_rows"], 1)
        self.assertEqual(report["invalid_rows"], 1)
        self.assertEqual(report["valid_rows"], 1)
        self.assertEqual(cleaned.iloc[0]["close"], 11)

    def test_repeat_run_is_idempotent(self):
        raw = pd.DataFrame([
            ["2024-01-02", "AAA", 10, 11, 9, 10, 100],
            ["2024-01-03", "AAA", 11, 12, 10, 11, 120],
            ["2024-01-02", "BBB", 20, 22, 19, 20, 100],
        ], columns=["date", "symbol", "open", "high", "low", "close", "volume"])
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)
            run(raw, out)
            run(raw, out)
            with sqlite3.connect(out / "market_data.sqlite") as conn:
                count = conn.execute("SELECT COUNT(*) FROM daily_prices").fetchone()[0]
            self.assertEqual(count, 3)
            returns = pd.read_csv(out / "daily_returns.csv")
            second = returns.query("symbol == 'AAA'").iloc[1]["daily_return"]
            self.assertAlmostEqual(second, 0.1)

    def test_sample_generator(self):
        with tempfile.TemporaryDirectory() as temp:
            path = make_sample(Path(temp) / "sample.csv", days=30)
            sample = pd.read_csv(path)
            self.assertEqual(len(sample), 60)
            clean, report = clean_prices(sample)
            self.assertEqual(report["invalid_rows"], 0)
            self.assertEqual(len(clean), 60)


if __name__ == "__main__":
    unittest.main()
