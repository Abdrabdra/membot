import json

import aiohttp

from utils.helpers import send_message
from main import users_db
from data.constants import ADMINS_ID, USER_FIRST_INFO
from utils.statistics import update_statistics


async def check_user_info(chat_id):
    user_info_db = users_db.get(chat_id)
    if user_info_db is not None and str(user_info_db, 'utf-8') != 'None':
        user_info = json.loads(user_info_db)
        return user_info
    else:
        await update_statistics('new')
        users_db.set(chat_id, json.dumps(USER_FIRST_INFO))

        return USER_FIRST_INFO


# Send notification that bot started working
async def on_startup(args):  # send errors to admin
    for one_admin_id in ADMINS_ID:
        await send_message(one_admin_id, 'admin-bot-started')


# Function to download video or audio
async def download_audio(url_to_download, file_name):
    file_directory = 'music/{}.mp3'.format(file_name)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url_to_download) as get_video:
                with open(file_directory, "wb") as file_stream:
                    video_url_content = await get_video.content.read()
                    file_stream.write(video_url_content)

                return file_directory

    except Exception as err:
        print(err, '[ERROR] in download_file')

    return None


async def save_favourite_memes(chat_id, method, audio_id):
    user_info = await check_user_info(chat_id)
    list_user_favourite_memes = user_info['memes']

    if method == 'remove_meme':
        if audio_id in list_user_favourite_memes:
            list_user_favourite_memes.remove(audio_id)
    else:
        if audio_id not in list_user_favourite_memes:
            list_user_favourite_memes.append(audio_id)

    user_info['memes'] = list_user_favourite_memes
    users_db.set(chat_id, json.dumps(user_info))


