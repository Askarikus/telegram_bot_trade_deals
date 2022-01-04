import telebot
import datetime
from pathlib import Path
from time import sleep
from get_quotes_211217 import get_data


def new_picture(bot, chat_id, ticket):
    # отправка рисунка
    if ticket:
        pic = open(f'graph/{ticket}.png', 'rb')
        bot.send_photo(chat_id, pic)
        print(f"send picture {ticket}")
    else:
        print("No picture to send yet")


def new_message(bot, chat_id, record):
    # только отправка сообщения
    bot.send_message(chat_id, record)


if __name__ == "__main__":
    # файл токена содержит токен и chat_id
    with open('telegram_token.txt', 'r') as file_telegram_token:
        # открываем объект бота в самом начале, чтобы не открывать его в цикле
        token, chat_id = file_telegram_token.read().split()
        deals_counter = 0  # объявляем счетчик сделок
        my_bot = telebot.TeleBot(token)
        for i in range(1):  # В РАБОЧЕЙ ВЕРСИИ while True
            dt_now = datetime.datetime.now()
            if 10 < dt_now.second < 59:  # фильтрация по времени, должен проверять не часто, раз в 5 минут
                # первые 10 секунд отводятся для записи файла истории сделок
                path_to_history = Path("/home", "askar", "Python_Proj", "telegram_bot_trade_deals", "history.txt")
                with open(path_to_history, 'r') as file_history_from_mt5, open('storage.txt', 'a+') as file_storage:
                    # файл-хранилище в режиме чтения/добавления
                    file_storage.seek(0)  # в режиме добавления указатель находится в конце файла
                    storage = [line.rstrip('\n') for line in file_storage]
                    history = [line.rstrip('\n') for line in file_history_from_mt5]
                    # записали массивы истории и хранилища, заодно подсчитаем и сравним количество строк
                    if len(history) > len(storage):
                        # если в истории прибавились записи
                        for record in history[:(len(history) - len(storage))]:
                            # для каждой записи, которой нет в хранилище посылаем record через телеграм-бот
                            data = get_data(record)
                            # если возвращается строка, то отправляем как есть
                            if data == record:
                                new_message(my_bot, int(chat_id), record)
                            else:
                                # в случае успешной отрисовки графика
                                new_picture(my_bot, chat_id, data)
                            # записываем в storage
                            print(record, file=file_storage)
                            deals_counter += 1
                            # если с момента запуска прошло 7 сделок, то отправляем пароль
                            if deals_counter > 7:
                                new_message(my_bot, int(chat_id), "password")
                sleep(1)  # В РАБОЧЕЙ ВЕРСИИ параметр 250
