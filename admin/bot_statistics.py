import json

from main import users_db, bot, files_id


# Function to get bot statistics
from utils.statistics import get_today_statistics


async def bot_statistics_func(chat_id):
    waiting_message = await bot.send_message(chat_id, 'Пожалуйста, подождите')

    statistics_db = files_id.get('STATISTICS')
    if statistics_db is None:
        statistics = {'downloads': 0, 'errors': 0}
    else:
        statistics = json.loads(statistics_db)

    total_downloads = statistics['downloads']

    one_day_statistics = await get_today_statistics()
    today_new = one_day_statistics['new']
    today_downloads = one_day_statistics['download']

    total_downloads += int(today_downloads)

    audios_count = files_id.dbsize()
    users_count = users_db.dbsize()

    admin_text = '*Статистика бота*:\n' \
                 'Пользователей сегодня: *{0:,}*\n' \
                 'Пользователей всего: *{1:,}*\n\n' \
                 'Скачиваний сегодня: *{2:,}*\n' \
                 'Скачиваний всего: *{3:,}*\n' \
                 'Музыки в базе: *{4:,}*'.format(today_new, users_count, today_downloads, total_downloads, audios_count)

    await bot.send_message(chat_id, admin_text, parse_mode='markdown')
    await waiting_message.delete()
