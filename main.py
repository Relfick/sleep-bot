import telebot
import json
import requests
import pandas as pd
import config
from telebot.types import *
from Filters.IsAllowedUserFilter import IsAllowedUserFilter


database_id = config.NOTION_DATABASE_ID
notion_token = config.NOTION_TOKEN
bot_token = config.BOT_TOKEN
allowed_users = config.ALLOWED_USERS
allowed_chats = config.ALLOWED_CHATS
# allowed_chats += allowed_users

def get_sleep():
    def get_row_value(d: dict) -> str:
        res = ''
        if d['type'] == 'date':
            res = d['date']['start']
        else:
            res = d[d['type']]

        return res


    url = f'https://api.notion.com/v1/databases/{database_id}/query'
    r = requests.post(url, headers={
        'Authorization': f'Bearer {notion_token}',
        'Notion-Version': '2021-08-16'
    })

    result = r.json()['results']
    rows = [row['properties'] for row in result]
    data = []
    for row in rows:
        row_dict = {}
        row_data = list(row.items())
        for prop in row_data:
            row_dict[prop[0]] = get_row_value(prop[1])
        data.append(row_dict)

    # df = pd.DataFrame.from_dict(data=data)

    print(result)


def post_sleep():
    url = f'https://api.notion.com/v1/pages'
    newPageData = {
        'parent': {'database_id': database_id},
        'properties': {
            'Спал (МАКС)': {
                'number': 5
            },
            'Встал в (РОМА)': {
                'number': 5
            },
            'Лег в (МАКС)': {
                'number': 5
            },
            'Комментарий': {
                'rich_text': []
            },
            'БЕЗ МАТА (МАКСИМ)': {
                'checkbox': True
            },
            'БЕЗ МАТА (РОМА)': {
                'checkbox': True
            },
            'Встал в (МАКС)': {
                'number': 5
            },
            'Лег в (РОМА)': {
                'number': 5
            },
            'Спал (РОМА)': {
                'number': 5
            },
            'Дата': {
                'date': {
                    'start': '2023-02-26',
                    'end': None
                }
            },
            'title': {
                'title': []
            }
        }
    }

    r = requests.post(url, headers={
        'accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': f'Bearer {notion_token}',
        'Notion-Version': '2022-06-28'
    }, json=newPageData)

    return r.status_code


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