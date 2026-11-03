# Financial Data Pipeline

A Python + SQLite pipeline for ingesting, validating, and querying daily stock price data.

**What it demonstrates:** loading market data, quality checks, duplicate handling, database upserts, and daily return calculations.

## Quick demo (offline)

1. Install Python 3.10+ and dependencies: `pip install -r financial-data-pipeline/requirements.txt`
2. Generate **fictional** market data: `python financial-data-pipeline/make_sample.py`
3. Run the importer: `python financial-data-pipeline/pipeline.py --csv data/sample_prices.csv --output output/market-data`

Run these commands from the repository root. The example generator writes `data/sample_prices.csv` relative to your current working directory.

## Historical prices from Yahoo (optional, internet required)

Install the optional dependency: `pip install yfinance`

`python financial-data-pipeline/pipeline.py --yahoo AAPL MSFT --start 2023-01-01 --end 2025-01-01 --output output/market-data`

The end date is exclusive. Yahoo availability and historical adjustments depend on the data provider. This is for research practice, not live trading.

## Outputs

- `clean_prices.csv`: validated and deduplicated OHLCV records
- `market_data.sqlite`: prices with unique (symbol, date) keys
- `daily_returns.csv`: close-to-close percentage returns per ticker, recalculated from the full database
- `quality_report.json`: rejected-row and duplicate counts

## Tests

`python -m unittest discover -s financial-data-pipeline/tests -v`

## Limitations

Synthetic demonstration data are not real market observations. The pipeline drops invalid records and reports counts rather than repairing them. It does not account for exchange holidays, every provider-specific field, corporate-action revisions, or real-time streaming.

Created as an AI-assisted learning project; review, run and adapt it before describing it as independent work.
