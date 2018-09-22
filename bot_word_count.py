# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings
import re


root_logger= logging.getLogger()
root_logger.setLevel(logging.INFO)
handler = logging.FileHandler('bot_word_count.log', 'w', 'utf-8')
handler.setFormatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
root_logger.addHandler(handler)


def get_word_count(string):
    if re.match(r"^\'(.|\n)*?\'$", string) or re.match(r"^\"(.|\n)*?\"$", string):
        if len(string) == 2:
            return 0
        else:
            string = string.replace('\n', '').strip('\'').strip('\"')
            if re.match(r"^(\W{,})$", string):
                return 0
            string = " ".join(string.split())
            word_list = string.split(' ')
            return len(word_list)
    else:
        raise Exception("incorrect")


# def get_ending_word(number):
#     if re.match(r"(2|3|4)$", number) and not re.match(r"(12|13|14)$", number):
#         return "слова"
#     elif re.match(r"(1)$", number) and not re.match(r"(11)$", number):
#         return "слово"
#     else:
#         return "слов"


def get_ending_word(number):
    if number[-1] in ["2", "3", "4"] and number[-2:] not in ["12", "13", "14"]:
        return "слова"
    elif number[-1] == "1" and number[-2:] != "11":
        return "слово"
    else:
        return "слов"


def get_answer(message):
    command, text_message = message.strip().split(' ', maxsplit=1)

    try:
        word_count = get_word_count(text_message)

        ending = (get_ending_word(str(word_count)))

        return "{} {}".format(word_count, ending)
    except Exception as err:
        if str(err) == "incorrect":
            return "Сообщение должно быть в ковычках (одного вида)"


def greet_user(bot, update):
    greet_text = "Вызван /start"
    logging.info(greet_text)
    update.message.reply_text(greet_text)


def talk_to_me(bot, update):
    user_text = "Привет {}! Ты написал {}".format(update.message.chat.username, update.message.text)
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                update.message.chat.id, update.message.text)
    update.message.reply_text(user_text)


def talk_word_count(bot, update):
    answer = get_answer(update.message.text)

    logging.info("User: %s, Chat id: %s, Message: %s, Answer: %s", update.message.chat.username,
                update.message.chat.id, update.message.text, answer)

    update.message.reply_text(answer)


def main():
    my_bot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    logging.info("Бот запускается")

    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    dp.add_handler(CommandHandler("wordcount", talk_word_count))

    my_bot.start_polling()
    my_bot.idle()


main()