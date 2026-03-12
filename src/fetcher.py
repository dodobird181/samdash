"""
Standalone cache fetcher — run alongside the Streamlit app:

    python src/fetcher.py

Fetches all configured instruments/timeframes and writes to the cache directory.
Streamlit reads only from cache and never triggers its own fetches.
"""
import time
from datetime import datetime

from config import INSTRUMENTS, TIMEFRAMES, cache_key
from data_sources.utils.caching import _cache_df
from data_sources.yfinance import get_yfinance_data


def fetch_all() -> None:
    for instrument in INSTRUMENTS:
        for timeframe in TIMEFRAMES:
            key = cache_key(instrument, timeframe)
            try:
                data = get_yfinance_data(instrument.ticker, period=timeframe.period, interval=timeframe.interval)
                if data.empty:
                    print(f"[{datetime.now():%H:%M:%S}] {key}: empty response, skipping")
                    continue
                _cache_df(key, data, timeframe.delta)
                print(f"[{datetime.now():%H:%M:%S}] {key}: cached {len(data)} rows")
            except Exception as e:
                print(f"[{datetime.now():%H:%M:%S}] {key}: error — {e}")


if __name__ == "__main__":
    min_sleep = min(tf.delta.total_seconds() for tf in TIMEFRAMES)
    while True:
        fetch_all()
        print(f"[{datetime.now():%H:%M:%S}] sleeping {min_sleep:.0f}s...")
        time.sleep(min_sleep)
