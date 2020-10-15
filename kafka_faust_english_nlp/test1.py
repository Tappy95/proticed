import requests
import functools
import asyncio
import time
from concurrent import futures

worker_executor = futures.ThreadPoolExecutor(5)


class WalmartProduct:
    def __init__(self, task):
        self.temp1 = 3
        self.temp2 = 2
        self.loop = asyncio.get_event_loop()

    def __aiter__(self):
        return self

    @property
    def url(self):
        return "https://www.baidu.com"

    def get_request(self):
        url = self.url
        print(url)
        resp = requests.get(url)
        time.sleep(2)
        return resp.status_code

    async def get_requests(self):
        executor_loop = asyncio.get_event_loop()
        with futures.ThreadPoolExecutor(1) as pool:
            return await executor_loop.run_in_executor(pool, self.get_request)

    async def __anext__(self):
        if self.temp1 <= 0:
            raise StopAsyncIteration()
        self.temp1 -= 1
        result_info = await self.get_requests()
        print(result_info)
        return self._parse_product_infos([1, 2, 3])

    def _parse_product_infos(self, infos):
        for _, info in enumerate(infos):
            parse_info = self._parse_product(info)
            if parse_info:
                yield parse_info

    def _parse_product(self, info):
        return info


class Stream:
    def __init__(self):
        self.temp = 3

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.temp <= 0:
            raise StopAsyncIteration()
        self.temp -= 1


async def sync_product():
    start = time.time()
    async for task in Stream():
        async for infos in WalmartProduct(task):
            for product_data in infos:
                print(product_data)
    print(time.time() - start)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(sync_product())
