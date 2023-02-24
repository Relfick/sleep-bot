import requests
import config
import pandas as pd

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

properties = {
    'Спал (МАКС)': {
        'number': None
    },
    'Встал в (РОМА)': {
        'number': None
    },
    'Лег в (МАКС)': {
        'number': None
    },
    'Комментарий': {
        'rich_text': []
    },
    'БЕЗ МАТА (МАКСИМ)': {
        'checkbox': False
    },
    'БЕЗ МАТА (РОМА)': {
        'checkbox': False
    },
    'Встал в (МАКС)': {
        'number': None
    },
    'Лег в (РОМА)': {
        'number': None
    },
    'Спал (РОМА)': {
        'number': None
    },
    'Дата': {
        'date': {
            'start': default_date,
            'end': None
        }
    },
    'title': {
        'title': []
    }
}


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

    print(result)


def post_sleep():
    props = properties.copy()


    newPageData = {
        'parent': {'database_id': database_id},
        'properties': props
    }

    r = requests.post(url=post_url, headers=post_headers, json=newPageData)

    return r.status_code


def up()