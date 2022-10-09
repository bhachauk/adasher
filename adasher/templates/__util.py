from adasher.elements.util import Elem, Colors
from adasher.data_utils.__util import Period, Periods, DF, Names, DATE_FORMAT, DATE_HOUR_FORMAT
from adasher.cards import card, stats_from_df

import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go


class PlotElem(Elem):
    def __init__(self, _df: pd.DataFrame, layout_kwargs, *args, **kwargs):
        Elem.__init__(self, None, *args, **kwargs)
        self._df = _df
        self.layout_kwargs = layout_kwargs


class PiePlotElem(PlotElem):
    def __init__(self, _df: pd.DataFrame, label, value, layout_kwargs, *args, **kwargs):
        PlotElem.__init__(self, _df, layout_kwargs, *args, **kwargs)
        self.label = label
        self.value = value

    def get_rows(self):
        result = list()

        fig = go.Figure()
        fig.add_trace(go.Pie(labels=self._df[self.label], values=self._df[self.value]))
        fig.update_layout(**self.layout_kwargs)

        result.append(dcc.Graph(figure=fig))
        return result


class BarPlotElem(PlotElem):
    def __init__(self, _df: pd.DataFrame, x, y, layout_kwargs, *args, **kwargs):
        PlotElem.__init__(self, _df, layout_kwargs, *args, **kwargs)
        self.x = x
        self.y = y

    def get_rows(self):
        result = list()

        fig = go.Figure()
        fig.add_trace(go.Bar(x=self._df[self.x], y=self._df[self.y]))
        fig.update_layout(**self.layout_kwargs)

        result.append(dcc.Graph(figure=fig))
        return result


class BarPlotWithColorHoverElem(BarPlotElem):
    def __init__(self, _df: pd.DataFrame, x, y, target_column, compare_column, layout_kwargs, *args, **kwargs):
        BarPlotElem.__init__(self, _df, x, y, layout_kwargs, *args, **kwargs)
        self.compare_column = compare_column
        self._df[Names.COLOR] = self._df[Names.PCT_DELTA].apply(lambda _x: Colors.RED if _x < 0 else Colors.GREEN)
        self._df[Names.HOVER] = self._df[Names.PCT_DELTA].astype(str) + '% {} : '.format(compare_column) + \
                               self._df[compare_column].astype(str) + ' {} : '.format(target_column) + self._df[target_column].astype(str)

    def get_rows(self):
        result = list()

        fig = go.Figure()
        fig.add_trace(go.Bar(x=self._df[self.x], y=self._df[self.y], marker_color=self._df[Names.COLOR],
                             hovertext=self._df[Names.HOVER]))
        fig.update_layout(**self.layout_kwargs)

        result.append(dcc.Graph(figure=fig))
        return result


class ScatterPlotElem(PlotElem):
    def __init__(self, _df: pd.DataFrame, x, y, layout_kwargs, *args, **kwargs):
        PlotElem.__init__(self, _df, layout_kwargs, *args, **kwargs)
        self.x = x
        self.y = y

    def get_rows(self):
        result = list()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=self._df[self.x], y=self._df[self.y]))
        fig.update_layout(**self.layout_kwargs)

        result.append(dcc.Graph(figure=fig))
        return result


class ScatterGroupPlotElem(PlotElem):
    def __init__(self, _df: pd.DataFrame, x, y, group, layout_kwargs, *args, **kwargs):
        PlotElem.__init__(self, _df, layout_kwargs, *args, **kwargs)
        self.x = x
        self.y = y
        self.group = group

    def get_rows(self):
        result = list()

        fig = go.Figure()

        for _val in list(self._df[self.group].unique()):
            __df = self._df[self._df[self.group] == _val]
            fig.add_trace(go.Scatter(x=__df[self.x], y=__df[self.y], name=str(_val)))

        fig.update_layout(**self.layout_kwargs)
        result.append(dcc.Graph(figure=fig))
        return result


class Template:

    def __init__(self, _df: pd.DataFrame, by, date_column: tuple, target_period: Period, compare_period: Period = None,
                 header: str = None, header_style: str = None, template_args: dict = None):

        # Handling invalids

        if _df.empty:
            raise Exception('Dataframe cannot be empty for auto_analytics')

        if len(date_column) < 2:
            raise Exception("date_column field expected to be tuple with length 2 like: ('column_name', 'ms')")

        self.col_name = by
        self.target_period = target_period
        self.date_col_name = date_column[0]

        if target_period is not None and compare_period is None:
            compare_period = Periods.get_prev_period(target_period)

        self.compare_period = compare_period
        self._adf = DF(_df, dict((x, y) for x, y in [date_column]))
        self._diff_df = self._adf.get_diff_df_by(by, self.date_col_name, target_period, compare_period)
        self.header = header
        self.header_style = header_style
        self.template_args = template_args if template_args else dict()

    def _get_stats_from_df(self):
        return stats_from_df(self._diff_df, self.target_period.name, self.compare_period.name, self.col_name,
                             **self.template_args)

    def _get_content(self):
        return [
            self._get_stats_from_df()
        ]

    def get_trend_df(self, date_time_fmt: str):
        if date_time_fmt is None:
            date_time_fmt = DATE_FORMAT if self.target_period.get_elps_sec() > 24 * 60 * 60 else DATE_HOUR_FORMAT
        __df = self._adf.get_date_trend_df(self.col_name, self.date_col_name, self.target_period, date_time_fmt)
        return __df

    def get_card(self):
        if self.header is None:
            return html.Div(children=self._get_content())
        return card(self.header, self._get_content(), header_style=self.header_style)


class GrowthPieBarTemplate(Template):

    def __init__(self, _df: pd.DataFrame, by, date_column: tuple, target_period: Period, compare_period: Period = None,
                 header: str = None, header_style: str = None, template_args:dict = None):
        Template.__init__(self, _df, by, date_column, target_period, compare_period, header, header_style, template_args)

    def _get_content(self):
        _pie_layout = {'title_text': self.col_name}
        _bar_layout = {'xaxis_title': self.col_name, 'yaxis_title': 'Growth Rate (%)'}
        _content = [
            PiePlotElem(_df=self._diff_df, label=self.col_name, value=self.target_period.name, layout_kwargs=_pie_layout).get_div(),
            BarPlotWithColorHoverElem(_df=self._diff_df, x=self.col_name, y=Names.PCT_DELTA, layout_kwargs=_bar_layout,
                                      compare_column=self.compare_period.name,
                                      target_column=self.target_period.name).get_div()
        ]

        return [html.Div(children=_content, style={'display': 'flex'})]


class GrowthPieBarTrendTemplate(Template):

    def __init__(self, _df: pd.DataFrame, by, date_column: tuple, target_period: Period, compare_period: Period = None,
                 header: str = None, date_time_format: str = None, header_style: str = None, template_args:dict = None):
        Template.__init__(self, _df, by, date_column, target_period, compare_period, header, header_style, template_args)
        self._trend_df = self.get_trend_df(date_time_format)

    def _get_content(self):
        _pie_layout = {'title_text': self.col_name}
        _bar_layout = {'xaxis_title': self.col_name, 'yaxis_title': 'Growth Rate (%)'}
        _trend_layout = {'xaxis_title': Names.DATE, 'yaxis_title': Names.COUNT}
        _content = [
            PiePlotElem(_df=self._diff_df, label=self.col_name, value=self.target_period.name, layout_kwargs=_pie_layout).get_div(),
            BarPlotWithColorHoverElem(_df=self._diff_df, x=self.col_name, y=Names.PCT_DELTA, layout_kwargs=_bar_layout,
                                      compare_column=self.compare_period.name,
                                      target_column=self.target_period.name).get_div()
        ]

        return [html.Div(children=_content, style={'display': 'flex'}),
                ScatterGroupPlotElem(self._trend_df, x=Names.DATE, y=self.target_period.name, group=self.col_name,
                                     layout_kwargs=_trend_layout).get_div()]
