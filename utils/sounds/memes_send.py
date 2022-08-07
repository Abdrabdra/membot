import json
import os

from keyboards.inline import generate_favourites_markup
from main import files_id, search_db
from utils.statistics import update_statistics
from utils.help_functions import download_audio, check_user_info
from utils.helpers import send_voice

DOWNLOAD_URL = 'https://zvukogram.com/index.php?r=site/download&id={}'


# Function to send only one meme
async def send_one_meme_main(chat_id, memes_type, audio_number):
    await update_statistics('download')

    previous_search_db = search_db.get(memes_type)
    if not previous_search_db:
        return

    previous_search_dict = json.loads(previous_search_db)
    audio_dict = previous_search_dict[audio_number]

    await send_meme_to_user(chat_id, audio_dict)


# Function to send all memes in a page
async def send_page_memes_main(chat_id, memes_type, page_number):
    previous_search_db = search_db.get(memes_type)
    if not previous_search_db:
        return

    previous_search_dict = json.loads(previous_search_db)

    start_number = int(page_number) * 10
    end_number = int(start_number) + 10

    for i, audio_dict in enumerate(previous_search_dict):
        if i in range(start_number, end_number):
            await send_meme_to_user(chat_id, audio_dict)


# Function to send meme to user
async def send_meme_to_user(chat_id, audio_dict):
    user_info = await check_user_info(chat_id)

    audio_id = audio_dict['id']
    audio_title = audio_dict['title']

    audio_download_url = DOWNLOAD_URL.format(audio_id)

    if int(audio_id) not in user_info['memes']:
        add_remove_meme_markup = await generate_favourites_markup(audio_id, 'add_meme')
    else:
        add_remove_meme_markup = await generate_favourites_markup(audio_id, 'remove_meme')

    # Check if there is a voice file id
    meme_info_db = files_id.get(audio_id)
    if meme_info_db is not None:
        mem_info = json.loads(meme_info_db)
        meme_file_id = mem_info['file_id']

        await send_voice(chat_id, str(meme_file_id, 'utf-8'), markup=add_remove_meme_markup)
        return

    audio_dir = await download_audio(audio_download_url, audio_title)
    sent_voice_id = await send_voice(chat_id, open(audio_dir, 'rb'), markup=add_remove_meme_markup)
    os.remove(audio_dir)

    # Save audio file id to db
    if sent_voice_id is not None:
        mem_info_id = {'file_id': sent_voice_id, 'title': audio_title}
        files_id.set(audio_id, json.dumps(mem_info_id))
