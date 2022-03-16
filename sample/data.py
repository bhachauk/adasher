import pandas as pd
import numpy as np
import os

from ..adasher.data_utils import time_period
from datetime import datetime, timedelta


MAG = 'mag'
TIME = 'time'
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


jan_start = datetime.strptime('2021-01-01', '%Y-%m-%d')
jan_end = jan_start + timedelta(days=31)
feb_end = jan_end + timedelta(days=28)

jan_period = time_period(jan_start, jan_end, 'Jan')
feb_period = time_period(jan_end, feb_end, 'Feb')


def get_eq_data():
    return pd.read_csv('https://earthquake.usgs.gov/fdsnws/event/1/query?starttime=2021-01-01&endtime=2021-03-01&format=csv&minmagnitude=2')


if __name__ == '__main__':

    _file = 'eq.csv'

    if not os.path.exists(_file):
        _df = get_eq_data()
        _df.to_csv(_file, index=False)
    else:
        _df = pd.read_csv(_file)

    _df['time'] = pd.to_datetime(_df['time'], format=TIME_FORMAT)
    _df['mon'] = _df['time'].dt.strftime("%m")
    print(_df)

    print(_df[['mon']].groupby('mon').size())
