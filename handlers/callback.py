from aiogram.types import CallbackQuery

from keyboards.inline import generate_favourites_markup
from main import dp
from utils.help_functions import save_favourite_memes
from utils.sounds.memes_search import memes_answer_search_call
from utils.sounds.memes_send import send_page_memes_main, send_one_meme_main


# Answer to delete called button
@dp.callback_query_handler(text='delete', chat_type='private')
async def delete_callback(call: CallbackQuery):
    await call.message.delete()


# Ответ на нажатие кнопки
@dp.callback_query_handler(lambda call: True)
@dp.throttled(rate=1)
async def call_back_message(call: CallbackQuery):
    await call.answer()

    chat_id = call.message.chat.id
    message_id = call.message.message_id
    call_data = str(call.data)

    split_data = str(call_data).split('!')
    method = split_data[0]
    meme_type = split_data[1]
    audio_id_or_page_number = int(split_data[2])

    if method == 'search':
        await memes_answer_search_call(chat_id, message_id, meme_type, audio_id_or_page_number)

    elif method == 'tracks':
        await send_one_meme_main(chat_id, meme_type, audio_id_or_page_number)

    elif method == 'tracksall':
        await send_page_memes_main(chat_id, meme_type, audio_id_or_page_number)

    elif method in ['add_meme', 'remove_meme']:
        await save_favourite_memes(chat_id, method, audio_id_or_page_number)

        if method == 'add_meme':
            generated_markup = await generate_favourites_markup(audio_id_or_page_number, 'remove_meme')
        else:
            generated_markup = await generate_favourites_markup(audio_id_or_page_number, 'add_meme')

        await call.message.edit_reply_markup(generated_markup)
