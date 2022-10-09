from adasher.elements.util import Header, Info, Footer
from adasher.elements.util import S1DiffElem, S1Elem


def header(text, align='center', style=None, contents=None):
    return Header(text, align, style, contents).get_div()


def footer(contents: list, style=None):
    return Footer(contents, style).get_div()


def info(text):
    return Info(text=text).get_div()


def number(val, info=None, style=None, header_text=None, number_style=None, header_style=None):
    return S1Elem(val, info=info, style=style, header=header_text, number_style=number_style, header_style=header_style).get_div()


def number_with_diff(val, prev_val, info: str, font_size=25, is_positive_impact=True, header=None, header_style=None, *args, **kwargs):
    """
    :param val:
    :param prev_val:
    :param info:
    :param is_positive_impact: to define type of deviation whether it makes positive or negative impact in result
    :param header
    :param header_style str or dict
    :return:
    """
    return S1DiffElem(val, prev_val, info, is_positive_impact, header=header,
                      header_style=header_style, font_size=font_size, *args, **kwargs).get_div()
