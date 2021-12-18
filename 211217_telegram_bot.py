import telebot
import datetime
from pathlib import Path
from time import sleep
from get_quotes_211217 import get_data


def new_message(bot, chat_id, ticket):
    # только отправка сообщения
    # bot.send_message(chat_id, message)
    pic = open(f'{ticket}.png', 'rb')
    bot.send_photo(chat_id, pic)


if __name__ == "__main__":
    # файл токена содержит токен и chat_id
    with open('telegram_token.txt', 'r') as file_telegram_token:
        # открываем объект бота в самом начале, чтобы не открывать его в цикле
        token, chat_id = file_telegram_token.read().split()
        my_bot = telebot.TeleBot(token)
        for i in range(2):  # должно быть while True
            dt_now = datetime.datetime.now()
            if 0 < dt_now.second < 59:  # фильтрация по времени, должен проверять не часто, раз в 5 минут
                path_to_history = Path("C:\\", "Users", "Аскар", "AppData", "Roaming", "MetaQuotes",
                                       "Terminal", "Common", "Files", "history.txt")
                with open(path_to_history, 'r') as file_history_from_mt5:
                    with open('storage.txt', 'a+') as file_storage:  # файл-хранилище в режиме чтения/добавления
                        file_storage.seek(0)  # в режиме добавления указатель находится в конце файла
                        storage = [line.rstrip('\n') for line in file_storage]
                        history = [line.rstrip('\n') for line in file_history_from_mt5]
                        # записали массивы истории и хранилища, заодно подсчитаем и сравним количество строк
                        if len(history) > len(storage):  # если в истории прибавились записи
                            for record in history[:(len(history) - len(storage))]:
                                # для каждой записи, которой нет в хранилище
                                # посылаем record через телеграмм-бот
                                #print(get_data(record))
                                new_message(my_bot, int(chat_id), get_data(record))
                                # записываем в storage
                                print(record, file=file_storage)
                sleep(250)
