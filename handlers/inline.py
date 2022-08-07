from aiogram.types import InlineQuery

from utils.sounds.memes_search_inline import memes_search_inline
from main import dp


@dp.inline_handler(lambda query: True)
async def inline_query(query: InlineQuery):
    await memes_search_inline(query.from_user.id, query.id)
