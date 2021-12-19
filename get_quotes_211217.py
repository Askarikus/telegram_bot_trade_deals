from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from get_picture_211218 import plot_graph
from datetime import timedelta
from datetime import datetime


def get_data(rec):
    t_delta = 2  # время отсупа от момента исполнения сделки, в часах
    dt_form = '%Y.%m.%d %H:%M:%S'  # формат преобразования времени
    interval = '15min'  # период построения графика
    time_zone_diff = '06:30:00'

    r = rec.split()
    # распаковка строки в переменные, для удобства по порядку номеров
    symb, oper, lot, ticket = r[0], r[1], float(r[2]), int(r[3])
    open_price = float(r[4])
    open_time = r[5] + " " + r[6]
    close_price = float(r[7])
    close_time = r[8] + " " + r[9]
    profit = float(r[10])
    # время открытия и закрытия берем с отступом указанным в перем. t_delta - получаем границы графика
    left_border = (datetime.strptime(open_time, dt_form) - timedelta(hours=t_delta)).strftime(dt_form)
    right_border = (datetime.strptime(close_time, dt_form) + timedelta(hours=t_delta)).strftime(dt_form)

    try:
        alpha_vantage_key = open("alpha_vantage_key.txt", 'r')
        ts = TimeSeries(key=alpha_vantage_key.readline(), output_format="pandas")
        # делаем выборку по указанному символу(торг. инструменту), 'compact' - скачивается 100 баров
        data, metadata = ts.get_intraday(symbol=symb, interval=interval, outputsize='full')
        data.rename(columns={"1. open": "Open", "2. high": "High", "3. low": "Low",
                             "4. close": "Close", "5. volume": "Volume"}, inplace=True)
        # делаем смещение по времени относительно часового пояса места откуда качаем и откуда берем историю
        data.index = data.index + pd.Timedelta(time_zone_diff)
        # фильтруем нужные бары по ранее определенным границам
        df = data[(data.index >= left_border) & (data.index <= right_border)].sort_index()
        # сохраняем готовый график в папке проекта под именем тикета
        plot_graph(df, symb, oper, lot, ticket, profit, open_time, open_price, close_time, close_price, interval)
        # возвращает номер тикета, он же название файла png
        return ticket
    except ValueError or ConnectionError:
        # если данные в моменте недоступны
        print("Data not available now")
    pass
