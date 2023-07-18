import pandas as pd
import utils
import instrument
import ma_result
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
    return df[["time", "ticker", "mid_o", "mid_h", "mid_l", "mid_c"]]

def process_data(ma_short, ma_long, price_data):
    """ Add all required MAs to DF """
    ma_list = set(ma_short + ma_long)

    for ma in ma_list:
        price_data[get_ma_col(ma)] = price_data.mid_c.rolling(window=ma).mean()

    return price_data

def evaluate_pair(i_pair, mashort, malong, price_data):

    price_data["DIFF"] = price_data[get_ma_col(mashort)] - price_data[get_ma_col(malong)]
    price_data["DIFF_PREV"] = price_data.DIFF.shift(1)
    price_data["IS_TRADE"] = price_data.apply(is_trade, axis = 1)

    df_trades = price_data[price_data.IS_TRADE!=0].copy()
    df_trades["PIP_Delta"] = (df_trades.mid_c.diff() /  i_pair.ins_pipLocation).shift(-1)
    df_trades["GAIN"] = df_trades.PIP_Delta * df_trades.IS_TRADE

    #  print(f"{i_pair.ins_name} {mashort}/{malong} made {df_trades.shape[0]} trades.  Gain: {df_trades['GAIN'].sum():.2f}")

    params = {'mashort': mashort, 'malong': malong}
    return ma_result.MAResult(
        i_pair.ins_name,
        df_trades,
        params
    )

def process_results(results):    
    results_list = [r.result_obj() for r in results]
    final_df = pd.DataFrame.from_dict(results_list)

    print(final_df.info())
    print(final_df.head())

def run():

    pairname = "GBP_JPY"
    granularity = "H1"
    ma_short = [8, 16, 32, 64]
    ma_long = [32, 64, 96, 128, 256]
    i_pair = instrument.Instrument.get_instruments_dict()[pairname]

    price_data = get_price_data(pairname, granularity)
    price_data = process_data(ma_short, ma_long, price_data)

    results = []

    for _malong in ma_long:
        for _mashort in ma_short:
            if _mashort >= _malong:
                continue
            results.append(evaluate_pair(i_pair, _mashort, _malong, price_data.copy()))
            
    process_results(results)

if __name__ == "__main__":
    run()