from mplfinance import plot as fin_plot
from pandas import DataFrame


def get_candle_chart(df: DataFrame, title=None, xlabel=None):
    """
    Create a matplotlib candle-chart using a HLOCV dataframe.
    """

    optional_params = {}
    if title is not None:
        optional_params["title"] = title
    if xlabel is not None:
        optional_params["xlabel"] = xlabel

    fig, _ = fin_plot(
        df,
        type="candle",
        style="yahoo",
        ylabel="USD",
        volume=True,
        returnfig=True,
        **optional_params,
    )
    return fig
