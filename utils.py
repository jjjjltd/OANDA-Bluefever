import datetime as dt
from dateutil.parser import *

def get_hist_data_filename(pair, granularity):
    """ Return pair data by reading csv e.g. ./Data/GBP_JPY_H1  """
    return f"./Data/Pairs/{pair}_{granularity}.csv"

def get_instruments_data_filename():
    """ Return the path/filename to available instruments file """
    return "./Data/available_instruments.csv"

def time_utc():
    return dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)

def get_utc_dt_from_string(date_str):
    d = parse(date_str)
    return d.replace(tzinfo=dt.timezone.utc)


if __name__ == "__main__":
    print(dt.datetime.utcnow())
    print(time_utc())
    print(get_utc_dt_from_string("2023-07-26 03:00:00"))