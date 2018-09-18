# -*- coding: utf-8 -*-
 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings
import re
 

root_logger= logging.getLogger()
root_logger.setLevel(logging.INFO)
handler = logging.FileHandler('bot_calculator.log', 'w', 'utf-8')
handler.setFormatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
root_logger.addHandler(handler)
 

def get_sum(num_list):
    return sum(num_list)


def get_dif(num_list):
    return num_list[0] - num_list[1]


def get_mul(num_list):
    return num_list[0] * num_list[1]


def get_div(num_list):
    return num_list[0] / num_list[1]


def get_result(text_message):
    text_message = text_message.replace(" ", '')

    try:
        if re.match(r"^\d{,}\.{,1}\d{,}(\+|\-|\*|\/)\d{,}\.{,1}\d{,}\=$", text_message):
            text_message = text_message.replace("=", '')
            if '+' in text_message:
                num_list = [float(num) for num in text_message.split('+')]
                return get_sum(num_list)
            elif '-' in text_message:
                num_list = [float(num) for num in text_message.split('-')]
                return get_dif(num_list)
            elif '*' in text_message:
                num_list = [float(num) for num in text_message.split('*')]
                return get_mul(num_list)
            elif '/' in text_message:
                num_list = [float(num) for num in text_message.split('/')]
                return get_div(num_list)
            else:
                print(text_message)
        else:
            return "Неверная форма записи. Пример: 22/11="
    except ZeroDivisionError:
        return "На ноль делить нельзя"
    except OverflowError:
        return "Результат слишком велик"


def greet_user(bot, update):
    greet_text = "Вызван /start"
    logging.info(greet_text)
    update.message.reply_text(greet_text)


def talk_calculator(bot, update):
    result = get_result(update.message.text)
    logging.info("User: %s, Chat id: %s, Message: %s, Result: %s", update.message.chat.username,
                update.message.chat.id, update.message.text, result)
    update.message.reply_text(result)


def main():
    my_bot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    logging.info("Бот запускается")

    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_calculator))

    my_bot.start_polling()

    my_bot.idle()
 

main()



