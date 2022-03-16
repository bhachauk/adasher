from dash import html, dcc
import pandas as pd


from ..adasher.elements.impl import number, number_with_diff, stats_from_df
from ..adasher.cards import card, container, CardHeaderStyles
from ..adasher.templates import pie_plot, bar_plot, scatter_plot
from ..adasher import templates
from ..adasher.advanced import auto_analytics
from . import data


def get_stats_content():
    content = [
        [(number_1(), 2), (number_2(), 2), (number_3(), 2), (number_4(), 2)],
        [(number_with_diff_1(), 2), (number_with_diff_2(), 2), (number_with_diff_3(), 2), (number_with_diff_4(), 2)],
        [(stats_using_df_1(), 4), (stats_using_df_2(), 4)]
    ]

    result = list()
    result.append(container(content))
    return result


def get_py_markdown(code_text):
    return dcc.Markdown('''
    ```python
    {}
    ```
    '''.format(code_text))


def number_1():
    return card("Basic Number", [number(12)])


def number_2():
    return card("Number with style", [number(12, number_style={'font-size': '30px', 'margin': '15px', 'color': 'red'})])


def number_3():
    return card("Number with header", [number(-12, number_style={'font-size': '30px', 'margin': '15px', 'color': 'green'}, header_text='Number')])


def number_4():
    return card("Number with header/style/info", [number(-12, number_style={"color": 'coral'}, info='All', header_text='Number')])


def number_with_diff_1():
    return card("Number Diff 1", [number_with_diff(10, 12, '+ impact fall')])


def number_with_diff_2():
    return card("Number Diff 2", [number_with_diff(12, 10, '+ impact raise')])


def number_with_diff_3():
    return card("Number Diff 3", [number_with_diff(10, 12, '- impact fall', is_positive_impact=False)])


def number_with_diff_4():
    return card("Number Diff 4", [number_with_diff(12, 10, '- impact raise 1', is_positive_impact=False, header='Num 1'),
                                  number_with_diff(15, 10, '- impact raise 1', is_positive_impact=False, header='Num 2')])


def stats_using_df_1():
    df = pd.DataFrame({'Metric': ['A', 'B', 'C'], 'T1': [3, 4, 8], 'T2': [4, 5, 7]})
    return stats_from_df(df, 'T1', 'T2', 'Metric')


def stats_using_df_2():
    df = pd.DataFrame({'Metric': ['A', 'B', 'C'], 'T1': [3, 4, 8], 'T2': [4, 5, 7]})
    return stats_from_df(df, 'T1', 'T2', 'Metric', is_positive_impact=False)


def get_stats_with_plots_content():
    content = [
        [(stats_plot_1(), 6), (stats_plot_2(), 6)],
        [(stats_plot_3(), 6), (stats_plot_4(), 6)],
    ]

    result = list()
    result.append(container(content, 'Number with plot'))
    return result


def stats_plot_1():
    df = pd.DataFrame({'name': ['A', 'B'], 'value': [3, 4]})
    return card('Stats pie plot', [number_with_diff(3, 4, 'info A', header='A'),
                                   number_with_diff(12, 14, 'info B', header='B'),
                                   pie_plot(df, label='name', value='value')])


def stats_plot_2():
    df = pd.DataFrame({'name': ['A', 'B'], 'value': [3, 4]})
    return card('Stats bar plot', [number_with_diff(3, 4, 'info A', header='A'),
                                   number_with_diff(12, 14, 'info B', header='B'),
                                   bar_plot(df, x='name', y='value')])


def stats_plot_3():
    df = pd.DataFrame({'name': ['A', 'B'], 'value': [3, 4]})
    return card('Stats scatter plot', [number_with_diff(3, 4, 'info A', header='A'),
                                   number_with_diff(12, 14, 'info B', header='B'),
                                   scatter_plot(df, x='name', y='value')])


def stats_plot_4():
    df = pd.DataFrame({'name': ['A', 'B', 'A', 'B'], 'value': [3, 4, 5, 6], 'group': ['X', 'X', 'Y', 'Y']})
    return card('Stats scatter group plot', [number_with_diff(3, 4, 'info A', header='A'),
                                   number_with_diff(12, 14, 'info B', header='B'),
                                   scatter_plot(df, x='name', y='value', group='group')])


def get_style_content():
    content = [
        [(header_1(), 2), (header_2(), 2), (header_3(), 2)],
    ]

    result = list()
    result.append(container(content, 'Number with plot'))
    return result


def header_1():
    return card('Default Header', [number(25, 'test')])


def header_2():
    return card('Black font Gray Bg', [number(25, 'test')], header_style=CardHeaderStyles.BLACK_FONT_GRAY_BG)


def header_3():
    return card('White font Black Bg', [number(25, 'test')], header_style=CardHeaderStyles.WHITE_FONT_BLACK_BG)


def get_advanced_stats_content():
    content = [
        # [(advanced_1(), 12)],
        # [(advanced_2(), 12)],

        [(advanced_3(), 12)],
    ]

    result = list()
    result.append(container(content, 'Number with plot'))
    return result


def advanced_1():
    _df = data.get_eq_data()
    _df[data.MAG] = _df[data.MAG].astype(int)
    return auto_analytics(_df, data.MAG, (data.TIME, data.TIME_FORMAT), data.feb_period, data.jan_period,
                          header='Default Stats : February 2022 EQ Stats {} vs {}'.format(data.feb_period.name, data.jan_period.name),
                          header_style=CardHeaderStyles.WHITE_FONT_BLACK_BG
                          )


def advanced_2():
    _df = data.get_eq_data()
    _df[data.MAG] = _df[data.MAG].astype(int)
    return auto_analytics(_df, data.MAG, (data.TIME, data.TIME_FORMAT), target_period=data.feb_period,
                          compare_period=data.jan_period,
                          header='Growth Pie Bar : February 2022 EQ Stats {} vs {}'.format(data.feb_period.name, data.jan_period.name),
                          template=templates.GROWTH_PIE_BAR, header_style=CardHeaderStyles.WHITE_FONT_BLACK_BG)


def advanced_3():
    _df = data.get_eq_data()
    _df[data.MAG] = _df[data.MAG].astype(int)
    return auto_analytics(_df, data.MAG, (data.TIME, data.TIME_FORMAT), target_period=data.feb_period,
                          compare_period=data.jan_period,
                          header='Growth Pie Bar Trend : February 2022 EQ Stats {} vs {}'.format(data.feb_period.name, data.jan_period.name),
                          template=templates.GROWTH_PIE_BAR_TREND, header_style=CardHeaderStyles.WHITE_FONT_BLACK_BG)
