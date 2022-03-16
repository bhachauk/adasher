from .util import Header, Info
from .util import S1DiffElem, S1Elem

from adasher.cards import card, container
import pandas as pd


def header(text, align='center'):
    return Header(text, align).get_div()


def info(text):
    return Info(text=text).get_div()


def number(val, info=None, style=None, header_text=None, number_style=None, header_style=None):
    return S1Elem(val, info=info, style=style, header=header_text, number_style=number_style, header_style=header_style).get_div()


def number_with_diff(val, prev_val, info: str, is_positive_impact=True, header=None, header_style=None):
    """
    :param val:
    :param prev_val:
    :param info:
    :param is_positive_impact: to define type of deviation whether it makes positive or negative impact in result
    :param header
    :param header_style str or dict
    :return:
    """
    return S1DiffElem(val, prev_val, info, is_positive_impact, header=header, header_style=header_style).get_div()


def stats_from_df(df: pd.DataFrame, current_column, previous_column, label, is_positive_impact=True):

    result = list()
    for _, _row in df.iterrows():
        result.append(number_with_diff(_row[current_column], _row[previous_column], '', header=_row[label],
                                       is_positive_impact=is_positive_impact))

    return card(label, result)
