"""Ingest daily OHLCV data into SQLite and export daily returns."""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path

import pandas as pd

COLUMNS = ["date", "symbol", "open", "high", "low", "close", "volume"]


def fetch_yahoo(symbols: list[str], start: str, end: str) -> pd.DataFrame:
    """Optional live data source. Internet access and yfinance required."""
    try:
        import yfinance as yf
    except ImportError as exc:
        raise RuntimeError("Install optional data provider: pip install yfinance") from exc

    frames = []
    for symbol in symbols:
        history = yf.Ticker(symbol).history(start=start, end=end, auto_adjust=True)
        if history.empty:
            raise ValueError(f"No price history returned for {symbol}")
        frame = history.reset_index()
        frame.columns = [str(col).lower() for col in frame.columns]
        frame["symbol"] = symbol
        frames.append(frame[COLUMNS])
    return pd.concat(frames, ignore_index=True)


def clean_prices(raw: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Drop invalid rows, deduplicate by (symbol, date), and report counts."""
    df = raw.copy()
    df.columns = [str(col).strip().lower() for col in df.columns]
    missing = set(COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing CSV columns: {', '.join(sorted(missing))}")

    before = len(df)
    df["symbol"] = df["symbol"].astype("string").str.strip().str.upper()
    df["date"] = pd.to_datetime(df["date"], utc=True, errors="coerce").dt.strftime("%Y-%m-%d")
    for column in ["open", "high", "low", "close", "volume"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    valid = (
        df[COLUMNS].notna().all(axis=1)
        & df["symbol"].str.fullmatch(r"[A-Z0-9.^_-]+").fillna(False)
        & (df[["open", "high", "low", "close"]] > 0).all(axis=1)
        & (df["volume"] >= 0)
        & (df["high"] >= df[["open", "close", "low"]].max(axis=1))
        & (df["low"] <= df[["open", "close", "high"]].min(axis=1))
    )
    df = df.loc[valid, COLUMNS]
    invalid = before - len(df)
    duplicates = int(df.duplicated(["symbol", "date"], keep="last").sum())
    df = df.drop_duplicates(["symbol", "date"], keep="last").sort_values(
        ["symbol", "date"]
    ).reset_index(drop=True)
    if df.empty:
        raise ValueError("No usable rows after validation")
    return df, {
        "input_rows": before,
        "invalid_rows": invalid,
        "duplicate_rows": duplicates,
        "valid_rows": len(df),
        "symbols": sorted(df["symbol"].unique().tolist()),
    }


def save_prices(prices: pd.DataFrame, database: Path) -> None:
    """Idempotent insert/update of daily prices."""
    with sqlite3.connect(database) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS daily_prices (
                symbol TEXT NOT NULL,
                date TEXT NOT NULL,
                open REAL NOT NULL,
                high REAL NOT NULL,
                low REAL NOT NULL,
                close REAL NOT NULL,
                volume INTEGER NOT NULL,
                PRIMARY KEY (symbol, date)
            )
        """)
        values = [
            (r.symbol, r.date, float(r.open), float(r.high), float(r.low),
             float(r.close), int(r.volume))
            for r in prices.itertuples(index=False)
        ]
        conn.executemany("""
            INSERT INTO daily_prices
              (symbol, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(symbol, date) DO UPDATE SET
              open=excluded.open, high=excluded.high, low=excluded.low,
              close=excluded.close, volume=excluded.volume
        """, values)


def export_returns(database: Path, directory: Path) -> pd.DataFrame:
    """Recalculate returns from the full stored series, avoiding stale values."""
    with sqlite3.connect(database) as conn:
        prices = pd.read_sql_query(
            "SELECT symbol, date, close FROM daily_prices ORDER BY symbol, date",
            conn
        )
    prices["daily_return"] = prices.groupby("symbol")["close"].pct_change(
        fill_method=None
    )
    prices.to_csv(directory / "daily_returns.csv", index=False, na_rep="")
    return prices


def run(raw: pd.DataFrame, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    clean, report = clean_prices(raw)
    clean.to_csv(output_dir / "clean_prices.csv", index=False)
    database = output_dir / "market_data.sqlite"
    save_prices(clean, database)
    returns = export_returns(database, output_dir)
    report["stored_rows"] = len(returns)
    (output_dir / "quality_report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sources = parser.add_mutually_exclusive_group()
    sources.add_argument("--csv", type=Path, help="CSV with date,symbol,OHLCV")
    sources.add_argument("--yahoo", nargs="+", metavar="TICKER", help="Fetch Yahoo prices")
    parser.add_argument("--start", default="2024-01-01")
    parser.add_argument("--end", default="2025-01-01", help="Exclusive end date")
    parser.add_argument("--output", type=Path, default=Path("output"))
    args = parser.parse_args()

    if args.yahoo:
        raw = fetch_yahoo(args.yahoo, args.start, args.end)
    elif args.csv:
        raw = pd.read_csv(args.csv)
    else:
        raise SystemExit("Provide --csv PATH or --yahoo TICKER [TICKER...]")

    report = run(raw, args.output)
    print(json.dumps(report, indent=2))
    print(f"Created database and CSV reports in {args.output}")


if __name__ == "__main__":
    main()
