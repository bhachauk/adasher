from adasher.templates.__util import PiePlotElem, BarPlotElem, ScatterPlotElem, ScatterGroupPlotElem


# templates
STATS = 'STATS'
GROWTH_PIE_BAR = 'GROWTH_PIE_BAR'
GROWTH_PIE_BAR_TREND = 'GROWTH_PIE_BAR_TREND'


def pie_plot(df, label, value):
    return PiePlotElem(_df=df, label=label, value=value, layout_kwargs={}).get_div()


def bar_plot(df, x, y):
    return BarPlotElem(_df=df, x=x, y=y, layout_kwargs={}).get_div()


def scatter_plot(df, x, y, group=None):
    if group is None:
        return ScatterPlotElem(_df=df, x=x, y=y, layout_kwargs={}).get_div()
    return ScatterGroupPlotElem(_df=df, x=x, y=y, layout_kwargs={}, group=group).get_div()
