# Quantitative Engineering Projects

Two learning projects exploring financial data engineering and simple quantitative research.

## Projects

| Project | Tools | What it does |
| --- | --- | --- |
| [Financial Data Pipeline](financial-data-pipeline/) | Python, pandas, SQLite | Cleans daily OHLCV data, stores prices in a database, and calculates returns. |
| [Moving-Average Backtester](quant-backtester/) | Python, pandas, Matplotlib | Simulates a basic trend strategy, includes estimated transaction costs, and compares returns with buy-and-hold. |

## Getting started

Each project folder includes a README with setup instructions, example commands, limitations, and tests.

- Both projects work with **synthetic demonstration data** without an external API key.
- The data pipeline can optionally fetch historical Yahoo Finance data when an internet connection is available.
- The backtester is an educational research exercise. It is not a live trading system.

## Testing

Install both projects' dependencies and run:

```bash
python -m unittest discover -s financial-data-pipeline/tests -v
python -m unittest discover -s quant-backtester/tests -v
```

## Scope and attribution

These are AI-assisted starter implementations using sample data, intended for learning, review, and further development. The results are not investment advice or evidence of independent historical research. Anyone presenting the projects should accurately describe what they personally tested, changed, and learned.
