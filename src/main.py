from logging import getLogger

from pandas import DataFrame
from plotly.graph_objects import Candlestick, Figure
from streamlit import (
    cache_data,
    columns,
    empty,
    fragment,
    markdown,
    plotly_chart,
    runtime,
    session_state,
    set_page_config,
    write,
)
from streamlit.delta_generator import DeltaGenerator
from streamlit.runtime.scriptrunner import get_script_run_ctx

from config import INSTRUMENTS, SPY_TO_GOLD_30Y_KEY, US_TEN_YEAR_TREASURY_KEY, cache_key
from data_sources.utils.caching import read_cached_df, read_cached_price

logger = getLogger(__name__)

set_page_config(layout="wide")

_min_hist_delta = min(tf.hist_delta for inst in INSTRUMENTS for tf in inst.timeframes)

_CHART_H = 400
_MARGIN_T = 30
_MARGIN_B = 80
_MARGIN_R = 80
_PLOT_H = _CHART_H - _MARGIN_T - _MARGIN_B  # 290
_OVERLAY_OFFSET = _CHART_H + 16  # 416


def get_remote_ip() -> str | None:
    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None

        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except Exception as e:
        return None

    if "X-Real-IP" in session_info.request.headers:
        return session_info.request.headers["X-Real-IP"]
    return None


@cache_data
def _make_base_figure(df: DataFrame, tickstrftime: str) -> Figure:
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
        height=_CHART_H,
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
        margin=dict(t=_MARGIN_T, b=_MARGIN_B, r=_MARGIN_R),
    )

    return fig


@fragment(run_every="2s")
def _price_header() -> None:
    _, *header_cols = columns([2] + [5] * len(INSTRUMENTS))
    for instrument, col in zip(INSTRUMENTS, header_cols):
        price = read_cached_price(f"{instrument.key}price")
        price_str = str(price) if price is not None else "—"
        col.header(f"{instrument.name} - `{price_str}`", divider=instrument.color)


@fragment(run_every=_min_hist_delta)
def _chart_grid() -> None:
    for timeframe_row in zip(*[inst.timeframes for inst in INSTRUMENTS]):
        header_col, *data_cols = columns([2] + [5] * len(INSTRUMENTS))
        header_col.header(timeframe_row[0].label)
        header_col.write(timeframe_row[0].candle_label)

        for instrument, timeframe, col in zip(INSTRUMENTS, timeframe_row, data_cols):
            with col:
                key = cache_key(instrument, timeframe)
                df = read_cached_df(key)
                if df is not None and not df.empty:
                    plotly_chart(_make_base_figure(df, timeframe.tick_fmt), width="stretch", key=key)
                    session_state[f"overlay_{key}"] = empty()
                    session_state[f"yrange_{key}"] = (float(df["Low"].min()), float(df["High"].max()))
                else:
                    write("Fetching data...")


@fragment(run_every="2s")
def _price_overlays() -> None:
    for instrument in INSTRUMENTS:
        for timeframe in instrument.timeframes:
            key = cache_key(instrument, timeframe)
            overlay: DeltaGenerator | None = session_state.get(f"overlay_{key}")
            yrange: tuple[float, float] | None = session_state.get(f"yrange_{key}")
            price = read_cached_price(f"{instrument.key}price")
            if overlay is None or yrange is None or price is None:
                continue
            y_lo, y_hi = yrange
            if y_hi <= y_lo:
                continue
            frac = (price - y_lo) / (y_hi - y_lo)
            y_px = _MARGIN_T + (1.0 - frac) * _PLOT_H
            y_px = max(_MARGIN_T, min(_CHART_H - _MARGIN_B, y_px))
            overlay.markdown(
                f'<div style="position:relative;height:0;margin-top:-{_OVERLAY_OFFSET}px;'
                f'overflow:visible;pointer-events:none;z-index:9999;">'
                f'<div style="position:absolute;top:{y_px:.0f}px;left:0;right:{_MARGIN_R}px;'
                f'height:1px;border-top:1px dashed rgba(255,255,255,0.4);"></div>'
                f'<div style="position:absolute;top:{y_px - 10:.0f}px;right:0;width:{_MARGIN_R}px;'
                f"text-align:right;font-size:11px;color:white;font-family:monospace;"
                f'background:rgba(40,40,40,0.9);padding:1px 4px;">{price:.2f}</div>'
                f"</div>",
                unsafe_allow_html=True,
            )


@fragment(run_every="60s")
def _ap_newsfeed():

    # TODO: Refactor this into a datasource file.
    import requests
    from bs4 import BeautifulSoup

    html = """
    <div style="
        height:1500px;
        overflow-y:scroll;
        border:1px solid #ccc;
        padding:10px;
        border-radius:8px;
        background:#FFFFFF;
    ">
    """

    url = "https://apnews.com/live/iran-war-israel-trump-03-12-2026"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    for tag in [*soup.select(".Advertisement"), *soup.select(".Page-actions")]:
        tag.decompose()
    posts = soup.select_one(".LiveBlogPage-currentPosts")  # selector may change
    if posts is not None:
        html += str(posts)
        html += "</div>"
        return markdown(html, unsafe_allow_html=True)
    else:
        logger.warning("Could not fetch posts from AP News.")


@fragment(run_every="1h")
def _indicators():
    markdown("### Spy to gold ratio")
    df_30y = read_cached_df(SPY_TO_GOLD_30Y_KEY)
    if df_30y is not None and not df_30y.empty:
        plotly_chart(_make_base_figure(df_30y, "%Y"), width="stretch", key=SPY_TO_GOLD_30Y_KEY)
    else:
        write("SPY/Gold (30 year): fetching data...")

    markdown("### US 10-year treasury yield")
    df_30y = read_cached_df(US_TEN_YEAR_TREASURY_KEY)
    if df_30y is not None and not df_30y.empty:
        plotly_chart(_make_base_figure(df_30y, "%Y"), width="stretch", key=US_TEN_YEAR_TREASURY_KEY)
    else:
        write("SPY/Gold (30 year): fetching data...")


_price_header()
_chart_grid()
_price_overlays()

news_col, bonds_col = columns([1, 1])
with news_col:
    news_col.header(f"AP News", divider="violet")
    _ap_newsfeed()
with bonds_col:
    bonds_col.header(f"Indicators", divider="green")
    _indicators()


logger.info(f"Rendering streamlit app for {get_remote_ip()}")
