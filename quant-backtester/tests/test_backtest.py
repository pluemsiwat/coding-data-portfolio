"""Tests for a moving-average backtest, including no look-ahead behavior."""
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backtest import demo_prices, prepare_prices, run, simulate


class BacktestTests(unittest.TestCase):
    def test_signal_is_used_only_next_day(self):
        raw = pd.DataFrame({
            "date": pd.date_range("2024-01-01", periods=7),
            "close": [10, 10, 10, 12, 14, 13, 11],
        })
        prices = prepare_prices(raw)
        results, _ = simulate(prices, fast=2, slow=3, cost_bps=0)
        self.assertEqual(results["position"].iloc[3], results["signal"].iloc[2])
        self.assertEqual(results["position"].iloc[4], results["signal"].iloc[3])
        self.assertEqual(results["position"].iloc[0], 0)

    def test_cost_reduces_results(self):
        prices = prepare_prices(demo_prices(100))
        no_cost, _ = simulate(prices, fast=5, slow=20, cost_bps=0)
        with_cost, metrics = simulate(prices, fast=5, slow=20, cost_bps=15)
        self.assertLessEqual(with_cost["strategy_equity"].iloc[-1],
                             no_cost["strategy_equity"].iloc[-1])
        self.assertGreater(metrics["number_of_position_changes"], 0)

    def test_select_symbol(self):
        raw = pd.concat([demo_prices(50), demo_prices(50).assign(symbol="OTHER")])
        with self.assertRaises(ValueError):
            prepare_prices(raw)
        self.assertEqual(len(prepare_prices(raw, "OTHER")), 50)

    def test_outputs_written(self):
        with tempfile.TemporaryDirectory() as temp:
            metrics = run(demo_prices(100), Path(temp), fast=5, slow=20)
            self.assertIn("max_drawdown_pct", metrics["strategy"])
            self.assertTrue((Path(temp) / "equity_curve.csv").exists())
            self.assertTrue((Path(temp) / "equity_curve.png").exists())
            self.assertTrue((Path(temp) / "metrics.json").exists())

    def test_invalid_params(self):
        prices = prepare_prices(demo_prices(60))
        with self.assertRaises(ValueError):
            simulate(prices, fast=20, slow=10)
        with self.assertRaises(ValueError):
            simulate(prices, fast=2, slow=30, cost_bps=-1)


if __name__ == "__main__":
    unittest.main()
