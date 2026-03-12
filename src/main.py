from pandas import DataFrame
from plotly.graph_objects import Candlestick, Figure
from streamlit import columns, plotly_chart, set_page_config, write
from streamlit.elements.plotly_chart import PlotlyState
from streamlit_autorefresh import st_autorefresh

from config import INSTRUMENTS, cache_key
from data_sources.utils.caching import read_cached_df, read_cached_price

st_autorefresh(interval=5000)
set_page_config(layout="wide")


def get_plotly_chart(df: DataFrame, tickstrftime="%b %d", current_price: float | None = None) -> PlotlyState:
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

    if current_price is not None:
        fig.add_shape(
            type="line", x0=0, x1=1, xref="paper",
            y0=current_price, y1=current_price, yref="y",
            line=dict(dash="dot", color="rgba(255,255,255,0.4)", width=1),
        )
        fig.add_annotation(
            x=1, xref="paper", y=current_price, yref="y",
            text=f" {current_price} ", showarrow=False,
            xanchor="left", yanchor="middle",
            bgcolor="rgba(40,40,40,0.9)", bordercolor="white", borderwidth=1,
            font=dict(color="white", size=11),
        )

    return plotly_chart(fig, width="stretch")


# instrument header row
_, *header_cols = columns([2] + [5] * len(INSTRUMENTS))
for instrument, col in zip(INSTRUMENTS, header_cols):
    price = read_cached_price(f"{instrument.key}price")
    price_str = str(price) if price is not None else "—"
    col.header(f"{instrument.name} - `{price_str}`", divider=instrument.color)

# one row per timeframe
for timeframe_row in zip(*[inst.timeframes for inst in INSTRUMENTS]):
    header_col, *data_cols = columns([2] + [5] * len(INSTRUMENTS))
    header_col.header(timeframe_row[0].label)
    header_col.write(timeframe_row[0].candle_label)

    for instrument, timeframe, col in zip(INSTRUMENTS, timeframe_row, data_cols):
        with col:
            df = read_cached_df(cache_key(instrument, timeframe))
            if df is not None and not df.empty:
                price = read_cached_price(f"{instrument.key}price")
                get_plotly_chart(df, timeframe.tick_fmt, price)
            else:
                write("Fetching data...")
