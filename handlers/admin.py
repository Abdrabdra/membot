from aiogram.types import Message

from main import bot, dp
from keyboards.buttons import admin_markup

from admin.bot_statistics import bot_statistics_func
from admin.mailing_everyone import mailing_everyone_func
from admin.backup_database import backup_database_func

from data.constants import ADMINS_ID, MANAGERS_ID
from data.messages.admin import LIST_ADMIN_COMMANDS, MAILING_MSG, BACKUP_MSG, STATISTICS_MSG


# Answer to admin commands
@dp.message_handler(chat_id=ADMINS_ID + MANAGERS_ID, commands=['admin'])
async def get_admin_commands_handler(message: Message):
    await bot.send_message(message.chat.id, 'Все команды админа', reply_markup=admin_markup)


# Answer to admin commands
@dp.message_handler(chat_id=ADMINS_ID + MANAGERS_ID, text=LIST_ADMIN_COMMANDS)
async def answer_admin_command_handler(message: Message):
    chat_id = message.chat.id
    admin_command = message.text

    if chat_id in ADMINS_ID:
        if admin_command == BACKUP_MSG:
            await backup_database_func(chat_id)

        elif admin_command == STATISTICS_MSG:
            await bot_statistics_func(chat_id)

    if admin_command == MAILING_MSG:
        await mailing_everyone_func(chat_id)
