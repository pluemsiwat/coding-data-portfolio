"""Generate deterministic fictional OHLCV examples for offline testing."""
import csv
import math
from datetime import date, timedelta
from pathlib import Path


def make_sample(path: Path, days: int = 260) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    day = date(2024, 1, 1)
    number = 0
    while number < days:
        if day.weekday() < 5:
            for symbol, start, drift in [("DEMOA", 95, 0.0008), ("DEMOB", 130, 0.00025)]:
                close = start * math.exp(drift * number + 0.045 * math.sin(number / 15 + (1 if symbol == "DEMOB" else 0)))
                open_price = close * (1 - 0.004 * math.sin(number / 7))
                high = max(open_price, close) * 1.008
                low = min(open_price, close) * 0.992
                rows.append([day.isoformat(), symbol, round(open_price, 4),
                             round(high, 4), round(low, 4), round(close, 4),
                             100000 + 200 * number])
            number += 1
        day += timedelta(days=1)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["date", "symbol", "open", "high", "low", "close", "volume"])
        writer.writerows(rows)
    return path


if __name__ == "__main__":
    result = make_sample(Path("data/sample_prices.csv"))
    print(f"Created {result}")
