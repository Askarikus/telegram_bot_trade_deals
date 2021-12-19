import mplfinance as mpf
from random import choice


def plot_graph(data, symbol, oper, lot, ticket, profit, otime, oprice, ctime, cprice, interval):
    """  тип свечной, случайный выбор стиля графика, figratio[0] если нечетный,
         то пояснение к шкале Y слева, четный - справа, alines  рисует линию сделки,
         сохранение в файл без вывода на экран """
    title = f'{symbol} {interval} {oper} {lot} {profit}'
    styles = ['binance', 'blueskies', 'brasil', 'charles',
                'checkers', 'classic', 'default', 'ibd',
                'kenan', 'mike', 'nightclouds', 'sas',
                'starsandstripes', 'yahoo']
    try:
        mpf.plot(data, type='candle', style=choice(styles), figratio=(15, 5),
                 alines=dict(alines=[(otime, oprice), (ctime, cprice)], linestyle='-.'),
                 title=title, volume=False, savefig=f'{ticket}.png')
    except TypeError:
        print("Can`t plot diagram. Out of range")
