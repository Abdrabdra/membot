import asyncio
import redis
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State

from data.config import BOT_TOKEN

loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage, loop=loop)

files_id = redis.StrictRedis(host='localhost', port=6379, db=1)
users_db = redis.StrictRedis(host='localhost', port=6379, db=2)
search_db = redis.StrictRedis(host='localhost', port=6379, db=3)
stats_db = redis.StrictRedis(host='localhost', port=6379, db=4)
users_mem_db = redis.StrictRedis(host='localhost', port=6379, db=5)


class AdminSendEveryOne(StatesGroup):
    ask_post = State()
    ask_send = State()


class UserAddVoice(StatesGroup):
    ask_voice = State()
    ask_title = State()
