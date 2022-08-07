from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from data.messages.admin import LIST_ADMIN_COMMANDS, START_MAILING_MSG, REJECT_MSG

reject_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
reject_button = KeyboardButton(REJECT_MSG)
reject_markup.add(reject_button)


sure_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
send_button = KeyboardButton(START_MAILING_MSG)
reject_button = KeyboardButton(REJECT_MSG)
sure_markup.add(*[send_button, reject_button])


admin_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
for admin_command in LIST_ADMIN_COMMANDS:
    admin_button = KeyboardButton(admin_command)
    admin_markup.add(admin_button)


start_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
# start_button_1 = KeyboardButton('🔎 Поиск звуков')
start_button_1 = KeyboardButton('🎧 Добавить свой звук')
start_button_2 = KeyboardButton('🔊 Популярные звуки')
start_button_3 = KeyboardButton('🕺 Звуки из TikTok')
start_button_4 = KeyboardButton('💃 Звуки из Reels')
start_button_5 = KeyboardButton('❤️ Избранные звуки')
start_markup.add(*[start_button_1, start_button_2, start_button_3, start_button_4, start_button_5])
