import mplfinance as mpf
from random import choice


def plot_graph(data, symbol, oper, lot, ticket, profit, otime, oprice, ctime, cprice, interval):
    """  тип свечной, случайный выбор стиля графика, figratio - размеры сторон,
         alines  рисует линию сделки, сохранение в файл без вывода на экран
         closefig закрывает график после создания, чтобы не было множественного открытия"""
    title = f'{symbol} {interval} {oper}  {lot}  {profit}'
    styles = ['binance', 'blueskies', 'charles', 'checkers', 'classic', 'default', 'ibd',
              'kenan', 'mike', 'nightclouds', 'sas', 'starsandstripes', 'yahoo']
    try:
        mpf.plot(data, type='candle', style=choice(styles), figratio=(15, 6),
                 alines=dict(alines=[(otime, oprice), (ctime, cprice)], linestyle='-.'),
                 title=title, volume=False, savefig=f'graph/{ticket}.png', closefig=True)

    except TypeError or ValueError:
        print("Can`t plot diagram. Out of range")
