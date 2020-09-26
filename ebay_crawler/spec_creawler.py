import asyncio
import json

import aiohttp

from api.ebay_api import GetItem

if __name__ == '__main__':
    async def test():
        api = GetItem('EBAY-UK', '283978783369')
        dct = await api.aio_request()
        print(str(dct['Item']['ItemSpecifics']['NameValueList']))
        # print(json.dumps(dct))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())