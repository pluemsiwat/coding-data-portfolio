"""Research-only moving-average backtest with next-bar signals and costs."""
from __future__ import annotations

import argparse
import json
import math
from datetime import date, timedelta
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

TRADING_DAYS = 252


def demo_prices(days: int = 280) -> pd.DataFrame:
    """Create synthetic prices with a trend and cycles (not real market data)."""
    rows = []
    d = date(2024, 1, 1)
    i = 0
    while i < days:
        if d.weekday() < 5:
            close = 100 * math.exp(0.00055 * i + 0.065 * math.sin(i / 16))
            rows.append({"date": d.isoformat(), "symbol": "DEMO", "close": round(close, 4)})
            i += 1
        d += timedelta(days=1)
    return pd.DataFrame(rows)


def prepare_prices(raw: pd.DataFrame, symbol: str | None = None) -> pd.DataFrame:
    df = raw.copy()
    df.columns = [str(x).lower().strip() for x in df.columns]
    if "date" not in df or "close" not in df:
        raise ValueError("CSV must contain date and close columns")
    if "symbol" not in df:
        df["symbol"] = "SAMPLE"
    df["symbol"] = df["symbol"].astype("string").str.strip().str.upper()
    available = df["symbol"].dropna().unique()
    if symbol:
        df = df.loc[df["symbol"] == symbol.upper()]
    elif len(available) > 1:
        raise ValueError("Several tickers found; select one with --symbol")
    df["date"] = pd.to_datetime(df["date"], utc=True, errors="coerce")
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.dropna(subset=["date", "close"])
    df = df.loc[df["close"] > 0]
    df = df.drop_duplicates("date", keep="last").sort_values("date").reset_index(drop=True)
    if df.empty:
        raise ValueError("No valid prices for selected ticker")
    return df[["date", "symbol", "close"]]


def simulate(prices: pd.DataFrame, fast: int = 10, slow: int = 30,
             cost_bps: float = 5.0) -> tuple[pd.DataFrame, dict]:
    if not 1 < fast < slow:
        raise ValueError("Choose periods satisfying 1 < fast < slow")
    if not 0 <= cost_bps <= 1000:
        raise ValueError("Cost must be between 0 and 1000 basis points")
    if len(prices) <= slow:
        raise ValueError(f"Need more than {slow} price observations")

    df = prices.copy()
    df["fast_sma"] = df["close"].rolling(fast, min_periods=fast).mean()
    df["slow_sma"] = df["close"].rolling(slow, min_periods=slow).mean()
    df["signal"] = ((df["fast_sma"] > df["slow_sma"]) &
                    df["slow_sma"].notna()).astype(int)
    # Signal at the end of day t applies only to the next close-to-close period.
    df["position"] = df["signal"].shift(1).fillna(0).astype(int)
    df["daily_return"] = df["close"].pct_change(fill_method=None).fillna(0.0)
    df["turnover"] = df["position"].diff().abs().fillna(df["position"]).astype(int)
    fee = cost_bps / 10000.0
    df["strategy_return"] = df["position"] * df["daily_return"] - fee * df["turnover"]
    # Both strategies use the same fee assumption when initiating a position.
    df["buy_hold_return"] = df["daily_return"].copy()
    df.loc[df.index[0], "buy_hold_return"] = -fee
    df["strategy_equity"] = (1 + df["strategy_return"]).cumprod()
    df["buy_hold_equity"] = (1 + df["buy_hold_return"]).cumprod()

    metrics = {
        "observations": len(df),
        "fast_window": fast,
        "slow_window": slow,
        "cost_bps_per_trade": cost_bps,
        "number_of_position_changes": int(df["turnover"].sum()),
        "strategy": performance(df["strategy_return"]),
        "buy_and_hold": performance(df["buy_hold_return"]),
    }
    return df, metrics


def performance(returns: pd.Series) -> dict:
    equity = (1 + returns).cumprod()
    annual = (float(equity.iloc[-1]) ** (TRADING_DAYS / len(returns))) - 1
    annual_vol = float(returns.std(ddof=0) * math.sqrt(TRADING_DAYS))
    sharpe = (float(returns.mean()) * TRADING_DAYS / annual_vol
              if annual_vol > 0 else None)
    drawdown = equity / equity.cummax() - 1
    return {
        "total_return_pct": round((float(equity.iloc[-1]) - 1) * 100, 2),
        "annualized_return_pct": round(annual * 100, 2),
        "annualized_volatility_pct": round(annual_vol * 100, 2),
        "max_drawdown_pct": round(float(drawdown.min()) * 100, 2),
        "sharpe_zero_rf": None if sharpe is None else round(sharpe, 3),
    }


def run(raw: pd.DataFrame, output: Path, symbol: str | None = None,
        fast: int = 10, slow: int = 30, cost_bps: float = 5.0) -> dict:
    prices = prepare_prices(raw, symbol=symbol)
    results, metrics = simulate(prices, fast=fast, slow=slow, cost_bps=cost_bps)
    output.mkdir(parents=True, exist_ok=True)
    exported = results.copy()
    exported["date"] = exported["date"].dt.strftime("%Y-%m-%d")
    exported.to_csv(output / "equity_curve.csv", index=False)
    (output / "metrics.json").write_text(
        json.dumps(metrics, indent=2) + "\n", encoding="utf-8"
    )
    plt.figure(figsize=(9, 5))
    plt.plot(results["date"], results["strategy_equity"], label="SMA strategy")
    plt.plot(results["date"], results["buy_hold_equity"], label="Buy and hold")
    plt.xlabel("Date")
    plt.ylabel("Growth of 1 unit")
    plt.title("Historical strategy comparison (research only)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output / "equity_curve.png", dpi=140)
    plt.close()
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--demo", action="store_true", help="Generate synthetic prices")
    group.add_argument("--csv", type=Path, help="CSV with date,close[,symbol]")
    parser.add_argument("--symbol", help="Ticker to select in multi-symbol CSV")
    parser.add_argument("--fast", type=int, default=10)
    parser.add_argument("--slow", type=int, default=30)
    parser.add_argument("--cost-bps", type=float, default=5)
    parser.add_argument("--output", type=Path, default=Path("output/backtest"))
    args = parser.parse_args()
    raw = demo_prices() if args.demo else pd.read_csv(args.csv)
    report = run(raw, args.output, symbol=args.symbol,
                 fast=args.fast, slow=args.slow, cost_bps=args.cost_bps)
    print(json.dumps(report, indent=2))
    print(f"Saved results in {args.output}")


if __name__ == "__main__":
    main()
