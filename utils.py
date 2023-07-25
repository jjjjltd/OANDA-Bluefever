def get_hist_data_filename(pair, granularity):
    """ Return pair data by reading csv e.g. ./Data/GBP_JPY_H1  """
    return f"./Data/{pair}_{granularity}.csv"

def get_instruments_data_filename():
    """ Return the path/filename to available instruments file """
    return "./Data/available_instruments.csv"

