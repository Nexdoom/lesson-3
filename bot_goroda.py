# -*- coding: utf-8 -*-
# Правила игры взять из Вики:
# https://ru.wikipedia.org/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D0%B0_(%D0%B8%D0%B3%D1%80%D0%B0)

 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings
import csv
import random
import re

CITIES_LIST=[]

root_logger= logging.getLogger()
root_logger.setLevel(logging.INFO)
handler = logging.FileHandler('bot_goroda.log', 'w', 'utf-8')
handler.setFormatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
root_logger.addHandler(handler)


def greet_user(bot, update):
    with open('cities_ru_en.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            CITIES_LIST.append(row[0]) # в файле две колонки: рус и англ версия
        random.shuffle(CITIES_LIST)


    greet_text = "Игра начата, напиши команду /goroda и город"
    logging.info(greet_text)
    update.message.reply_text(greet_text)


def take_user_turn(city):
    CITIES_LIST.remove(city)
    last_letter = city[-1]
    if last_letter == 'ь' or last_letter == 'ъ' or last_letter == 'ы' or last_letter == 'й':
        last_letter = city[-2]  # по правилам если мягкий или твердый знак, то берем предпоследнюю букву
    return last_letter.upper()


def get_bot_turn(first_letter):
    for city in CITIES_LIST:
        if city[0] == first_letter:
            CITIES_LIST.remove(city)
            return "\"{}\" - \"{}\", ваш ход".format(first_letter.lower(), city)
    return "Ты победил"


def goroda_hadler(text_message):
    try:
        text_message = re.sub(' +', ' ', text_message)
        command, city = text_message.strip().split(' ', 1)
        city = city.title()
    except ValueError:
        return "Вы не указали город"

    try:
        last_letter = take_user_turn(city)
        answer = get_bot_turn(last_letter)
        return answer
    except ValueError:
        return "Ты проиграл, жми /start что бы начать заного"


def give_answer(bot, update):
    text_message = update.message.text

    answer = goroda_hadler(text_message)

    logging.info("User: %s, Chat id: %s, Message: %s, Answer: %s", update.message.chat.username,
                update.message.chat.id, update.message.text, answer)
    update.message.reply_text(answer)


def main():
    my_bot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    logging.info("Бот запускается")

    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("goroda", give_answer))

    my_bot.start_polling()

    my_bot.idle()

main()