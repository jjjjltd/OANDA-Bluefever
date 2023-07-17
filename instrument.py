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
        return pd.read_csv(utils.get_instruments_data_filename())
    
    @classmethod
    def get_instruments_list(cls):
        df = cls.get_instruments_df()
        return [Instrument(x) for x in df.to_dict(orient='records')]

    @classmethod
    def get_instruments_dict(cls):
        i_list = cls.get_instruments_list()
        i_keys = [x.ins_name for x in i_list]
        return {k:v for (k, v) in zip(i_keys, i_list)}

    @classmethod
    def get_instrument_by_name(cls, pairname):
        d = cls.get_instruments_dict()

        if pairname in d:
            return d[pairname]
        else:
            return None

if __name__ == "__main__":
    print(Instrument.get_instruments_list())
    for k, v in Instrument.get_instruments_dict().items():
        print(k, v)
    print(Instrument.get_instrument_by_name("AUD_SGD"))