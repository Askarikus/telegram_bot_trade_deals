import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
import mplfinance as mpf


def plot_graph(data, symbol, oper, lot, ticket):
    title = symbol + ' ' + oper + ' ' + str(lot)
    mpf.plot(data, type='candle', style='mike', title=title, volume=False, savefig=f'{ticket}.png')



