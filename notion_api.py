import requests
import config
from datetime import datetime, timedelta
import pandas as pd

allowed_users_dict = config.ALLOWED_USERS_DICT
properties = config.TABLE_PROPERTIES
database_id = config.NOTION_DATABASE_ID
notion_token = config.NOTION_TOKEN
post_url = 'https://api.notion.com/v1/pages'
post_headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': f'Bearer {notion_token}',
        'Notion-Version': '2022-06-28'
    }
default_date = '2030-01-01'


def get_sleep():
    def get_row_value(d: dict) -> str:
        res = ''
        if d['type'] == 'date':
            res = d['date']['start']
        else:
            res = d[d['type']]

        return res

    url = f'https://api.notion.com/v1/databases/{database_id}/query'
    headers = {
        'Authorization': f'Bearer {notion_token}',
        'Notion-Version': '2021-08-16'
    }
    r = requests.post(url, headers=headers)

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

    return data


def post_sleep(props):
    newPageData = {
        'parent': {'database_id': database_id},
        'properties': props
    }

    r = requests.post(url=post_url, headers=post_headers, json=newPageData)

    return r.status_code == 200


def get_last_down_time(user: str, up_date: str) -> int:
    sleep = get_sleep()
    down_date_last = str(datetime.strptime(up_date, '%Y-%m-%d').date() - timedelta(days=1))
    down_time_last = -1
    for row in sleep:
        if row['Дата'] == down_date_last:
            down_time_last = row[f'Лег в ({user})']
            break
    # TODO: если вчера не записал
    return down_time_last


def create_up_props(user: str, up_date: str, up_time: float):
    props = properties.copy()
    down_time_last = get_last_down_time(user, up_date)
    sleep_hours = 24-down_time_last+up_time

    props[f'Встал в ({user})']['number'] = up_time
    props['Дата']['date']['start'] = up_date
    props[f'Спал ({user})']['number'] = sleep_hours

    return props



def up(user_id: int, up_datetime: datetime):
    up_date = up_datetime.date()
    up_time = up_datetime.time()

    up_date = str(up_date)
    up_time = round(up_time.hour + up_time.minute / 60, 1)

    user = ''
    for k, v in allowed_users_dict.items():
        if user_id in v:
            user = k
            break

    props = create_up_props(user, up_date, up_time)
    success = post_sleep(props)
    return success
