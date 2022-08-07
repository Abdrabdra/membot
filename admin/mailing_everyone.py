import asyncio

from time import time
from datetime import timedelta

from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.utils.exceptions import UserDeactivated, BotBlocked

from utils.helpers import wrap
from data.messages.admin import REJECT_MSG, START_MAILING_MSG
from main import users_db, dp, bot, AdminSendEveryOne
from keyboards.buttons import reject_markup, sure_markup, admin_markup
from data.constants import AD_CHANNEL_ID, AD_CHANNEL_LINK, AD_STATS_GROUP_ID, ADS_ACTION_GROUP_ID


# Ask admin to choose to which users send advertisement
async def mailing_everyone_func(chat_id):
    admin_text = 'Перешлите пост для рассылки с @KamronMediaAds.'
    await bot.send_message(chat_id, admin_text, reply_markup=reject_markup)
    await AdminSendEveryOne.ask_post.set()


# Handler to receive reject message
@dp.message_handler(state=AdminSendEveryOne.all_states, text=REJECT_MSG)
async def admin_reject_handler(message: Message, state: FSMContext):
    admin_text = 'Вы отменили действия'
    await bot.send_message(message.chat.id, admin_text, reply_markup=admin_markup)
    await state.finish()


# Handler to get admin to sent advertisement post
@dp.message_handler(state=AdminSendEveryOne.ask_post, content_types=['photo', 'text', 'voice', 'animation'])
async def admin_post_type(message: Message, state: FSMContext):
    chat_id = message.chat.id

    post_markup = message.reply_markup
    message_id = message.forward_from_message_id

    admin_text = 'Ваш пост будет выглядеть так, начать рассылку?'
    await bot.send_message(chat_id, admin_text, reply_markup=sure_markup)
    await bot.copy_message(chat_id, AD_CHANNEL_ID, message_id, reply_markup=post_markup)
    await state.update_data(buttons=post_markup, message_id=message_id)
    await AdminSendEveryOne.ask_send.set()


# Ask, if the admin sure to start sending advertisement
@dp.message_handler(state=AdminSendEveryOne.ask_send, text=START_MAILING_MSG)
async def admin_ask_send(message: Message, state: FSMContext):
    chat_id = message.chat.id

    # Get data that is needed to send advertisement
    data = await state.get_data()
    message_id = data.get('message_id')
    buttons = data.get('buttons')

    await state.finish()

    admin_message = f'Идет подготовка базы для рассылки.'
    sent_message = await bot.send_message(chat_id, admin_message, reply_markup=admin_markup)

    list_users_id = await get_users_id()
    await sent_message.delete()

    admin_message = 'Рассылка началась!\n' \
                    'Количество пользователей: {0:,}\n' \
                    'Пост: {1}{2}'.format(len(list_users_id), AD_CHANNEL_LINK, message_id)

    await bot.send_message(chat_id, admin_message, reply_markup=admin_markup, disable_web_page_preview=True)
    await bot.send_message(ADS_ACTION_GROUP_ID, admin_message, disable_web_page_preview=True)

    blocked = 0
    deactivated = 0
    errors = 0
    success = 0

    start_time = time()

    sent_message = await send_progress_message(chat_id, success)

    first_users_to_send = []
    for user_id in list_users_id:
        if len(first_users_to_send) < 20:
            first_users_to_send.append(user_id)
            continue

        tasks = []
        for user_to_send in first_users_to_send:
            tasks.append(asyncio.ensure_future(send_copied_post_to_user(user_to_send, message_id, buttons)))

        gather_results = await asyncio.gather(*tasks)
        for result in gather_results:
            if result == 'success':
                success += 1
                if success % 5000 == 0:
                    await sent_message.delete()
                    sent_message = await send_progress_message(chat_id, success)
            elif result == 'blocked':
                blocked += 1
            elif result == 'deactivated':
                deactivated += 1
            else:
                errors += 1

        await asyncio.sleep(1)
        first_users_to_send = []

    end_time = time()
    taken_time_seconds = int(end_time - start_time)
    taken_time = str(timedelta(seconds=taken_time_seconds))

    admin_stat = "Рассылку получили: {0:,}\n" \
                 "Удалили бота: {1:,}\n" \
                 "Удалились с телеграм: {2:,}\n" \
                 "Прочие ошибки: {3:,}\n" \
                 "Длительность: {4}\n" \
                 "Пост: {5}{6}".format(success, blocked, deactivated, errors, taken_time, AD_CHANNEL_LINK, message_id)

    await bot.send_message(chat_id, admin_stat, reply_markup=admin_markup, disable_web_page_preview=True)
    await bot.send_message(AD_STATS_GROUP_ID, admin_stat, reply_markup=admin_markup, disable_web_page_preview=True)
    await sent_message.delete()


async def send_copied_post_to_user(user_id, message_id, buttons):
    try:
        await bot.copy_message(user_id, AD_CHANNEL_ID, message_id, disable_notification=True, reply_markup=buttons)
        return 'success'
    except BotBlocked:
        users_db.set(user_id, 'None')
        return 'blocked'
    except UserDeactivated:
        users_db.set(user_id, 'None')
        return 'deactivated'
    except Exception as err:
        print(err, 'send_copied_post_to_user')
        return False


async def send_progress_message(chat_id, count):
    sent_message = await bot.send_message(chat_id, '{0:,} пользователей получили рассылку'.format(count))
    return sent_message


# Function to get users id
@wrap
def get_users_id():
    users_id = users_db.keys()
    list_users_id = []

    for user_id in users_id:
        str_user_id = str(user_id, 'utf-8')
        if not str_user_id.isdigit():
            continue

        list_users_id.append(int(str_user_id))

    return list_users_id
