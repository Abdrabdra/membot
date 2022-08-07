import csv
import os

from data.constants import BOT_USERNAME
from main import users_db, bot
from utils.helpers import wrap


async def backup_database_func(chat_id):
    waiting_message = await bot.send_message(chat_id, 'Пожалуйста, подождите...')

    file_name = await get_files()

    with open(file_name, 'rb') as file_to_send:
        await bot.send_document(chat_id, file_to_send)

    os.remove(file_name)

    await bot.delete_message(chat_id, waiting_message.message_id)


@wrap
def get_files():
    list_users_id = users_db.keys()

    file_name = '{} all users id.csv'.format(BOT_USERNAME)

    with open(file_name, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        for user_id in list_users_id:
            str_user_id = str(user_id, 'utf-8')
            if not str_user_id.isdigit():
                continue

            writer.writerow([str_user_id])

    return file_name
