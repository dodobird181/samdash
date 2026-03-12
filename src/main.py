from datetime import timedelta

from matplotlib import pyplot
from pandas import DataFrame
from plotly.graph_objects import Candlestick, Figure
from streamlit import (
    area_chart,
    cache_data,
    columns,
    header,
    html,
    markdown,
    plotly_chart,
)
from streamlit import pyplot as st_pyplot
from streamlit import session_state, set_page_config, write
from streamlit.delta_generator import DeltaGenerator
from streamlit.elements.plotly_chart import PlotlyState
from streamlit_autorefresh import st_autorefresh

from data_sources.investingdotcom import latest_brent_crude_oil_price
from data_sources.kitco import latest_gold_price, latest_silver_price
from data_sources.utils.caching import get_cached_df
from data_sources.utils.plotting import get_candle_chart
from data_sources.yfinance import get_yfinance_data

st_autorefresh(interval=5000)  # refresh every 5 seconds
set_page_config(layout="wide")

if "latest_gold_price" not in session_state:
    session_state.latest_gold_price = latest_gold_price()

if "latest_silver_price" not in session_state:
    session_state.latest_silver_price = latest_silver_price()

if "latest_brent_crude_oil_price" not in session_state:
    session_state.latest_brent_crude_oil_price = latest_brent_crude_oil_price()

_, gold_col_header, silver_col_header, oil_col_header = columns([2, 5, 5, 5])
row1_header, row1_gold, row1_silver, row1_oil = columns([2, 5, 5, 5])
row2_header, row2_gold, row2_silver, row2_oil = columns([2, 5, 5, 5])
row3_header, row3_gold, row3_silver, row3_oil = columns([2, 5, 5, 5])

row1_header.space(size="xxlarge")
row1_header.header("1 Day")
row1_header.write("15 min candles")

row2_header.space(size="xxlarge")
row2_header.header("10 Day")
row2_header.write("4 hour candles")

row3_header.space(size="xxlarge")
row3_header.header("3 Month")
row3_header.write("daily candles")

gold_col_header.header(f"Gold - `{session_state.latest_gold_price}`", divider="yellow")
silver_col_header.header(f"Silver - `{session_state.latest_silver_price}`", divider="grey")
oil_col_header.header(f"Brent Oil - `{session_state.latest_brent_crude_oil_price}`", divider="red")


def get_plotly_chart(df: DataFrame, tickstrftime="%b %d") -> PlotlyState:

    # this is time-zome conversion slop but I don't care enough to do this properly...
    try:
        df.index = df.index.tz_localize("UTC").tz_convert("US/Eastern")  # type: ignore
    except:
        df.index = df.index.tz_convert("US/Eastern")  # type: ignore

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
                    "%{x|%b %-d, %Y at %-I:%M %p %Z}<br>"  # hover text
                    "Open: %{open}<br>"
                    "High: %{high}<br>"
                    "Low: %{low}<br>"
                    "Close: %{close}<extra></extra>"  # hides the secondary box
                ),
            )
        ]
    )
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=False,
        xaxis=dict(
            # remove gaps in x-axis data (e.g., weekends)
            type="category",
            tickmode="array",
            # every 8th timestamp
            tickvals=df.index[::8],
            ticktext=df.index[::8].strftime(tickstrftime),  # type: ignore
            # tilt for readability
            tickangle=-40,
        ),
    )
    # fig.add_shape(
    #     type="rect",
    #     x0=0,
    #     y0=0,
    #     x1=1,
    #     y1=1,
    #     xref="paper",
    #     yref="paper",
    #     line=dict(color="red", width=3),
    #     fillcolor="rgba(0,0,0,0)",  # transparent fill
    # )
    return plotly_chart(fig, width="stretch")


########
# GOLD #
########


with row1_gold:
    df = get_cached_df(
        obj_name="gold15min",
        data_provider=lambda: get_yfinance_data("GC=F", period="1d", interval="15m"),
        delta=timedelta(minutes=5),
    )
    get_plotly_chart(df, "%-I:%M %p")


with row2_gold:
    df = get_cached_df(
        obj_name="gold4h",
        data_provider=lambda: get_yfinance_data("GC=F", period="10d", interval="4h"),
        delta=timedelta(minutes=5),
    )
    get_plotly_chart(df)


with row3_gold:
    df = get_cached_df(
        obj_name="gold1d",
        data_provider=lambda: get_yfinance_data("GC=F", period="90d", interval="1d"),
        delta=timedelta(minutes=5),
    )
    get_plotly_chart(df, "%b %d, %Y")

##########
# SILVER #
##########

with row1_silver:
    df = get_cached_df(
        obj_name="silver15min",
        data_provider=lambda: get_yfinance_data("SI=F", period="1d", interval="15m"),
        delta=timedelta(minutes=5),
    )
    get_plotly_chart(df, "%-I:%M %p")

with row2_silver:
    df = get_cached_df(
        obj_name="silver4h",
        data_provider=lambda: get_yfinance_data("SI=F", period="10d", interval="4h"),
        delta=timedelta(minutes=30),
    )
    get_plotly_chart(df)

with row3_silver:
    df = get_cached_df(
        obj_name="silver1d",
        data_provider=lambda: get_yfinance_data("SI=F", period="90d", interval="1d"),
        delta=timedelta(minutes=30),
    )
    get_plotly_chart(df, "%b %d, %Y")


#######
# Oil #
#######


with row1_oil:
    df = get_cached_df(
        obj_name="oil15min",
        data_provider=lambda: get_yfinance_data("BZ=F", period="1d", interval="15m"),
        delta=timedelta(minutes=5),
    )
    get_plotly_chart(df, "%-I:%M %p")


with row2_oil:
    df = get_cached_df(
        obj_name="oil4h",
        data_provider=lambda: get_yfinance_data("BZ=F", period="10d", interval="4h"),
        delta=timedelta(minutes=30),
    )
    get_plotly_chart(df)

with row3_oil:
    df = get_cached_df(
        obj_name="oil1d",
        data_provider=lambda: get_yfinance_data("BZ=F", period="90d", interval="1d"),
        delta=timedelta(minutes=30),
    )
    get_plotly_chart(df, "%b %d, %Y")


# with col2:
#     header(f"Silver - `{session_state.latest_silver_price}`", divider="grey")
#     fig = get_candle_chart("SI=F", xlabel="10 days (4 hours bars)", period="10d", interval="4h")
#     st_pyplot(fig)
#     pyplot.close(fig)
#     fig = get_candle_chart("SI=F", xlabel="3 months (daily bars)", period="90d", interval="1d")
#     st_pyplot(fig)
#     pyplot.close(fig)

# with col3:
#     header(f"Brent Oil - `{session_state.latest_brent_crude_oil_price}`", divider="red")
#     fig = get_candle_chart("BZ=F", xlabel="10 days (4 hours bars)", period="10d", interval="4h")
#     st_pyplot(fig)
#     pyplot.close(fig)
#     fig = get_candle_chart("BZ=F", xlabel="3 months (daily bars)", period="90d", interval="1d")
#     st_pyplot(fig)
#     pyplot.close(fig)


session_state.latest_gold_price = latest_gold_price()
session_state.latest_silver_price = latest_silver_price()
session_state.latest_brent_crude_oil_price = latest_brent_crude_oil_price()
