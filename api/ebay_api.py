import json
import asyncio
import aiohttp
from ebaysdk.trading import Connection as Trading
from ebaysdk.response import Response, ResponseDataObject
from util.log import logger


class BaseAPI:
    verb = None
    id_map = {
        'EBAY-US': 0,
        'EBAY-ENCA': 2,
        'EBAY-GB': 3,
        'EBAY-AU': 15,
        'EBAY-AT': 16,
        'EBAY-FRBE': 23,
        'EBAY-FR': 71,
        'EBAY-DE': 77,
        'EBAY-MOTOR': 100,
        'EBAY-IT': 101,
        'EBAY-NL': 146,
        'EBAY-NLBE': 123,
        'EBAY-ES': 186,
        'EBAY-CH': 193,
        'EBAY-HK': 201,
        'EBAY-IN': 203,
        'EBAY-IE': 205,
        'EBAY-MY': 207,
        'EBAY-FRCA': 210,
        'EBAY-PH': 211,
        'EBAY-PL': 212,
        'EBAY-SG': 216,
    }
    APPID = 'hsfWwmhs-tianshiz-PRD-9f8f66498-3851d3d0'
    DEVID = 'c1cd3fa3-bea2-4058-8ead-83c5d562ef01'
    CERTID = 'PRD-f8f664985b00-3731-4e23-9258-8438'
    TOKEN = 'AgAAAA**AQAAAA**aAAAAA**xXQIXQ**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6AHlIOnC5CAqAWdj6x9nY+seQ**7EIDAA**AAMAAA**IOoLODsPncRfznEUpBa0UvdO7TcxgzueyidoWl3m6bjN/O0DaWi1QlLq12gQrQsDy8L8Hg4VA2vD9FWYoWx1JtE6Gn5F2/mwRaEK5T3ZixOEo0/eCQx/L7Tbra6GTcylsLoiNQE3zbLq1lQvouLZ3G8Pc5qZpKRuYEr4AU207EACLXYfPvYOFdUHFddRRoBtS0icVvAyv4Q+i4J8HO+CBr6qx19wRkLFNZgyG5HPYvqfGCXIr3vNNcNYbrtp6FPlY18oZ5Fu3u5hVomENIJnba0WkG/1ncy0UbxmSW1c6YnzVmLgDaaqlVNnCuUe+RkTnxPsb4XBN9zmuh7O9ge1Dzna+M8dF4CeNpbt0Hs1COYaINFC/WcmMwsFsH4BUZN7FpA3VmfWe/6vQi8qnegjdI04lobJjAa0GL+ljlwMPGdQatgc53aIZ2w+BjsrdYqKY1HvdNyePyg9zic6GPxOGF+l01MqOlIVZZS6U4VrfD8DbyUwcf7hupOlhtcA7HhLlNAb65oxE3Jlm3yBIW1JJCfMUHFICVkKr2h0a+aCkQH/by0lEGBnP8u2X8ejSnzXxhO6xd4ZvSvWGzisMVm3IATIBOXHv6EETr4BP/gWawqVjYbLvtGLg+ufVp06M5KFCWubNEkDkcHb8CLDT90srr8H12VRuLAcX5tSTIOX9dENrpcRl22EANGS8OFBPSu9fMdzhZeB5Dm16U6seGlwYc7J+tWuGTBJRYqJzjW/XPpVLoiL3kghQGkLLgb56Uzl'

    connector = aiohttp.TCPConnector(enable_cleanup_closed=True)
    params = None

    def __init__(self, site, data):
        self._api = Trading(siteid=self.id_map.get(site, 0), appid=self.APPID,
                            devid=self.DEVID, certid=self.CERTID, token=self.TOKEN,
                            config_file=None)
        self._api.build_request(self.verb, data, verb_attrs=None)
        self.method = self._api.request.method
        self.url = self._api.request.url


        self.headers = self._api.request.headers
        self.body = self._api.request.body

    async def aio_request(self, timeout=60, proxy=None, retry=3, request_interval=0, retry_interval=0):
        while retry:
            try:
                await asyncio.sleep(request_interval)
                async with aiohttp.ClientSession(connector=self.connector, connector_owner=False) as session:
                    async with session.request(self.method, self.url, headers=self.headers,
                                               data=self.body, proxy=proxy,
                                               timeout=aiohttp.ClientTimeout(total=timeout)) as resp:
                        if resp.status != 200:
                            retry -= 1
                            logger.error(
                                "[status code error] {}, params: {}, retry remain: {}".format(resp.status, self.params,
                                                                                              retry))
                        else:
                            return Response(ResponseDataObject({'content': await resp.read()}),
                                            self.verb).dict()
            except Exception as exc:
                logger.error(
                    "[request error] {} {}, params: {}, retry remain: {}".format(type(exc), exc, self.params, retry))
            await asyncio.sleep(retry_interval)


class GetItem(BaseAPI):
    verb = "GetItem"

    def __init__(self, site, item_id):
        self.params = (site, item_id)
        data = {
            'ItemID': item_id,
            'IncludeWatchCount': True,
            'IncludeItemSpecifics': True,
            'DetailLevel ': 'ItemReturnAttributes'
        }
        super().__init__(site, data)


class GetSellerList(BaseAPI):
    verb = "GetSellerList"

    def __init__(self, site, user_id):
        self.params = (user_id)
        data = {
            'UserID': user_id,
            'EndTimeFrom': '2020-11-18 10:00:00',
            'EndTimeTo': '2020-11-18 10:00:00',
            'StartTimeFrom': '2020-11-11 10:00:00',
            'StartTimeTo': '2020-11-11 10:00:00',
            'Pagination ': {
                "EntriesPerPage": 10,
                "PageNumber": 1
            }
        }
        super().__init__(site, data)


if __name__ == '__main__':
    async def test():
        api = GetSellerList('uk', 'neogames')
        dct = await api.aio_request()
        print(json.dumps(dct))


    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
