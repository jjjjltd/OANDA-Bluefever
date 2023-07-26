import pandas as pd
from dateutil.parser import *

import utils
import instrument
import ma_result
import ma_excel

pd.set_option('display.max_columns', None)

def is_trade(row):
    """  Return direction of MA Cross."""
    if row.DIFF >= 0 and row.DIFF_PREV < 0:
        return 1
    if row.DIFF <= 0 and row.DIFF_PREV > 0:
        return -1
    return 0

def get_ma_col(ma):
    """  Simple:  Return MA column name based on received MA number."""
    return f"MA_{ma}"

def get_price_data(pairname, granularity):
    """ Read pricing data, convert to numeric, return DF"""
    df = pd.read_csv(utils.get_hist_data_filename(pairname, granularity))

    non_nums = ["time", "volume", "ticker"]
    num_cols = [x for x in df.columns if x not in non_nums]
    df[num_cols] = df[num_cols].apply(pd.to_numeric)
    df.info()
    return df[["time", "ticker", "mid_o", "mid_h", "mid_l", "mid_c"]]

def process_data(ma_short, ma_long, price_data):
    """ Add all required MAs to DF """
    ma_list = set(ma_short + ma_long)

    for ma in ma_list:
        price_data[get_ma_col(ma)] = price_data.mid_c.rolling(window=ma).mean()

    return price_data

def evaluate_pair(i_pair, mashort, malong, price_data):

    price_data = price_data[['time', 'mid_c', get_ma_col(mashort), get_ma_col(malong)]].copy()

    price_data["DIFF"] = price_data[get_ma_col(mashort)] - price_data[get_ma_col(malong)]
    price_data["DIFF_PREV"] = price_data.DIFF.shift(1)
    price_data["IS_TRADE"] = price_data.apply(is_trade, axis = 1)

    df_trades = price_data[price_data.IS_TRADE!=0].copy()
    df_trades["PIP_Delta"] = (df_trades.mid_c.diff() /  i_pair.ins_pipLocation).shift(-1)
    df_trades["GAIN"] = df_trades.PIP_Delta * df_trades.IS_TRADE
    df_trades["PAIR"] = i_pair.ins_name
    df_trades["MASHORT"] = mashort
    df_trades["MALONG"] = malong

    del df_trades[get_ma_col(mashort)]
    del df_trades[get_ma_col(malong)]

    df_trades["time"] = [parse(x) for x in df_trades.time]
    df_trades["DURATION"] = df_trades.time.diff().shift(-1)
    df_trades["DURATION"] = [x.total_seconds() / 3600 for x in df_trades.DURATION]
    df_trades.dropna(inplace=True)

    #  print(f"{i_pair.ins_name} {mashort}/{malong} made {df_trades.shape[0]} trades.  Gain: {df_trades['GAIN'].sum():.2f}")
    params = {'mashort': mashort, 'malong': malong, }
    return ma_result.MAResult(
        i_pair.ins_name,
        df_trades,
        params
    )

def store_trades(results):
    """ Write full Trade Details to ./Data/All Trades.csv """
    all_trade_df_list = [x.df_trades for x in results]
    all_trade_df = pd.concat(all_trade_df_list)
    all_trade_df.to_csv("./Data/All Trades.csv")
    return all_trade_df

def process_results(results):    
    """ Write out results to ./Data/ma_test_results.csv  
    Note:  This file is aggregated by ma_results.py and has a single line per pair/cross.  Not transaction level, therefore no time data.  """
    results_list = [r.result_obj() for r in results]
    final_df = pd.DataFrame.from_dict(results_list)
   
    final_df.to_csv("./Data/ma_test_results.csv")

    return final_df


def get_existing_pairs(pair_str):
    """  Receive string of individual currencies, pair up and check if they are available instruments.    """
    existing_pairs = instrument.Instrument.get_instruments_dict().keys()
    pairs = pair_str.split(",")

    test_list = []

    # Loop through pairs list twice (each currency within each currency)
    for p1 in pairs:
        for p2 in pairs:
            p = f"{p1}_{p2}"
            if p in existing_pairs:
                test_list.append(p)

    return test_list

def run():
    """ 
    1. Get existing pairs: read pairs from /Data/available instruments.csv
          Note:  available instruments written in getinstruments.py
    2. Get instrument data, including decimal place of pip.
    3. Aggregate data to ma_test_results using ma_result.py, MAResult class.
    4. Write detail to all_trades
     
      
       
        
          """

    pair_str = "GBP,JPY,USD,CAD,EUR,CHF,NZD"
    granularity = "H1"
    ma_short = [4, 8, 16, 24, 32, 64]
    ma_long = [8, 16, 32, 64, 96, 128, 256]

    test_pairs = instrument.Instrument.get_pairs_from_string(pair_str)

    

    results = []
    for pairname in test_pairs:
        print("running pair...", pairname)
        i_pair = instrument.Instrument.get_instruments_dict()[pairname]

        price_data = get_price_data(pairname, granularity)
        price_data = process_data(ma_short, ma_long, price_data)

        for _malong in ma_long:
            for _mashort in ma_short:
                if _mashort >= _malong:
                    continue
                results.append(evaluate_pair(i_pair, _mashort, _malong, price_data))
                break
            
    final_df = process_results(results)
    all_trades_df = store_trades(results)

    ma_excel.create_excel(final_df, all_trades_df)
if __name__ == "__main__":
    run()