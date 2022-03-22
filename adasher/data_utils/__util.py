import pandas as pd
from dateutil import rrule
from datetime import datetime, timedelta
import numpy as np


DATE_FORMAT = '%Y-%m-%d'
DATE_HOUR_FORMAT = '%Y-%m-%d-%H'


def today_start():
    today = datetime.today()
    return today.replace(hour=0, minute=0, second=0, microsecond=0)


class Names:

    DELTA = 'DELTA'
    PCT_DELTA = 'PCT_DELTA'
    COUNT = 'COUNT'
    COLOR = 'COLOR'

    DAY = 'DAY'
    HOUR = 'HOUR'
    TIME_UNIT = 'CUSTOM__TIME_UNIT'
    DATE = 'DATE'
    HOVER = 'HOVER'
    SESSION = 'SESSION'


class TimePeriods:

    YD = 'Yesterday'
    TD = 'Today'
    DBY = 'Day before Yesterday'
    LW = 'Last week'
    WBL = 'Week before last'
    LM = 'Last 30 Days'
    MBL = '30 Days before last'

    @staticmethod
    def check_tp(time_period):
        tp_dict = get_tps_vs_dict()
        if time_period not in (list(tp_dict.keys()) + list(tp_dict.values())):
            raise Exception("Invalid time_period " + time_period)


def get_tps_vs_dict():
    vs_map = dict()
    vs_map[TimePeriods.TD] = TimePeriods.YD
    vs_map[TimePeriods.YD] = TimePeriods.DBY
    vs_map[TimePeriods.LW] = TimePeriods.WBL
    vs_map[TimePeriods.LM] = TimePeriods.MBL
    return vs_map


class Period:
    def __init__(self, start: datetime, end: datetime, name):
        self.name = name
        self.start = start
        self.end = end

    def get_dates(self):
        return rrule.rrule(rrule.DAILY, dtstart=self.start, until=self.end)

    def __str__(self):
        return str(self.start) + '-' + str(self.end)

    def get_elps_sec(self):
        return self.end.timestamp() - self.start.timestamp()


class Periods:
    @staticmethod
    def get(tp: str):
        tps = dict()
        tps[TimePeriods.TD] = Period(today_start(), datetime.now(), TimePeriods.TD)
        tps[TimePeriods.YD] = Period(today_start() - timedelta(days=1), today_start(), TimePeriods.YD)
        tps[TimePeriods.LW] = Period(today_start() - timedelta(days=7), today_start(), TimePeriods.LW)
        tps[TimePeriods.LM] = Period(today_start() - timedelta(days=30), today_start(), TimePeriods.LM)
        tps[TimePeriods.WBL] = Period(today_start() - timedelta(days=14), today_start() - timedelta(days=7), TimePeriods.WBL)
        tps[TimePeriods.MBL] = Period(today_start() - timedelta(days=60), today_start() - timedelta(days=30), TimePeriods.MBL)
        return tps.get(tp, None)

    @staticmethod
    def get_prev_period(period: Period, name: str = None):
        _elapsed = period.end - period.start
        name = name if name else 'prev_' + period.name
        return Period(period.start - _elapsed, period.start, name)


class SessionBinConfig:
    BIN_HOUR = [0, 4, 8, 12, 16, 20, 24]
    BIN_LABEL = ['Late_Night', 'Early_Morning', 'Morning', 'Noon', 'Evening', 'Night']


class DF:

    """
    :param date_time_cols expects dict like { column_name : dateformat }
    """

    def __init__(self, _df: pd.DataFrame, date_time_cols=None, *args, **kwargs):
        self._df = _df
        self.args = args
        self.kwargs = kwargs
        self._dt_cols = date_time_cols

        # prepare
        self.__set_dt_details()

    def __set_dt_details(self):
        if self._dt_cols is not None and isinstance(self._dt_cols, dict):
            for _col, _fmt in self._dt_cols.items():
                self._df[_col] = pd.to_datetime(self._df[_col], format=_fmt)

    def __check_col(self, column_name):
        if column_name not in self._df.columns:
            raise Exception("Invalid column_name : " + column_name)

    def __check_date_col(self, column_name):
        self.__check_col(column_name)
        if self._dt_cols is None or column_name not in self._dt_cols.keys():
            raise Exception("datetime not configured for column_name : " + column_name)

    def get_df(self):
        return self._df

    def get_df_by(self, _time_col, period: Period):
        return self._df[((self._df[_time_col].astype(np.int64) / int(1e6)) >= period.start.timestamp() * 1000) & ((self._df[_time_col].astype(np.int64) / int(1e6)) < period.end.timestamp() * 1000)]

    def __get_df_group_count(self, col, _time_col, period: Period):
        _df = self.get_df_by(_time_col, period)
        return _df[[col]].groupby([col]).size().reset_index(name=period.name)

    def get_date_trend_df(self, col, _time_col, period: Period, date_time_fmt=DATE_FORMAT):
        _df = self.get_df_by(_time_col, period)
        _df[Names.TIME_UNIT] = _df[_time_col].dt.strftime(date_time_fmt)
        return _df[[Names.TIME_UNIT, col]].groupby([Names.TIME_UNIT, col]).size().reset_index(name=period.name).rename(columns={Names.TIME_UNIT: Names.DATE})

    def get_diff_df_by(self, column_name, time_col, current_period: Period, previous_period: Period):

        a_df = self.__get_df_group_count(column_name, time_col, current_period)
        b_df = self.__get_df_group_count(column_name, time_col, previous_period)

        __act_values = list(set(list(a_df[column_name].unique()) + list(b_df[column_name].unique())))
        m_df = pd.DataFrame(data={column_name: __act_values})
        m_df = pd.merge(m_df, a_df, on=column_name, how='left').fillna(0)
        m_df = pd.merge(m_df, b_df, on=column_name, how='left').fillna(0)
        m_df[Names.DELTA] = m_df[current_period.name] - m_df[previous_period.name]
        m_df[Names.PCT_DELTA] = round((m_df[Names.DELTA] / m_df[previous_period.name]) * 100, 2).replace(np.inf, 100)
        return m_df

    def auto_analytics_by(self, col_name, time_column, time_period):

        # check args
        self.__check_date_col(time_column)

        # time_period handling
        if not (isinstance(time_period, str) or isinstance(time_period, Period)):
            raise Exception('time_period value expected to be str or Period')

        a_tp, b_tp = None, None

        if isinstance(time_period, str):
            TimePeriods.check_tp(time_period)
            a_tp, b_tp = Periods.get(time_period), Periods.get(get_tps_vs_dict()[time_period])

        elif isinstance(time_period, Period):
            a_tp, b_tp = time_period, Periods.get_prev_period(time_period)

        m_df = self.get_diff_df_by(col_name, time_column, a_tp, b_tp)

        print(m_df)

    def get_auto_analytics_field(self, column_name, time_period):

        if column_name not in self._df.columns:
            raise Exception("Invalid column_name : " + column_name)

        tp_dict = get_tps_vs_dict()

        if time_period not in (list(tp_dict.keys()) + list(tp_dict.values())):
            raise Exception("Invalid time_period " + time_period)

    def apply_day_session(self, time_column, day=True, session=True, hour=False):

        self._df[Names.HOUR] = self._df[time_column].dt.hour

        if day:
            self._df[Names.DAY] = self._df[time_column].dt.day_name()

        if session:
            self._df[Names.SESSION] = pd.cut(self._df[Names.HOUR], bins=SessionBinConfig.BIN_HOUR,
                                             labels=SessionBinConfig.BIN_LABEL, include_lowest=True)

        if not hour:
            del self._df[Names.HOUR]

