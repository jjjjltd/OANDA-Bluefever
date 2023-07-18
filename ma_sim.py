import pandas as pd
import utils
import instrument
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

    print(f"{i_pair.ins_name} {mashort}/{malong} made {df_trades.shape[0]} trades.  Gain: {df_trades['GAIN'].sum():.2f}")

    return df_trades["GAIN"].sum()

def run():

    pairname = "GBP_JPY"
    granularity = "H1"
    ma_short = [8, 16, 32, 64]
    ma_long = [32, 64, 96, 128, 256]
    i_pair = instrument.Instrument.get_instruments_dict()[pairname]

    price_data = get_price_data(pairname, granularity)
    price_data = process_data(ma_short, ma_long, price_data)

    # Set defaults for best pips, best ma-short and long...
    best = -1000000.0
    b_mashort = 0
    b_malong = 0

    for _malong in ma_long:
        for _mashort in ma_short:
            if _mashort >= _malong:
                continue
            res = evaluate_pair(i_pair, _mashort, _malong, price_data.copy())
            if res > best:
                best = res
                b_mashort = _mashort
                b_malong = _malong

    print(f"Best strategy: {best:.2f} return with  MASHORT: {b_mashort:.0f}, MALONG: {b_malong:.0f}")        

if __name__ == "__main__":
    run()