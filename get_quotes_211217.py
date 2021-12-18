from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from get_picture_211218 import plot_graph


def get_data(rec):
    r = rec.split()
    symb = r[0]
    oper = r[1]
    lot = float(r[2])
    ticket = int(r[3])
    open_price = float(r[4])
    open_time = r[5] + " " + r[6]
    close_price = float(r[7])
    close_time = r[8] + " " + r[9]
    profit = float(r[10])
    try:
        alpha_vantage_key = open("alpha_vantage_key.txt", 'r')
        ts = TimeSeries(key=alpha_vantage_key.readline(), output_format="pandas")
        data, metadata = ts.get_intraday(symbol=symb, interval='30min', outputsize='compact')
        data.rename(columns={"1. open": "Open", "2. high": "High",
                             "3. low": "Low", "4. close": "Close",
                             "5. volume": "Volume"}, inplace=True)
        data.index = data.index + pd.Timedelta('06:30:00')
        df = data[(data.index >= open_time) & (data.index <= close_time)].sort_index()
        plot_graph(df, symb, oper, lot, ticket)
        return ticket
        #mpf.plot(df, type="candle", volume=False)
        # fig, ax = plt.subplots()

    except ValueError:
        print("ValueError")
    pass
