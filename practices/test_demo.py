import asyncio

import aiohttp


async def assfdss():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://www.songyixian.top:5000/nlp/keywords',
                               params={"title": "asdfadf"}) as resp:
            rate_info = await resp.json()
            print(rate_info['result'])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(assfdss())
    loop.close()