import oanda_api
import utils
import pandas as pd

# https://www.youtube.com/watch?v=Lc9AArgBZDk&list=PLZ1QII7yudbecO6a-zAI6cuGP1LLnmW8e&index=20
#
# This is a point where lots of things are coming together, and beginning to feel a bit fast.  So.
# Time for a summary/recap of where we are, and how we got here.
#
#

api = oanda_api.OandaAPI()
api.save_instruments()

candles_df = pd.DataFrame()

instruments_df = pd.read_csv("./Data/available_instruments.csv", index_col=False)
for pair in instruments_df["name"]:
    code, data = api.fetch_candlesticks(pair, api.candles_count, api.granularity)
    
    if code == 200:
        candle_df = api.build_candlesdf(data)
        print(f"Candle data:  {candle_df}")
        candle_df.info()
        candle_df["MA_8"] = candle_df.mid_c.rolling(window=8).mean()
        candle_df["MA_64"] = candle_df.mid_c.rolling(window=64).mean()
        api.save_candlestick(candle_df, pair, api.granularity)
        break
    else:
        print(f"Failed to get candlestick data for {pair}")

