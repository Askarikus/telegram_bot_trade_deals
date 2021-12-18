from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from get_picture_211218 import plot_graph
from datetime import timedelta
from datetime import datetime


def get_data(rec):
    t_delta = 2  # время в часах отсупа от времени исполнения сделки
    dt_form = '%Y.%m.%d %H:%M:%S'  # формат преобразования времени
    r = rec.split()
    # распаковка строки в переменные, для удобства по порядку номеров
    symb, oper, lot, ticket = r[0], r[1], float(r[2]), int(r[3])
    open_price = float(r[4])
    open_time = r[5] + " " + r[6]
    # время открытия и закрытия берем с отступом указанным в перем. t_delta - получаем границы графика
    left_border = (datetime.strptime(open_time, dt_form) - timedelta(hours=t_delta)).strftime(dt_form)
    close_price = float(r[7])
    close_time = r[8] + " " + r[9]
    right_border = (datetime.strptime(close_time, dt_form) + timedelta(hours=t_delta)).strftime(dt_form)
    profit = float(r[10])

    try:
        alpha_vantage_key = open("alpha_vantage_key.txt", 'r')
        ts = TimeSeries(key=alpha_vantage_key.readline(), output_format="pandas")
        # делаем выборку по указанному symb, по умолчанию скачивается 100 баров
        data, metadata = ts.get_intraday(symbol=symb, interval='60min', outputsize='compact')
        data.rename(columns={"1. open": "Open", "2. high": "High",
                             "3. low": "Low", "4. close": "Close",
                             "5. volume": "Volume"}, inplace=True)
        # делаем смещение по времени для учета часового пояса места откуда качаем и откуда берем историю
        data.index = data.index + pd.Timedelta('06:30:00')
        # фильтруем нужные бары по ранее определенным границам
        df = data[(data.index >= left_border) & (data.index <= right_border)].sort_index()
        plot_graph(df, symb, oper, lot, ticket, profit, open_time, open_price, close_time, close_price)
        # возвращает номер тикета, он же название файла png
        return ticket
    except ValueError:
        # если данные в моменте недоступны
        print("ValueError")
    pass
