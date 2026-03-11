"""Dashboard utility functions."""

from datetime import date, timedelta
from random import Random


def generate_time_series(base_value: float, volatility: float, days: int = 180):
    """Generate a mock daily price time series for the past N days."""
    today = date.today()
    dates = []
    prices = []
    price = base_value
    rng = Random(base_value)  # deterministic seed for reproducibility

    for i in range(days, 0, -1):
        day = today - timedelta(days=i)
        if day.weekday() >= 5:  # skip weekends
            continue
        change = rng.gauss(0, volatility)
        price = max(price * (1 + change), 0.01)
        dates.append(day.isoformat())
        prices.append(round(price, 4))

    return {"x": dates, "y": prices}
