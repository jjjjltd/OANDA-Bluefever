import pandas as pd
import xlsxwriter

def add_pair_charts(ma_test_res, all_trades, writer=None):
    cols = ["time", "CUM_GAIN"]
    df_temp = ma_test_res.drop_duplicates(subset=["pair"])
    # print(df_temp.head(10))

    # For each (de-duplicated) index, return columns of interest for each row
    for index, row in df_temp.iterrows():
        # print("index", index)
        # print("row", row.CROSS, row.pair)
        temp_all_trades = df_temp[(df_temp.CROSS==row.CROSS) & (df_temp.pair==row.pair) ].copy()
        print(temp_all_trades.info())
        temp_all_trades["CUM_GAIN"] = temp_all_trades.total_gain.cumsum()
        temp_all_trades[cols].to_excel(writer, sheet=row.pair, startrow=0, startcol=7)

def add_pair_sheets(ma_test_res, writer):
    for p in ma_test_res.pair.unique():
        temp_df = ma_test_res[ma_test_res.pair==p]
        temp_df.to_excel(writer, sheet_name=p, index=False)

def create_excel(ma_test_res, all_trades):
    filename = "./Data/ma_results.xlsx"
    writer = pd.ExcelWriter(filename, engine="xlsxwriter")


    ma_test_res = ma_test_res[['pair', 'num_trades', 'total_gain', 'mashort', 'malong']]
    ma_test_res["CROSS"] = "MA_" + ma_test_res.mashort.map(str) + "_" + ma_test_res.malong.map(str)
    ma_test_res.sort_values(by=["pair", "total_gain"], ascending=[True, False], inplace=True)

    all_trades["CROSS"] = "MA_" + all_trades.MASHORT.map(str) + "_" + all_trades.MALONG.map(str)
    all_trades["time"] = pd.to_datetime(all_trades.time)
    
    all_trades["time"] = [x.replace(tzinfo=None) for x in all_trades.time]
    add_pair_sheets(ma_test_res, writer)
    add_pair_charts(ma_test_res, all_trades, writer)

    writer.save()

if __name__ == "__main__":
    ma_test_res = pd.read_csv("./Data/ma_test_results.csv")
    all_trades = pd.read_csv("./Data/All Trades.csv")
    create_excel(ma_test_res, all_trades)

    # 2m10