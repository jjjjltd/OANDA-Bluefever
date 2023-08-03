import pandas as pd
import plotly.graph_objects as go
import utils

def plot_candles(df_plot):

    plot_cols = ['ENTRY', 'STOPLOSS', 'TAKEPROFIT']
    plot_colours_buy = ['#043ef9', '#eb5334', '#34eb37']
    plot_colours_sell = ['white', 'red', 'yellow']

    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df_plot.time, open=df_plot.mid_o, high=df_plot.mid_h, low = df_plot.mid_l, close=df_plot.mid_c,
        line=dict(width=1), opacity=1,
        increasing_fillcolor="#24A06B",
        decreasing_fillcolor="#CC2E3C",
        increasing_line_color="#2EC886",
        decreasing_line_color="#FF3A4C"
        ))

    # Loop through buys, and plot
    for i in range(0, 3):
        fig.add_trace(go.Scatter(
            x=df_buys.time,
            y=df_buys[plot_cols[i]],
            mode='markers',
            name=(f"Buy {plot_cols[i]}"),
            marker=dict(color=plot_colours_buy[i], size=12),
            
        ))

    # Loop through sells and plot
    for i in range(0, 3):
        fig.add_trace(go.Scatter(
            x=df_sells.time,
            y=df_sells[plot_cols[i]],
            mode='markers',
            name=(f"Sell {plot_cols[i]}"),
            marker=dict(color=plot_colours_sell[i], size=12)
        ))


    fig.update_layout(width=1000, height=400, paper_bgcolor = "#1e1e1e", plot_bgcolor = "#1e1e1e",
                    margin=dict(l=10, b=10, t=10, r=10), 
                    font=dict(size=10, color="#e1e1e1"))
    fig.update_xaxes(gridcolor="#1f292f",
                    showgrid=True,
                    fixedrange=True,
                    rangeslider=dict(visible=False),
                    rangebreaks=[
                        dict(bounds=["sat", "mon"])
                        ]
                    )
    fig.update_yaxes(gridcolor="#1f292f",
                    showgrid=True)

    fig.show


def direction(row):
    """ Return price direction based on close vs open price i.e. if close higher, upwards (1)..."""
    if row.mid_c > row.mid_o:
        return 1
    return -1

def get_signal(row):
    """  Identify encapsulation in previous candle and return direction.  Pass back zero if no encapsulation.  
    1 = Buy, -1=Sell:  Buy if encapsulated in a previously upward candle...      """
    if row.mid_h_prev > row.mid_h and row.mid_l_prev > row.mid_l:
        return row.DIRECTION_prev
    return 0

def get_entry_stop(row):
    if row.SIGNAL == 1:
        return (row.RANGE_prev * ENTRY_PRC) + row.mid_h_prev
    elif row.SIGNAL == -1:
        return row.mid_l_prev - (row.RANGE_prev * ENTRY_PRC)
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

pair = "USD_JPY"
granularity = "H4"

SLOSS = 0.4
TPROFIT = 0.8
ENTRY_PRC = 0.1


df_raw = pd.read_csv(utils.get_hist_data_filename(pair, granularity))


df = df_raw[['ticker', 'time', 'mid_o', 'mid_h', 'mid_l', 'mid_c', 'ask_c']].copy()
df['RANGE'] = df.mid_h - df.mid_l
df['mid_h_prev'] = df.mid_h.shift(1)
df['mid_l_prev'] = df.mid_l.shift(1)
df['RANGE_prev'] = df.RANGE.shift(1)
df['DIRECTION'] = df.apply(direction, axis=1)
df['DIRECTION_prev'] = df.DIRECTION.shift(1).fillna(0).astype(int)
df.dropna(inplace=True)
df['SIGNAL'] = df.apply(get_signal, axis=1)
df.reset_index(drop=True, inplace=True)

df['ENTRY'] = df.apply(get_entry_stop, axis=1)
df['STOPLOSS'] = df.apply(get_stop_loss, axis=1)
df['TAKEPROFIT'] = df.apply(get_take_profit, axis=1)

df_plot = df.iloc[0:60]
print(df_plot.head())
df_buys = df_plot[df_plot.SIGNAL == 1]
df_sells = df_plot[df_plot.SIGNAL == -1]
plot_candles(df_plot)