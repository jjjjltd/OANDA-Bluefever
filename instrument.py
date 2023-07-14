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



if __name__ == "__main__":
    print(Instrument.get_instruments_list())