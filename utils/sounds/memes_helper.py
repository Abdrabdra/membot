import asyncio

import aiohttp
from pyquery import PyQuery as pq

POPULAR_MEME_LINK = 'https://zvukogram.com/category/zvuki-iz-memov/'
TIKTOK_MEME_LINK = 'https://zvukogram.com/category/tik-tok/'
REELS_MEME_LINK = 'https://zvukogram.com/category/reels/'
SEARCH_MEME_LINK = 'https://zvukogram.com/?r=search&s={}'


async def get_list_memes(meme_type):
    try:
        if meme_type == 'TIKTOK_MEMES':
            url_to_request = TIKTOK_MEME_LINK
        elif meme_type == 'REELS_MEMES':
            url_to_request = REELS_MEME_LINK
        elif meme_type == 'POPULAR_MEMES':
            url_to_request = POPULAR_MEME_LINK
        else:
            url_to_request = SEARCH_MEME_LINK.format(meme_type)

        async with aiohttp.ClientSession() as session:
            async with session.get(url_to_request, allow_redirects=True) as get_request:
                response = await get_request.content.read()
                response_str = str(response, 'utf-8')
                pq_objects = pq(response_str)('div.trackList')('div.onetrack').items()

                list_dict = []
                for i, pq_object in enumerate(pq_objects):
                    audio_title = pq_object('div.waveTitle').text()
                    audio_id = pq_object.attr('data-id')

                    info_dict = {'title': audio_title, 'id': audio_id}
                    list_dict.append(info_dict)

        return list_dict

    except Exception as err:
        print(err, 'get_list_memes')
        return []


if __name__ == '__main__':
    asyncio.run(get_list_memes('ЫВахфывахыфвхафыхвах3цуахыхва'))

