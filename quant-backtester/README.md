# Moving-Average Strategy Backtester

A simple, transparent backtesting project comparing a **moving-average signal** with a buy-and-hold benchmark.

## Quick start

From the repository root, install Python 3.10+ and dependencies:

`pip install -r quant-backtester/requirements.txt`

Generate a reproducible **synthetic** price series and run the backtest:

`python quant-backtester/backtest.py --demo --fast 10 --slow 30 --cost-bps 5 --output output/backtest`

Run on a historical CSV instead:

`python quant-backtester/backtest.py --csv prices.csv --symbol AAPL --output output/backtest`

The CSV needs `date` and `close` fields, and may include `symbol`. If your CSV contains multiple symbols, supply `--symbol`. Adjusted closing prices are preferable for real historical comparisons.

## What is tested?

- 10-day vs. 30-day simple moving averages (configurable)
- A **long or cash** position; no short selling or leverage
- Signals shifted by one bar to reduce look-ahead bias
- Transaction fee per entry/exit (`cost-bps`, default 5 basis points)
- Comparison with a buy-and-hold benchmark
- Annualized return, volatility, maximum drawdown, and a simplified Sharpe ratio

## Outputs

- `equity_curve.csv`: daily signals, positions, fees, and equity values
- `equity_curve.png`: strategy vs. buy-and-hold comparison chart
- `metrics.json`: summary of historical results

## Tests

`python -m unittest discover -s quant-backtester/tests -v`

## Research limitations

This is a **learning backtest, not a trading recommendation**. The example prices are fictional. Signal execution uses a simplified next-bar, close-to-close return model and does **not** model opening-price gaps, bid-ask spread, slippage, financing, taxes, stock splits, dividend handling, market impact, exchange trading calendars, or survivorship bias. The risk-free rate is set to zero for the simplified Sharpe calculation. Historical performance cannot predict future returns.

Created as an AI-assisted starter project. Read the code and improve it before presenting it as independently completed research.
