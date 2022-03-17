import pandas as pd

from adasher.data_utils.__util import DF, Period, Periods
from adasher.templates import *
from adasher.templates.__util import Template, GrowthPieBarTemplate, GrowthPieBarTrendTemplate


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
