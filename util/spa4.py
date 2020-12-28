import asyncio
import aiohttp

semaphore = asyncio.Semaphore(10)
def get_url():
    url_lis = []
    for i in range(0, 100):
        url = 'https://spa5.scrape.center/api/book/?limit=18&offset={}'.format(i * 18)
        url_lis.append(url)
    return url_lis


url_lis = get_url()


async def request(url):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                await asyncio.sleep(1)
                return await r.json()


async def main():
    await asyncio.gather(*[request(url) for url in url_lis])


if __name__ == '__main__':
    import time

    start = time.time()
    asyncio.get_event_loop().run_until_complete(main())
    print(time.time() - start)
