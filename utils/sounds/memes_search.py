import json

from keyboards.inline import memes_generate_buttons
from utils.helpers import send_message, edit_message
from main import search_db
from data.constants import EXPIRE_TIME
from utils.sounds.memes_helper import get_list_memes


async def search_memes_chat(chat_id, memes_type):
    previous_search_db = search_db.get(memes_type)
    if not previous_search_db:
        list_memes_dict = await get_list_memes(memes_type)
        if not list_memes_dict:
            await send_message(chat_id, 'search-result-none', args=memes_type)
            return

        search_db.set(memes_type, json.dumps(list_memes_dict), ex=EXPIRE_TIME)
        previous_search_db = search_db.get(memes_type)

    previous_search_dict = json.loads(previous_search_db)

    audio_markup = await memes_generate_buttons(previous_search_dict, memes_type, 0, is_prev=False)
    text_args = '1', '10', len(previous_search_dict)
    await send_message(chat_id, 'search-result-text', args=text_args, markup=audio_markup, parse='markdown')


async def memes_answer_search_call(chat_id, message_id, request_id, page_number):
    if page_number == '-1':
        return

    previous_search = search_db.get(request_id)
    if previous_search is None:
        return
    search_json = json.loads(previous_search)

    start_from = int(page_number) * 10
    if start_from == 0:
        start_from = 1
    end_from = int(page_number) * 10 + 10

    is_next = True
    if end_from >= len(search_json):
        is_next = False

    is_prev = True
    if start_from == 1:
        is_prev = False

    audio_markup = await memes_generate_buttons(search_json, request_id, int(page_number), is_prev, is_next)
    if not audio_markup:
        return

    text_args = start_from, end_from, len(search_json)
    await edit_message(chat_id, 'search-result-text', message_id, audio_markup, text_args, parse='markdown')
