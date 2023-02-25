import requests
import config
from datetime import datetime, timedelta
import pandas as pd

allowed_users_dict = config.ALLOWED_USERS_DICT
properties = config.TABLE_PROPERTIES
database_id = config.NOTION_DATABASE_ID
notion_token = config.NOTION_TOKEN
base_url = 'https://api.notion.com/v1/pages'
base_headers = {
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
    # rows = [row['properties'] for row in result]
    # data = []
    # for row in rows:
    #     row_dict = {}
    #     row_data = list(row.items())
    #     for prop in row_data:
    #         row_dict[prop[0]] = get_row_value(prop[1])
    #     data.append(row_dict)
    #
    # # df = pd.DataFrame.from_dict(data=data)
    # return data

    return result


def get_new_up_props(last_row, user, up_date, up_time):
    props = properties.copy()

    # TODO: down_time_last может быть None
    down_time_last = last_row['properties'][f'Лег в ({user})']['number']
    sleep_hours = 24 - down_time_last + up_time

    props[f'Встал в ({user})']['number'] = up_time
    props['Дата']['date']['start'] = up_date
    props[f'Спал ({user})']['number'] = sleep_hours

    new_page_data = {
        'parent': {'database_id': database_id},
        'properties': props
    }

    return new_page_data


def get_updated_up_props(last_2_rows, user, up_date, up_time):
    props = last_2_rows[0]['properties']

    # TODO: down_time_last может быть None
    down_time_last = last_2_rows[1]['properties'][f'Лег в ({user})']['number']
    sleep_hours = 24 - down_time_last + up_time

    props[f'Встал в ({user})']['number'] = up_time
    props['Дата']['date']['start'] = up_date
    props[f'Спал ({user})']['number'] = sleep_hours

    updated_page_data = {
        'properties': props
    }

    return updated_page_data


def up(user_id: int, up_datetime: datetime):
    method = ''
    url = ''
    payload = ''
    headers = base_headers

    up_date = up_datetime.date()
    up_time = up_datetime.time()

    up_date = str(up_date)
    up_time = round(up_time.hour + up_time.minute / 60, 1)

    user = ''
    for username, ids in allowed_users_dict.items():
        if user_id in ids:
            user = username
            break

    last_2_rows = get_sleep()[:2]
    last_row_date = last_2_rows[0]['properties']['Дата']['date']['start']

    if last_row_date == up_date:
        # Юзер сегодня уже записал время подъема / кол-во часов сна
        if last_2_rows[0]['properties'][f'Встал в ({user})']['number'] is not None or \
                last_2_rows[0]['properties'][f'Спал ({user})']['number'] is not None:
            return False

        # Юзер проснулся вторым
        payload = get_updated_up_props(last_2_rows, user, up_date, up_time)

        row_id = last_2_rows[0]['id']
        url = base_url + f'/{row_id}'
        method = 'PATCH'
    elif last_row_date == str(datetime.strptime(up_date, '%Y-%m-%d').date() - timedelta(days=1)):
        # Юзер проснулся первым
        payload = get_new_up_props(last_2_rows[0], user, up_date, up_time)

        url = base_url
        method = 'POST'
    else:
        # Ошибка. Последняя дата - не сегодня и не вчера, значит бота давно не юзали
        return False

    result = requests.request(method=method, url=url, headers=headers, json=payload)

    return result.status_code == 200
