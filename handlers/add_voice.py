import json
import random

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from data.messages.admin import REJECT_MSG
from keyboards.inline import favourite_memes_markup
from main import dp, bot, UserAddVoice, users_mem_db
from utils.help_functions import save_favourite_memes
from keyboards.buttons import reject_markup, sure_markup, admin_markup


# Handler to receive add voice message
@dp.message_handler(text='🎧 Добавить свой звук')
async def add_user_voice(message: Message):
    admin_text = 'Пришлите ваше голосовое сообщение в этот чат, для того, чтобы добавить его в список'
    await bot.send_message(message.chat.id, admin_text, reply_markup=reject_markup)
    await UserAddVoice.ask_voice.set()


# Handler to receive reject message
@dp.message_handler(state=UserAddVoice.all_states, text=REJECT_MSG)
async def admin_reject_handler(message: Message, state: FSMContext):
    admin_text = 'Вы отменили действия'
    await bot.send_message(message.chat.id, admin_text, reply_markup=admin_markup)
    await state.finish()


# Handler to get admin to sent advertisement post
@dp.message_handler(state=UserAddVoice.ask_voice, content_types=['voice'])
async def admin_post_type(message: Message, state: FSMContext):
    chat_id = message.chat.id

    user_voice_id = message.voice.file_id

    admin_text = 'Как ваше голосовое сообщение будет называться?\nПришлите название для вашего голосового сообщения'
    await bot.send_message(chat_id, admin_text)
    await state.update_data(user_voice_id=user_voice_id)
    await UserAddVoice.ask_title.set()


# Ask, if the admin sure to start sending advertisement
@dp.message_handler(state=UserAddVoice.ask_title)
async def admin_ask_send(message: Message, state: FSMContext):
    chat_id = message.chat.id
    user_voice_title = message.text

    data = await state.get_data()
    user_voice_id = data['user_voice_id']
    user_voice_db_id = random.randint(1000000, 10000000)

    mem_info_id = {'file_id': user_voice_id, 'title': user_voice_title}

    users_mem_db.set(user_voice_db_id, json.dumps(mem_info_id))

    admin_message = 'Ваше голосовое сообщение успешно добавлено в ваш список ✅'
    await bot.send_message(chat_id, admin_message, reply_markup=favourite_memes_markup)

    await save_favourite_memes(chat_id, 'add_meme', user_voice_db_id)

    await state.finish()
