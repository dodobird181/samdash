from pandas import DataFrame
from plotly.graph_objects import Candlestick, Figure
from streamlit import columns, plotly_chart, session_state, set_page_config, write
from streamlit.elements.plotly_chart import PlotlyState
from streamlit_autorefresh import st_autorefresh

from config import INSTRUMENTS, TIMEFRAMES, cache_key
from data_sources.utils.caching import read_cached_df

st_autorefresh(interval=5000)
set_page_config(layout="wide")

# fetch latest spot prices into session state (only on first load per session)
for instrument in INSTRUMENTS:
    state_key = f"price_{instrument.key}"
    if state_key not in session_state:
        session_state[state_key] = instrument.price_fetcher()


def get_plotly_chart(df: DataFrame, tickstrftime="%b %d") -> PlotlyState:
    # timezone conversion
    try:
        df.index = df.index.tz_localize("UTC").tz_convert("US/Eastern")  # type: ignore
    except Exception:
        try:
            df.index = df.index.tz_convert("US/Eastern")  # type: ignore
        except Exception:
            pass

    fig = Figure(
        data=[
            Candlestick(
                x=df.index,  # type: ignore
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                increasing_line_color="green",
                decreasing_line_color="red",
                hovertemplate=(
                    "%{x|%b %-d, %Y at %-I:%M %p %Z}<br>"
                    "Open: %{open}<br>"
                    "High: %{high}<br>"
                    "Low: %{low}<br>"
                    "Close: %{close}<extra></extra>"
                ),
            )
        ]
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=False,
        xaxis=dict(
            type="category",
            tickmode="array",
            tickvals=df.index[::8],
            ticktext=df.index[::8].strftime(tickstrftime),  # type: ignore
            tickangle=-40,
        ),
    )
    return plotly_chart(fig, width="stretch")


# instrument header row
_, *header_cols = columns([2] + [5] * len(INSTRUMENTS))
for instrument, col in zip(INSTRUMENTS, header_cols):
    price = session_state[f"price_{instrument.key}"]
    col.header(f"{instrument.name} - `{price}`", divider=instrument.color)

# one row per timeframe
for timeframe in TIMEFRAMES:
    header_col, *data_cols = columns([2] + [5] * len(INSTRUMENTS))
    header_col.header(timeframe.label)
    header_col.write(timeframe.candle_label)

    for instrument, col in zip(INSTRUMENTS, data_cols):
        with col:
            df = read_cached_df(cache_key(instrument, timeframe))
            if df is not None and not df.empty:
                get_plotly_chart(df, timeframe.tick_fmt)
            else:
                write("Fetching data...")

# refresh spot prices at the end of each run
for instrument in INSTRUMENTS:
    session_state[f"price_{instrument.key}"] = instrument.price_fetcher()
