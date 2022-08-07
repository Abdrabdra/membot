# coding=utf-8
import asyncio
from functools import wraps, partial

from main import bot
from data.messages.bot import msg_dict


# Function to send waiting message
async def send_message(chat_id, msg_str, args=None, markup=None, parse=None):
    msg_to_send = await user_msg(msg_str, args)
    sent_message = await bot.send_message(chat_id, msg_to_send, reply_markup=markup, parse_mode=parse,
                                          disable_web_page_preview=True)
    return sent_message


async def copy_message(chat_id, from_chat_id, message_id):
    try:
        copied_message = await bot.copy_message(chat_id, from_chat_id, message_id)
        return copied_message.message_id
    except Exception as err:
        print('[ERROR] in copy_message\nException: {}\n\n'.format(err))


async def send_voice(chat_id, file_to_send, markup=None):
    try:
        caption = await user_msg('downloaded', None)
        sent_music = await bot.send_voice(chat_id, file_to_send, caption=caption, reply_markup=markup)
        return sent_music.voice.file_id

    except Exception as err:
        print(err, 'send_voice')
        return False


async def send_document(chat_id, file_to_send, caption):
    await bot.send_document(chat_id, open(file_to_send, 'rb'), caption=caption)


async def edit_message(chat_id, msg_str, message_id, markup, args, parse=None):
    try:
        msg_to_send = await user_msg(msg_str, args)
        await bot.edit_message_text(msg_to_send, chat_id, message_id=message_id, reply_markup=markup, parse_mode=parse)
    except Exception as err:
        pass


async def answer_inline_query(query_id, results, cache_time):
    await bot.answer_inline_query(query_id, results=results, switch_pm_text='Get more music 🔥',
                                  switch_pm_parameter='inline_vk', cache_time=cache_time)


# Get user message
async def user_msg(message_str, args=None):
    if args is None:
        user_message = msg_dict[message_str]
    else:
        if type(args) != tuple:
            user_message = msg_dict[message_str].format(args)
        else:
            user_message = msg_dict[message_str].format(*args)

    return user_message


def wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run
