from alpha_vantage.timeseries import TimeSeries
import pandas as pd


def get_data(rec):
    symb = rec[0]
    oper = rec[1]
    lot = float(rec[2])
    ticket = int(rec[3])
    open_price = float(rec[4])
    open_time = rec[5] + " " + rec[6]
    close_price = float(rec[7])
    close_time = rec[8] + " " + rec[9]
    profit = float(rec[10])
    try:
        alpha_vantage_key = open("alpha_vantage_key.txt", 'r')
        ts = TimeSeries(key=alpha_vantage_key.readline(), output_format="pandas")
        data, metadata = ts.get_intraday(symbol=symb, interval='15min', outputsize='compact')
        data.rename(columns={"1. open": "Open", "2. high": "High",
                             "3. low": "Low", "4. close": "Close",
                             "5. volume": "Volume"}, inplace=True)
        data.index = data.index + pd.Timedelta('06:30:00')
        df = data[(data.index > open_time) & (data.index < close_time)].sort_index()
        #print(df)
        return df
        #mpf.plot(df, type="candle", volume=False)
        # fig, ax = plt.subplots()

    except ValueError:
        print("ValueError")
    pass
