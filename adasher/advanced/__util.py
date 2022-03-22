import pandas as pd

from mlxtend.frequent_patterns import association_rules
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpmax, fpgrowth

from adasher.data_utils.__util import DF, Period
from adasher.templates import *
from adasher.templates.__util import Template, GrowthPieBarTemplate, GrowthPieBarTrendTemplate
from adasher.cards import card

import dash_bootstrap_components as dbc
from dash import html, dcc


def auto_analytics(_df: pd.DataFrame, by, date_column: tuple, target_period: Period, compare_period: str = None,
                   header: str = None, template: str = STATS, header_style=None, **kwargs):
    _template = __templates_dict(template)(_df, by, date_column, target_period, compare_period, header=header,
                                           header_style=header_style, **kwargs)
    return _template.get_card()


def __templates_dict(template: str):
    templates = {
        STATS: Template,
        GROWTH_PIE_BAR: GrowthPieBarTemplate,
        GROWTH_PIE_BAR_TREND: GrowthPieBarTrendTemplate
    }
    return templates.get(template, Template)


# Association rule mining

def association(_df: pd.DataFrame,  date_column: tuple, time_period: Period = None, header: str = None,
                header_style: str = None, apply_column_prefix=False, **kwargs):
    return AssociationMining(_df, date_column, time_period, header, header_style, apply_column_prefix, **kwargs).get_card()


class AssociationMining:

    def __init__(self, _df: pd.DataFrame, date_column: tuple, time_period: Period = None, header: str = None,
                 header_style: str = None, apply_column_prefix=False, **kwargs):

        if _df.empty:
            raise Exception("Empty Dataframe")

        self.kwargs = kwargs
        self.ANTECEDENTS = 'antecedents'
        self.CONSEQUENTS = 'consequents'
        self.SUPPORT = 'support'
        self.CONFIDENCE = 'confidence'

        # Handling invalids

        if _df.empty:
            raise Exception('Dataframe cannot be empty for auto_analytics')

        if len(date_column) < 2:
            raise Exception("date_column field expected to be tuple with length 2 like: ('column_name', 'ms')")

        self.time = time_period
        self.date_col_name = date_column[0]
        self._adf = DF(_df, dict((x, y) for x, y in [date_column]))
        self._adf.apply_day_session(self.date_col_name)
        self.apply_column_prefix=apply_column_prefix

        if time_period is not None:
            self._df = self._adf.get_df_by(self.date_col_name, time_period)

        else:
            self._df = self._adf.get_df()

        self.header = header
        self.header_style = header_style

    def __pre_process(self):
        for _col in self._df.columns:
            self._df[_col] = _col + '_' + self._df[_col].astype(str)

    def __get_req_cols(self):
        return [self.ANTECEDENTS, self.CONSEQUENTS, self.CONFIDENCE, self.SUPPORT]

    def get_freq_item_sets(self, min_support=0.1):

        if self.apply_column_prefix:
            self.__pre_process()

        __df = self._df.copy()
        del __df[self.date_col_name]
        te = TransactionEncoder()
        te_ary = te.fit(__df.values).transform(__df.values)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        return fpgrowth(df, min_support=min_support, use_colnames=True)

    def get_association(self, support_th=0.1, confidence_th=0.1):

        freq_itemsets = self.get_freq_item_sets(support_th)
        rules = association_rules(freq_itemsets, metric=self.CONFIDENCE, min_threshold=confidence_th)

        def __sort_and_join(x, sep='<->'):
            x.sort()
            return sep.join(x)

        _df = rules[self.__get_req_cols()]
        _df[self.ANTECEDENTS] = rules[self.ANTECEDENTS].apply(lambda x: list(x)).apply(__sort_and_join, args=(', ', ))
        _df[self.CONSEQUENTS] = rules[self.CONSEQUENTS].apply(lambda x: list(x)).apply(__sort_and_join, args=(', ', ))
        _df[self.CONFIDENCE] = round(rules[self.CONFIDENCE] * 100, 2)
        _df[self.SUPPORT] = round(rules[self.SUPPORT] * 100, 2)
        return _df.sort_values(by=self.CONFIDENCE, ascending=False).head(10)

    def __get_content(self):
        __content = list()
        __content.append(html.Div(children=[dbc.Table.from_dataframe(self.get_association(), striped=True, bordered=True, hover=True)]))
        return __content

    def get_card(self):
        return card(self.header, self.__get_content(), self.header_style)
