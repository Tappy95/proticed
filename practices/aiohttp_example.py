import asyncio

import aiohttp
import requests

proxy = {'https': 'http://lum-customer-onesiness-zone-static10:kz53twdp74rd@zproxy.lum-superproxy.io:22225',
         'http': 'http://lum-customer-onesiness-zone-static10:kz53twdp74rd@zproxy.lum-superproxy.io:22225'}
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; nl-nl) AppleWebKit/418.9 (KHTML, like Gecko) Safari/419.3',
    'accept-encoding': 'gzip, deflate, br', 'accept-language': 'en;q=0.9,ja;q=0.8,fr;q=0.7', 'accept': '*/*',
    'content-type': 'application/json',
    'referer': 'https://www.walmart.com/browse?cat_id=1072864_1067612_1230791_1067810&sort=best_seller',
    'connection': 'close'}


async def cooc():
    async with aiohttp.request('GET',
                               'https://www.walmart.com/search/api/preso?prg=desktop&cat_id=1005862_9157053_4585847&sort=best_seller',
                               proxy=proxy, headers=headers) as resp:
        print(resp.status)
        print(await resp.text())


def reuest_walmart_proxy():
    resp = requests.get(
        url='https://www.walmart.com/search/api/preso?prg=desktop&cat_id=1072864_1067612_1230791_1067810&sort=best_seller',
        headers=headers, proxies=proxy)
    print(resp.status_code)
    print(resp.text)

if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(cooc())
    # loop.close()
    # reuest_walmart_proxy()

    print(sum([]))