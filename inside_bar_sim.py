import pandas as pd
import datetime as dt
import utils
import instrument
import defs


SLOSS  = defs.SLOSS 
TPROFIT  = defs.TPROFIT 

ENTRY_PRC  = defs.ENTRY_PRC 
BUY  = defs.BUY 
SELL  = defs.SELL 
NONE  = defs.NONE 

LOSS_FRACTION  = defs.LOSS_FRACTION 
GAIN_FRACTION  = defs.GAIN_FRACTION  / defs.SLOSS

def direction(row):
    """ Return price direction based on close vs open price i.e. if close higher, upwards (1)..."""
    if row.mid_c > row.mid_o:
        return BUY
    return SELL

def get_signal(row):
    """  Identify encapsulation in previous candle and return direction.  Pass back zero if no encapsulation.  
        1 = Buy, -1=Sell:  Buy if encapsulated in a previously upward candle...      """
    if row.mid_h_prev > row.mid_h and row.mid_l_prev > row.mid_l:
        return row.DIRECTION_prev
    return 0

def get_entry_stop(row):
    if row.SIGNAL == 1:
        return (row.RANGE_prev * ENTRY_PRC) + row.ask_h_prev
    elif row.SIGNAL == -1:
        return row.bid_l_prev - (row.RANGE_prev * ENTRY_PRC)
    else:
        return 0
    
def get_stop_loss(row):
    if row.SIGNAL == 1:
        return row.ENTRY - (row.RANGE_prev * SLOSS)
    if row.SIGNAL == -1:
        return row.ENTRY + (row.RANGE_prev * SLOSS)
    else:
        return 0
    
def get_take_profit(row):
    if row.SIGNAL == 1:
        return row.ENTRY + (row.RANGE_prev * TPROFIT)
    if row.SIGNAL == -1:
        return row.ENTRY - (row.RANGE_prev * TPROFIT)
    else:
        return 0
    
def triggered(direction, current_price, signal_price):
    if direction == 1 and current_price > signal_price:
        return True
    elif direction == -1 and current_price < signal_price:
        return True
    else:
        return False
    
def end_hit_calc(direction, SL, price, start_price):
    """  Return fractional impact accounting for Entry/Stoploss swing.  """
    delta = price - start_price
    full_delta = start_price - SL
    fraction = abs(delta / full_delta)

    if direction == 1 and price >= start_price:
        return fraction
    elif direction == 1 and price <= start_price:
        return -fraction
    elif direction == -1 and price <= start_price:
        return fraction
    elif direction == -1 and price >= start_price:
        return -fraction
    
    print("Error:  end_hit_calc should return something!!")

def process_buy(TP, SL, ask_prices, bid_prices, entry_price):
    for index, price in enumerate(ask_prices):
        if triggered(1, price, entry_price) == True:
            for live_price in bid_prices[index:]:    
                if live_price >= TP:
                    return GAIN_FRACTION
                elif live_price <= SL:
                    return LOSS_FRACTION
            return end_hit_calc(1, SL, live_price, entry_price)
    return 0.0 

def process_sell(TP, SL, ask_prices, bid_prices, entry_price):
    for index, price in enumerate(bid_prices):
        if triggered(-1, price, entry_price) == True:
            for live_price in ask_prices[index:]:    
                if live_price <= TP:
                    return GAIN_FRACTION
                elif live_price >= SL:
                    return -LOSS_FRACTION
            return end_hit_calc(-1, SL, live_price, entry_price)   
    return 0.0

def get_test_pairs(pair_str):
        """  See instrument.get_pairs_from_string.  I think this is a needless duplicate...    """
        existing_pairs = instrument.Instrument.get_instruments_dict().keys()
        pairs = pair_str.split(",")

        pair_list = []

        # Loop through pairs list twice (each currency within each currency)
        for p1 in pairs:
            for p2 in pairs:
                p = f"{p1}_{p2}"
                if p in existing_pairs:
                    pair_list.append(p)

        return pair_list

def get_trades_df(df_raw):

    df = df_raw.copy()

    df['RANGE'] = df.mid_h - df.mid_l
    df['mid_h_prev'] = df.mid_h.shift(1)
    df['mid_l_prev'] = df.mid_l.shift(1)
    df['ask_h_prev'] = df.ask_h.shift(1)
    df['bid_l_prev'] = df.bid_l.shift(1)
    df['RANGE_prev'] = df.RANGE.shift(1)
    df['DIRECTION'] = df.apply(direction, axis=1)
    df['DIRECTION_prev'] = df.DIRECTION.shift(1).fillna(0).astype(int)
    
    df.dropna(inplace=True)
    
    df['SIGNAL'] = df.apply(get_signal, axis=1)
    df['ENTRY'] = df.apply(get_entry_stop, axis=1)
    df['STOPLOSS'] = df.apply(get_stop_loss, axis=1)
    df['TAKEPROFIT'] = df.apply(get_take_profit, axis=1)


    df_trades = df[df.SIGNAL!=NONE].copy()
    df_trades["next"] =  df_trades["time"].shift(-1)
    df_trades["trade_end"] = df_trades.next + dt.timedelta(hours=3, minutes=55)
    df_trades["trade_start"] = df_trades.time + dt.timedelta(hours=4)

    df.dropna(inplace=True)
    df_trades.reset_index(drop=True, inplace=True)

    return df_trades

def evaluate_pair(df_trades, m5_data):
    total = 0
    for index, row in df_trades.iterrows():
        m5_slice = m5_data[(m5_data.time >= row.trade_start) & (m5_data.time <= row.trade_end)]
        if row.SIGNAL == BUY:
            r = process_buy(row.TAKEPROFIT, row.STOPLOSS, m5_slice.ask_c.values, m5_slice.bid_c.values, row.ENTRY)
            total += r
        elif row.SIGNAL == SELL:
            r = process_sell(row.TAKEPROFIT, row.STOPLOSS, m5_slice.ask_c.values, m5_slice.bid_c.values, row.ENTRY)
            total += r            
    
    return total

def run():
    """ 
    1. Get existing pairs: read pairs from /Data/available instruments.csv
          Note:  available instruments written in getinstruments.py
    2. Get instrument data, including decimal place of pip.
    3. Aggregate data to ma_test_results using ma_result.py, MAResult class.
    4. Write detail to all_trades
     
      
       
        
          """

    pair_str = "GBP,JPY,USD,CAD,EUR,CHF,NZD"
    
    test_pairs = instrument.Instrument.get_pairs_from_string(pair_str)
    grand_total = 0
    

    results = []
    for pairname in test_pairs:
        
        i_pair = instrument.Instrument.get_instruments_dict()[pairname]

        h4_data = pd.read_csv(utils.get_hist_data_filename(pairname, "H4"))
        m5_data = pd.read_csv(utils.get_hist_data_filename(pairname, "M5"))


        df_trades = get_trades_df(h4_data)

        score = evaluate_pair(df_trades, m5_data)
        grand_total += score
        print(f"{pairname} {score:.0f}")
    print(f"TOTAL: {grand_total:,0f}")
    

if __name__ == "__main__":
    run()
