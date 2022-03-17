from adasher.elements.impl import header
from adasher.advanced import auto_analytics
from adasher.data_utils import time_period
from datetime import datetime, timedelta
import pandas as pd
import pytest


def test_header():
    assert header('Test') is not None


def test_auto_analytics():
    with pytest.raises(Exception) as execinfo:
        _df = pd.DataFrame()
        auto_analytics(_df, by=None, date_column=tuple(),
                       target_period=time_period(datetime.now()-timedelta(days=1), datetime.now(), 'test'),
                       compare_period=None)
    assert execinfo.value.args[0] == 'Dataframe cannot be empty for auto_analytics'


def test_auto_analytics_date_column():
    with pytest.raises(Exception) as execinfo:
        _df = pd.DataFrame({'a': [1]})
        auto_analytics(_df, by=None, date_column=tuple(),
                       target_period=time_period(datetime.now()-timedelta(days=1), datetime.now(), 'test'),
                       compare_period=None)
    assert execinfo.value.args[0] == "date_column field expected to be tuple with length 2 like: ('column_name', 'ms')"
