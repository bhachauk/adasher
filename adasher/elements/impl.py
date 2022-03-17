from adasher.elements.util import Header, Info
from adasher.elements.util import S1DiffElem, S1Elem


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
