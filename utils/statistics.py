import csv
import json
import os
from datetime import date

from utils.helpers import send_document
from main import files_id
from data.constants import STATS_GROUP_ID, BOT_USERNAME, ONE_DAY_STAT

current_date = str(date.today())
one_day_statistics = ONE_DAY_STAT


async def update_statistics(action):
    global current_date
    global one_day_statistics

    today_date = str(date.today())

    one_day_statistics[action] += 1

    if current_date != today_date:
        # Send bot and views statistics
        stat_date = current_date
        await send_day_statistics(stat_date)

        # Update date and views
        current_date = str(today_date)
        one_day_statistics = ONE_DAY_STAT


async def send_day_statistics(stat_date):
    file_name = await get_today_statistics_file(stat_date)
    await send_document(STATS_GROUP_ID, file_name, current_date)
    os.remove(file_name)

    # Update statistics
    statistics_db = files_id.get('STATISTICS')
    if statistics_db is None:
        statistics = {'downloads': 0, 'errors': 0}
    else:
        statistics = json.loads(statistics_db)

    statistics['downloads'] += one_day_statistics['download']
    statistics['errors'] += one_day_statistics['error']

    files_id.set('STATISTICS', json.dumps(statistics))


async def get_today_statistics_file(date_to_get):
    file_name = f'{date_to_get} {BOT_USERNAME}.csv'
    with open(file_name, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Язык пользователя', 'Новых пользователей', 'Скачиваний', 'Ошибок'])

        list_data = []
        for one_lang in ['ru']:
            list_data.append(one_lang)
            for one_action in ['new', 'download', 'error']:
                action_stat = one_day_statistics[one_action]
                list_data.append(action_stat)

            writer.writerow(list_data)
            list_data = []

    return file_name


async def get_today_statistics():
    return one_day_statistics
