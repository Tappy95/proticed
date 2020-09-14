import asyncio

import aiohttp


async def cooc():
    async with aiohttp.request('GET','http://httpbin.org/get') as resp:
        print(resp.status)
        print(await resp.text())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(cooc())
    loop.close()
