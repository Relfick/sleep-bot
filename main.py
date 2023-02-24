import telebot
import json
import config
from telebot.types import *
from Filters.IsAllowedUserFilter import IsAllowedUserFilter

bot_token = config.BOT_TOKEN
allowed_users = config.ALLOWED_USERS
allowed_chats = config.ALLOWED_CHATS
# allowed_chats += allowed_users


def main():
    telebot.apihelper.ENABLE_MIDDLEWARE = True

    bot = telebot.TeleBot(bot_token)
    bot.set_my_commands([
        BotCommand('start', 'Старт'),
        BotCommand('down', 'Лёг'),
        BotCommand('up', 'Встал')
    ])

    @bot.message_handler(chats_and_admins=(allowed_chats, allowed_users), commands=['start'])
    def send_welcome(message: Message):
        chat_id = message.chat.id
        bot.send_message(chat_id, 'hello boy')


    @bot.message_handler(chats_and_admins=(allowed_chats, allowed_users), content_types=['text'])
    def get_text_message(message: Message):
        msg_text = message.text
        chat_id = message.chat.id
        print(chat_id)
        bot.send_message(chat_id, 'abiba aboba')


    bot.add_custom_filter(IsAllowedUserFilter())

    bot.polling(none_stop=True, interval=0, skip_pending=True)
    # post_sleep()



main()