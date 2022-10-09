from adasher.elements.util import Elem
from adasher.elements import util as elem_util, impl as elem_impl
from dash import html
import dash_bootstrap_components as dbc
import pandas as pd


def card(_header, _elems: list, header_style=None):
    _card = Card(header=_header, header_style=header_style)
    for _elem in _elems:
        _card.append(_elem)
    return _card.get_div()


def container(cards: list, title=None):
    container_content = [dbc.Row([dbc.Col(card, width=w) for card, w in row], justify='center', style={'margin': '25px'}) for row in cards]
    if title:
        container_content = [title] + container_content
    return dbc.Container(container_content, fluid=True)


def stats_from_df(df: pd.DataFrame, current_column, previous_column, label, is_positive_impact=True, header: str = None,
                  header_style: str = None):
    result = list()
    for _, _row in df.iterrows():
        result.append(elem_impl.number_with_diff(_row[current_column], _row[previous_column], '', header=_row[label],
                                                 is_positive_impact=is_positive_impact))
    return card(header if header else label, result, header_style=header_style)


class Card(Elem):

    def __init__(self, header, header_style, *args, **kwargs):

        # type handling
        if not (isinstance(header_style, str) or isinstance(header_style, dict) or header_style is None):
            raise Exception('header_style expected to be str or dict. found: {}'.format(str(type(header_style))))

        Elem.__init__(self, val=header, *args, **kwargs)
        self.header = header
        self.header_style = header_style
        self.__content = list()
        self.style = {
            'margin': '5px',
            'border': '1px solid rgba(0, 0, 0, .125)',
            'border-radius': '0.25rem',
            'text-align': 'center'
        }

    def append(self, elem: html.Div):
        self.__content.append(elem)

    def __get_header_div(self):
        return self.__get_header_template().get_div()

    def get_rows(self):
        return [self.__get_header_div()] + self.__content

    def __get_header_template(self) -> elem_util.Title:

        if isinstance(self.header_style, dict):
            if self.header is not None:
                _title = elem_util.Title(header=self.header)
            _title.title_style = self.header_style
            return _title

        return elem_util.get_card_header_impl().get(self.header_style, elem_util.S1Title)(header=self.header)
