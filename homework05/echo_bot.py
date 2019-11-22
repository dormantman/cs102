import telebot
from telebot import apihelper

import config

bot = telebot.TeleBot(config.access_token)

apihelper.proxy = config.proxy


@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
