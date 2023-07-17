import oanda_api
import utils
import pandas as pd

# https://www.youtube.com/watch?v=Lc9AArgBZDk&list=PLZ1QII7yudbecO6a-zAI6cuGP1LLnmW8e&index=20
#
# This is a point where lots of things are coming together, and beginning to feel a bit fast.  So.
# Time for a summary/recap of where we are, and how we got here.
#
# Where we are:
# * Got Instrument and Candle Data via Oanda APIs
# * Used DataFrames (Pandas) for "ETL" to storage.
# * Worked with Plotly to output useful candle charts with trend lines.
# * Next (beyond recap):  use the data we have to implement a simple trading strategy (MACD)

###  Refresh list of instruments, write to csv and read back.
api = oanda_api.OandaAPI()
api.save_instruments()
instruments_df = pd.read_csv("./Data/available_instruments.csv", index_col=False)


### For each instrument (ForEx currency pair), get candles data
candles_df = pd.DataFrame()
for pair in instruments_df["name"]:
    code, data = api.fetch_candlesticks(pair, api.candles_count, api.granularity)
    
    if code == 200:
        candle_df = api.build_candlesdf(data)
        print(f"Candle data:  {candle_df}")
        candle_df.info()
        ### Plot indicators, MAs in this case.
        candle_df["MA_8"] = candle_df.mid_c.rolling(window=8).mean()
        candle_df["MA_64"] = candle_df.mid_c.rolling(window=64).mean()
        ### Save data to disk
        api.save_candlestick(candle_df, pair, api.granularity)
        ###  Output candles chart (when you have time to spare!!)
        # fig = oanda_api.go.Figure()
        # fig = api.format_plotly(fig, candle_df[-50:])
        # fig.show()
    else:
        print(f"Failed to get candlestick data for {pair}")

