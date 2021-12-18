import mplfinance as mpf
from random import choice


def plot_graph(data, symbol, oper, lot, ticket, profit, otime, oprice, ctime, cprice):
    """ случайный выбор стиля графика, тип свечной, сохранение в файл без вывода на экран
    параметр figratio[0] если нечетный, то пояснение к шкале y слева, четный - справа"""
    title = symbol + ' ' + oper + ' ' + str(lot) + ' ' + str(profit)
    styles = ['binance', 'blueskies', 'brasil', 'charles',
                'checkers', 'classic', 'default', 'ibd',
                'kenan', 'mike', 'nightclouds', 'sas',
                'starsandstripes', 'yahoo']
    try:
        mpf.plot(data, type='candle', style=choice(styles), figratio=(15, 5), alines=[(otime, oprice), (ctime, cprice)],
             title=title, volume=False, savefig=f'{ticket}.png')
    except TypeError:
        print("Can`t plot diagram. Out of range")

