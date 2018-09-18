# -*- coding: utf-8 -*-
 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings
import re
import ephem
 

root_logger= logging.getLogger()
root_logger.setLevel(logging.INFO)
handler = logging.FileHandler('bot_full_moon.log', 'w', 'utf-8')
handler.setFormatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
root_logger.addHandler(handler)
 

def get_date(text):
    if re.match(r"Когда ближайшее полнолуние после \d{4}-\d{2}-\d{2}\?", text):
        text_list = text.strip().split()
        date = text_list[-1].replace('?', '').split('-')
        return "{}/{}/{}".format(date[0], date[1], date[2])
    else:
        raise Exception("incorrect")


def get_full_moon(text_message):
    try:
        date = get_date(text_message)
        return ephem.next_full_moon(date)
    except Exception as err:
        if str(err) == "incorrect":
            return "Пиши вопрос ввиде: \"Когда ближайшее полнолуние после yyyy-mm-dd?\""


def greet_user(bot, update):
    greet_text = "Вызван /start"
    logging.info(greet_text)
    update.message.reply_text(greet_text)


def talk_full_moon(bot, update):
    answer = get_full_moon(update.message.text)
    logging.info("User: %s, Chat id: %s, Message: %s, Answer: %s", update.message.chat.username,
                update.message.chat.id, update.message.text, answer)
    update.message.reply_text(answer)


def main():
    my_bot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    logging.info("Бот запускается")

    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_full_moon))

    my_bot.start_polling()

    my_bot.idle()
 

main()