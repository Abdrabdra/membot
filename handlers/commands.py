from aiogram.types import Message

from keyboards.buttons import start_markup
from utils.helpers import send_message
from utils.help_functions import check_user_info
from main import dp


# Answer to all bot commands
# Ответ на команду /start
@dp.message_handler(commands=['start'])
async def start_command(message: Message):
    chat_id = message.chat.id

    await check_user_info(chat_id)
    await send_message(chat_id, 'start', markup=start_markup)
    await send_message(chat_id, 'our_bots', markup=start_markup, parse='markdown')
