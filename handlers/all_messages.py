from aiogram.types import Message

from main import dp
from utils.helpers import send_message
from utils.help_functions import check_user_info
from utils.sounds.memes_search import search_memes_chat
from keyboards.inline import favourite_memes_markup


@dp.message_handler()
@dp.throttled(rate=1)
async def all_messages(message: Message):
    user_message = message.text
    chat_id = message.chat.id

    await check_user_info(chat_id)

    if user_message == '❤️ Избранные звуки':
        await send_message(chat_id, 'favourite', markup=favourite_memes_markup)
        return

    # elif user_message == '🔎 Поиск звуков':
    #     await send_message(chat_id, 'search-memes')
    #     return

    elif user_message == '🕺 Звуки из TikTok':
        memes_type = 'TIKTOK_MEMES'

    elif user_message == '💃 Звуки из Reels':
        memes_type = 'REELS_MEMES'

    elif user_message == '🔊 Популярные звуки':
        memes_type = 'POPULAR_MEMES'

    else:
        memes_type = 'POPULAR_MEMES'
        # memes_type = user_message

    await search_memes_chat(chat_id, memes_type)
