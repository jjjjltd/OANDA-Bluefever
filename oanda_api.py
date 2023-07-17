# https://www.youtube.com/watch?v=wg5herWaV4M&list=PLZ1QII7yudbecO6a-zAI6cuGP1LLnmW8e&index=14

import pandas as pd
import utils
import requests
import defs
import pprint
class OandaAPI():

    def __init__(self):
        """ Oanda API initialisation"""
        self.session = requests.Session()
        self.candles_count = 400
        self.granularity = "H4"
    
    def __repr__(self):
        """ Output for log on API creation.  """
        print("Oanda API class created.")
    
    def fetch_instruments(self):
        """ Fetch instruments list from URL """
        url = f"{defs.OANDA_URL}/accounts/{defs.ACCOUNT_ID}/instruments"
        response = self.session.get(url, params=None, headers=defs.SECURE_HEADER)
        return response.status_code, response.json()

    def get_instrumentsdf(self):
        """ Build instruments dataframe, if API call successful.  """
        code, data = self.fetch_instruments()

        if code == 200:
            df = pd.DataFrame.from_dict(data["instruments"])
            return df[["name", "type", "displayName", "pipLocation", "marginRate"]]
        else:
            return None

    def save_instruments(self):
        """  Save instruments dataframe to CSV in Data folder.  """
        df = self.get_instrumentsdf()
        if df is not None:
            df.to_csv(utils.get_instruments_data_filename())
        else:
            print("Something weird happened here.")

    def fetch_candlesticks(self, pair_name, count, granularity):
        """  Get candlesticks from OANDA URL.  """
        url = f"{defs.OANDA_URL}/instruments/{pair_name}/candles"
        
        params = dict(
            count = count,
            granularity = granularity,
            price="MBA"
        )

        response = self.session.get(url, params=params, headers=defs.SECURE_HEADER)
        return response.status_code, response.json()
    
    def build_candlesdf(self, response):
        prices = ["bid", "mid", "ask"]
        ohlc = ["o", "h", "l", "c"]
        candle_df = pd.DataFrame()
        our_data = []
        
        for ticker in response["instrument"]:
                                            
            for candle in response["candles"]:
        

                new_dict = dict()
                new_dict["ticker"] = response["instrument"]


                if candle["complete"] == False:
                    continue

                new_dict["time"] = candle["time"]
                new_dict["volume"] = candle["volume"]

                for price in prices:
                    for oh in ohlc:
                        new_dict[f"{price}_{oh}"] = candle[price][oh]
    
                our_data.append(new_dict)

        return pd.DataFrame.from_dict(our_data)

    def save_candlestick(self, df, pair, granularity):
        """ Save candlestick dataframe to csv"""
        df.to_csv(f"./Data/{pair}_{granularity}.csv")

# if __name__ == "__main__":
#     api = OandaAPI()
#     res, data = api.fetch_candlesticks("EUR_NOK", 50, "H4")
#     api.save_instruments()
    