from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def memes_generate_buttons(search_response, memes_type, page_number, is_prev=True, is_next=True):
    start_number = int(page_number) * 10
    end_number = int(start_number) + 10

    audio_markup = InlineKeyboardMarkup(row_width=3)
    for i, audio_info in enumerate(search_response):
        if i in range(start_number, end_number):
            audio_title = audio_info['title']

            button_data = 'tracks!{0}!{1}'.format(memes_type, i)

            audio_button = InlineKeyboardButton(text=audio_title, callback_data=button_data)
            audio_markup.add(audio_button)

    if len(audio_markup['inline_keyboard']) == 0:
        return None

    data_next = 'search!{0}!{1}'.format(memes_type, page_number + 1)
    button_next = InlineKeyboardButton(text='➡️', callback_data=data_next)

    data_previous = 'search!{0}!{1}'.format(memes_type, page_number - 1)
    button_previous = InlineKeyboardButton(text='⬅️️', callback_data=data_previous)

    delete_button = InlineKeyboardButton(text='❌', callback_data='delete')

    all_data = 'tracksall!{0}!{1}'.format(memes_type, page_number)
    all_button = InlineKeyboardButton(text='🔽', callback_data=all_data)

    list_direct_buttons = []
    if is_prev:
        list_direct_buttons.append(button_previous)

    list_direct_buttons.append(delete_button)

    if is_next:
        list_direct_buttons.append(button_next)

    audio_markup.add(*list_direct_buttons)
    audio_markup.add(all_button)

    return audio_markup


async def generate_favourites_markup(audio_id, method):
    if method == 'remove_meme':  # If before button was add meme, then the new will be remove meme
        button_text = '💔 Убрать из избранного️'
    else:
        button_text = '❤️ Добавить в избранное️'

    favourite_markup = InlineKeyboardMarkup(row_width=1)
    favourite_button = InlineKeyboardButton(text=button_text, callback_data=f'{method}!!{audio_id}')
    favourite_markup.add(favourite_button)

    return favourite_markup


favourite_memes_markup = InlineKeyboardMarkup(row_width=1)
show_favourite_button = InlineKeyboardButton(text='❤️ Посмотреть избранные звуки', switch_inline_query_current_chat='')
favourite_memes_markup.add(show_favourite_button)

