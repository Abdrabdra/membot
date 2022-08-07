import json
from uuid import uuid4

from aiogram.types import InlineQueryResultCachedVoice

from utils.help_functions import check_user_info
from utils.helpers import answer_inline_query
from main import files_id, users_mem_db


async def memes_search_inline(chat_id, query_id):
    user_info = await check_user_info(chat_id)
    list_user_favourite_memes = user_info['memes']

    results = []
    for i, audio_id in enumerate(list_user_favourite_memes):
        if i == 45:
            break

        music_info_db = files_id.get(audio_id)
        if music_info_db is None:
            music_info_db = users_mem_db.get(audio_id)

        if music_info_db is not None:
            music_info = json.loads(music_info_db)
            voice_file_id = music_info['file_id']
            voice_title = music_info['title']
            result_id = str(uuid4())

            result = InlineQueryResultCachedVoice(id=result_id, voice_file_id=voice_file_id, title=voice_title,
                                                  caption='Больше прикольных звуков в @memsoundsbot')

            results.append(result)

    await answer_inline_query(query_id, results, cache_time=10)
