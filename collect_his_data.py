import pandas as pd
import datetime as dt

from instrument import Instrument
import utils
from oanda_api import OandaAPI

INCREMENTS = {
    "M5": 5,
    "H1": 60,
    "H4": 240
}

def create_file(pair, granularity, api):
    candle_count = 2000
    time_step = INCREMENTS[granularity] * candle_count

    # current_time = dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    # print(current_time)
    # years = 15
    # back_from_current = (dt.datetime.utcnow())-dt.timedelta(years*365)
    # print(minus2years)

    end_date = utils.get_utc_dt_from_string("2022-12-31 23:59:59")
    date_from = utils.get_utc_dt_from_string("2020-01-01 00:00:00")

    candle_dfs = []

    date_to = date_from
    while date_to < end_date:
        date_to = date_from + dt.timedelta(seconds=time_step*60)
        if date_to > end_date:
            date_to=end_date
            # TODO:  Collect candles
        print(date_from, date_to)
        date_from = date_to



def run_collection():
    pair_list = "GBP,JPY,USD,CAD,EUR,CHF,NZD"
    api=OandaAPI
    # g = granularity, i=instrument
    for g in INCREMENTS.keys():
        for i in Instrument.get_pairs_from_string(pair_list):
            print(g, i)
            create_file(i, g, api)
            break

if __name__ == "__main__":
    run_collection()