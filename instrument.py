import pandas as pd
import utils

class Instrument():
    
    def __init__(self, obj):
        self.ins_name           = obj["name"]
        self.ins_type           = obj["type"]
        self.ins_displayName    = obj["displayName"]
        self.ins_pipLocation    = pow(10, obj["pipLocation"])
        self.ins_marginRate     = obj["marginRate"]

    def __repr__(self):
        return str(vars(self))

    @classmethod
    def get_instruments_df(cls):
        """ Return DataFrame of instruments data e.g. from GBP_JPY_H1 """
        return pd.read_csv(utils.get_instruments_data_filename())
    
    @classmethod
    def get_instruments_list(cls):
        df = cls.get_instruments_df()
        """ Convert list of instruments into a dictionary, and return.  """
        return [Instrument(x) for x in df.to_dict(orient='records')]

    @classmethod
    def get_instruments_dict(cls):
        """ Return dictionary definition of instrument e.g. 
        {'ins_name': 'GBP_JPY', 'ins_type': 'CURRENCY', 'ins_displayName': 'GBP/JPY', 'ins_pipLocation': 0.01, 'ins_marginRate': 0.03333333333333}  """
        i_list = cls.get_instruments_list()
        i_keys = [x.ins_name for x in i_list]
        return {k:v for (k, v) in zip(i_keys, i_list)}

    @classmethod
    def get_instrument_by_name(cls, pairname):
        """  Receive pairname, return all data for pairname.  """
        d = cls.get_instruments_dict()

        if pairname in d:
            return d[pairname]
        else:
            return None

    @classmethod    
    def get_pairs_from_string(cls, pair_str):
        """  Receive string of individual currencies, pair up and check if they are available instruments.    """
        existing_pairs = cls.get_instruments_dict().keys()
        pairs = pair_str.split(",")

        pair_list = []

        # Loop through pairs list twice (each currency within each currency)
        for p1 in pairs:
            for p2 in pairs:
                p = f"{p1}_{p2}"
                if p in existing_pairs:
                    pair_list.append(p)

        return pair_list

if __name__ == "__main__":
    # print(Instrument.get_instruments_list())
    # for k, v in Instrument.get_instruments_dict().items():
    #     print(k, v)
    # print(Instrument.get_instrument_by_name("AUD_SGD"))
    print(Instrument.get_pairs_from_string("GBP,EUR,USD,CAD"))