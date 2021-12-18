import telebot
import datetime
from pathlib import Path
from time import sleep
from get_quotes_211217 import get_data


def new_message(bot, message, chat_id):
    # только отправка сообщения
    #bot.send_message(chat_id, message)
    gif = open('demo.gif', 'rb')
    bot.send_animation(chat_id, gif)


if __name__ == "__main__":
    # файл токена содержит токен и chat_id
    with open('telegram_token.txt', 'r') as file_telegram_token:
        # открываем объект бота в самом начале, чтобы не открывать его в цикле
        token, chat_id = file_telegram_token.read().split('\n')
        my_bot = telebot.TeleBot(token.rstrip('\\n'))
        for i in range(2):  # должно быть while True
            dt_now = datetime.datetime.now()
            if 0 < dt_now.second < 59:  # фильтрация по времени, должен проверять не часто, раз в 5 минут
                path_to_history = Path("C:\\", "Users", "Аскар", "AppData", "Roaming", "MetaQuotes",
                                       "Terminal", "Common", "Files", "history.txt")
                with open(path_to_history, 'r') as file_history_from_mt5:
                    storage = []
                    with open('storage.txt', 'r') as file_storage:  # сперва открываем файл-хранилище в режиме чтения
                        storage += [line.rstrip('\n') for line in file_storage]
                        history = [line.rstrip('\n') for line in file_history_from_mt5]
                        # записали массивы истории и хранилища, заодно подсчитаем и сравним количество строк
                        if len(history) > len(storage):  # если в истории прибавились записи
                            for record in history[:(len(history) - len(storage))]:
                                # для каждой записи, которой нет в хранилище
                                # посылаем record через телеграмм-бот
                                # print(get_data(record))
                                new_message(my_bot, record, int(chat_id))
                                # записываем в storage
                                storage.append(record)
                    #  затем все вместе: и то, что изъяли из хранилища до этого и новые записи пишем в файл-хранилище
                    with open('storage.txt', 'w') as file_storage:
                        file_storage.write('\n'.join(storage))
                        # sleep(250)
