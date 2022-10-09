import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
from adasher.elements.styles import CardHeaderStyles, NumberHeaderStyles


class Colors:
    GREEN = 'green'
    BLUE = 'blue'
    GRAY = 'gray'
    RED = 'red'
    BLACK = 'black'


# arrows

class Arrows:

    def __init__(self):
        pass

    def up(self):
        pass

    def down(self):
        pass

    def neutral(self):
        pass


class AweArrows(Arrows):

    def __init__(self):
        Arrows.__init__(self)
        self.__pre = 'fas'
        pass

    def up(self):
        return self.__join('fa-arrow-up')

    def down(self):
        return self.__join('fa-arrow-down')

    def neutral(self):
        return self.__join('fa-dot-circle')

    def __join(self, suf):
        return "{} {}".format(self.__pre, suf)


# symbols

class AweSymbols:

    PLUS = 'fas fa-plus'
    MINUS = 'fas fa-minus'


# impacts

class Impact:

    def __init__(self, name):
        self.name = name
        pass

    @staticmethod
    def color():
        pass


class PositiveImpact(Impact):

    def __init__(self):
        Impact.__init__(self, 'positive')

    @staticmethod
    def color():
        return Colors.GREEN

    @staticmethod
    def arrow():
        return 'fas fa-arrow-up'


class NegativeImpact(Impact):

    def __init__(self):
        Impact.__init__(self, 'negative')

    @staticmethod
    def color():
        return Colors.RED


class NeutralImpact(Impact):

    def __init__(self):
        Impact.__init__(self, 'neutral')

    @staticmethod
    def color():
        return Colors.GRAY


def get_delta_pct(a_val, b_val):
    return round(100 if b_val == 0 else ((a_val - b_val) / b_val) * 100, 2)


class Elem:

    def __init__(self, val, *args, **kwargs):
        self.val = val
        self.args = args
        self.kwargs = kwargs
        self._set_style(dict())
        pass

    def get_rows(self):
        return [self.val]

    def get_div(self):
        return html.Div(children=self.get_rows(), style=self.style)

    def _set_style(self, _style):
        self.style = self.kwargs.get('style') if 'style' in self.kwargs.keys() and self.kwargs.get('style') else _style


class S1Elem(Elem):
    def __init__(self, val, *args, **kwargs):
        Elem.__init__(self, val, *args, **kwargs)
        self._set_style({'font-size': 25, 'font-wight': 'bold', 'margin': '15px', 'color': 'blue', 'text-align': 'center'})

    def get_rows(self):
        _result = list()
        if 'header' in self.kwargs.keys():
            _result.append(get_number_header(self.kwargs['header'], self.kwargs['header_style']))

        _result.append(html.P(self.val, style=self.kwargs.get('number_style', {})))
        if 'info' in self.kwargs.keys():
            _result.append(Info(self.kwargs['info']).get_div())
        return _result


def get_number_header(header, _style):

    basic_style = {'color': Colors.BLACK, 'font-size': '12px', 'margin': '15px', 'padding': '10px'}

    if isinstance(_style, str):

        _styles_dict = {
            NumberHeaderStyles.RED: Colors.RED,
            NumberHeaderStyles.GRAY: Colors.GRAY,
            NumberHeaderStyles.BASIC_BLACK: Colors.BLACK
        }

        basic_style.update({'color': _styles_dict.get(_style, Colors.BLACK)})

    if isinstance(_style, dict):
        basic_style = _style

    _title = Title(header=header)
    _title.title_style = basic_style
    return _title.get_div()


def get_card_header_impl() -> dict:
    return {
        CardHeaderStyles.BASIC_BROWN: S1Title,
        CardHeaderStyles.WHITE_FONT_BLACK_BG: S2Title,
        CardHeaderStyles.BLACK_FONT_GRAY_BG: S3Title,
        CardHeaderStyles.GRAY_FONT_WHITE_BG: S4Title
    }


class Title(Elem):

    def __init__(self, header, *args, **kwargs):
        Elem.__init__(self, header, *args, **kwargs)
        self.title_style = {'color': 'gray', 'font-size': '12px', 'margin': '15px', 'padding': '10px'}

    def get_rows(self):
        return [html.P(self.val, style=self.title_style)]


class S1Title(Title):

    def __init__(self, header, *args, **kwargs):
        Title.__init__(self, header, *args, **kwargs)
        self.title_style = {'color': 'brown', 'font-size': '15px', 'padding': '10px'}


class S2Title(Title):

    def __init__(self, header, *args, **kwargs):
        Title.__init__(self, header, *args, **kwargs)
        self.title_style = {
            'font-size': '15px',
            'text-align': 'left',
            'padding': '10px',
            'background-color': '#333',
            'color': 'white',
            'border': '1px solid rgba(0, 0, 0, .125)',
            'border-radius': '0.25rem 0.25rem 0 0',
        }


class S3Title(Title):

    def __init__(self, header, *args, **kwargs):
        Title.__init__(self, header, *args, **kwargs)
        self.title_style = {
            'font-size': '15px',
            'text-align': 'left',
            'padding': '10px',
            'background-color': '#ccc',
            'border': '1px solid rgba(0, 0, 0, .125)',
            'border-radius': '0.25rem 0.25rem 0 0',
        }


class S4Title(Title):
    """
    simple gray font
    """
    def __init__(self, header, *args, **kwargs):
        Title.__init__(self, header, *args, **kwargs)
        self.title_style = {'font-size': '8px', 'color': '#999', 'text-align': 'left',
                            'padding': '5px 5px 0px'}


class DiffElem(Elem):

    def __init__(self, a_val, b_val, info=None, is_positive_impact=True, *args,  **kwargs):
        Elem.__init__(self, a_val)
        self.a_val = a_val
        self.b_val = b_val
        self.info = info
        self.p_impact = is_positive_impact
        self.args = args
        self._set_style({'display': 'inline-block', 'margin': '10px', 'text-align': 'center', 'align': 'center'})
        self.kwargs = kwargs

    def get_delta(self):
        return self.a_val-self.b_val

    def get_delta_per_str(self):
        return str(get_delta_pct(self.a_val, self.b_val)) + '%'

    def get_impact_color(self):

        if self.get_delta() == 0:
            return Colors.GRAY

        _imp = self.get_delta() > 0
        if not self.p_impact:
            _imp = not _imp
        return Colors.GREEN if _imp else Colors.RED

    def get_arr(self):
        arr = AweArrows()
        arrow = arr.neutral() if self.get_delta() == 0 else arr.up() if self.get_delta() >= 0 else arr.down()
        return html.I(className=arrow)

    def get_symbol(self):
        return html.I(className=AweSymbols.PLUS if self.get_delta() >= 0 else AweSymbols.MINUS)

    def get_rows(self):
        result = list()
        if 'header' in self.kwargs.keys():
            result.append(get_card_header_impl().get(self.kwargs['header_style'], Title)(self.kwargs['header']).get_div())
        result.append(html.P(self.a_val))
        result.append(html.P(self.get_delta()))
        result.append(html.P(self.get_delta_per_str()))
        return result


class S1DiffElem(DiffElem):

    def __init__(self, a_val, b_val, info=None, is_positive_impact=True, font_size=25, *args,  **kwargs):
        DiffElem.__init__(self, a_val, b_val, info, is_positive_impact, *args,  **kwargs)
        self.font_size = font_size

    def get_rows(self):
        _rows = list()
        _header_style = {'font-size': '15px', 'margin': '2px', 'padding': '2px'}
        if 'header_style' in self.kwargs.keys() and isinstance(self.kwargs['header_style'], dict):
            _header_style.update(self.kwargs['header_style'])

        if 'header' in self.kwargs.keys():
            _rows.append(get_number_header(self.kwargs['header'], _header_style))

        _rows.append(html.P(self.a_val, style={'font-size': str(self.font_size)+'px', 'margin-bottom': '0', 'text-align': 'center'}))
        _rows.append(html.P(children=[self.get_symbol(), " ", str(abs(self.get_delta())), " ",
                                      self.get_arr(), " ", self.get_delta_per_str(), "  ",
                                      ],
                            style={'color': self.get_impact_color(), 'padding-top': '2px;', 'margin': '9px',
                                   'font-size': str(int(self.font_size/2))+'px', 'text-align': 'center'}))

        __info_style = self.kwargs['info_style'] if 'info_style' in self.kwargs.keys() else None
        _rows.append(Info(self.info, __info_style).get_div())
        return _rows


class Header(Elem):

    def __init__(self, text, align='center', style=None, contents=None):
        Elem.__init__(self, text)
        self.align = align
        self.style = self.__get_style(style_obj=style)
        self.contents = contents

    def get_rows(self):
        result = list()
        result.append(html.H3(self.val, style={'margin': '25px'}))
        if self.contents:
            [result.append(_c) for _c in self.contents]
        return result

    def get_div(self):
        return html.Div(self.get_rows(), style=self.style)

    def __get_style(self, style_obj):
        __styles = {
            0: {
                'border-bottom': '1px solid #ccc',
                'width': '100%',
                'display': 'inline-block',
                'text-align': self.align,
                'font-size': '20px'
            },
            1: {
                'border-bottom': '1px solid #ccc',
                'background': '#333',
                'width': '100%',
                'display': 'inline-block',
                'text-align': self.align,
                'font-size': '20px',
                'color': 'white'
            }
        }
        return __styles.get(style_obj, {}) if isinstance(style_obj, int) else style_obj


class Footer(Elem):

    def __init__(self, contents: list, style=None):
        Elem.__init__(self, '')
        self.contents = contents
        self.style = self.__get_style()
        if style:
            self.style.update(style)

    def get_rows(self):
        result = list()
        result.append(html.Footer(children=self.contents, style=self.style))
        return result

    def get_div(self):
        return html.Div(self.get_rows(), style=self.style)

    def __get_style(self):
        return dict(position='fixed', height='50px', background='#333', bottom='0px', left='0px', right='0px',
                    margin='0px 0px 0px 0px')


class Info(Elem):

    def __init__(self, text, info_style=None):
        Elem.__init__(self, text)
        self.info_style = {'font-size': '12px', 'color': 'gray'} if info_style is None else info_style

    def get_rows(self):
        result = list()
        result.append(html.P(self.val, style=self.info_style))
        return result
