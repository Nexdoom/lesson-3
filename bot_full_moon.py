# -*- coding: utf-8 -*-



from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings
import ephem
import datetime


root_logger= logging.getLogger()
root_logger.setLevel(logging.INFO)
handler = logging.FileHandler('bot_astro.log', 'w', 'utf-8')
handler.setFormatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
root_logger.addHandler(handler)


def greet_user(bot, update):
    greet_text = "Вызван /start"
    logging.info(greet_text)
    update.message.reply_text(greet_text)


def get_constellation(message_text):
    try:
        command, planet = message_text.strip().split(' ')
    except(ValueError):
        return "Укажи только одну планету"

    planet = planet.title()

    try:
        planet_object = getattr(ephem,planet)(datetime.datetime.now())
    except(AttributeError):
        return "Такой планеты нет"

    return ephem.constellation(planet_object)


def talk_to_me(bot, update):
    user_text = "Привет {}! Ты написал {}".format(update.message.chat.username, update.message.text)
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                update.message.chat.id, update.message.text)
    update.message.reply_text(user_text)


def talk_constellation(bot, update):
    constellation = get_constellation(update.message.text)

    text = "{}".format(constellation)
    logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,
                update.message.chat.id, update.message.text)
    update.message.reply_text(text)


def main():
    my_bot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    logging.info("Бот запускается")

    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    dp.add_handler(CommandHandler("planet", talk_constellation))

    my_bot.start_polling()
    my_bot.idle()


main()