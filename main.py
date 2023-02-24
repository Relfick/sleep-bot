import telebot
from datetime import datetime
import json
import config
import notion_api
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


    @bot.message_handler(chats_and_admins=(allowed_chats, allowed_users), commands=['up'])
    def post_up(up_msg: Message):
        user_id = up_msg.from_user.id
        try_msg = bot.reply_to(message=up_msg, text='Пытаюсь добавить...')
        up_datetime = datetime.fromtimestamp(up_msg.date)

        up_date = up_datetime.date()
        up_time = up_datetime.time()

        up_date = str(up_date)
        up_time = round(up_time.hour + up_time.minute/60, 1)

        success = notion_api.up(user_id, up_datetime)
        if not success:
            bot.delete_message(up_msg.chat.id, try_msg.id)
            bot.reply_to(message=up_msg, text='Не удалось добавить!')
        else:
            bot.delete_message(up_msg.chat.id, try_msg.id)
            bot.delete_message(up_msg.chat.id, up_msg.id)
        print()


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