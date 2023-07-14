# https://www.youtube.com/watch?v=wg5herWaV4M&list=PLZ1QII7yudbecO6a-zAI6cuGP1LLnmW8e&index=14

import pandas as pd
import utils
import requests
import defs

class OandaAPI():

    def __init__(self):
        self.session = requests.Session()
    
    def fetch_instruments(self):
        url = f"{defs.OANDA_URL}/accounts/{defs.ACCOUNT_ID}/instruments"
        response = self.session.get(url, params=None, headers=defs.SECURE_HEADER)
        return response.status_code, response.json()

    def get_instrumentsdf(self):
        code, data = self.fetch_instruments()

        if code == 200:
            df = pd.DataFrame.from_dict(data["instruments"])
            return df[["name", "type", "displayName", "pipLocation", "marginRate"]]
        else:
            return None

    def save_instruments(self):
        df = api.get_instrumentsdf()
        if df is not None:
            df.to_csv(utils.get_instruments_data_filename())
        else:
            print("Something weird happened here.")

    def fetch_candlesticks(self, pair_name, count, granularity):
        url = f"{defs.OANDA_URL}/instruments/{pair_name}/candles"
        
        params = dict(
            count = count,
            granularity = granularity,
            price="MBA"
        )

        response = self.session.get(url, params=params, headers=defs.SECURE_HEADER)
        return response.status_code, response.json()

if __name__ == "__main__":
    api = OandaAPI()
    res, data = api.fetch_candlesticks("EUR_NOK", 50, "H4")
    api.save_instruments()
    