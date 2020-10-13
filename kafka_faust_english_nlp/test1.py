import requests
import functools
import asyncio
import time
from concurrent import futures

worker_executor = futures.ThreadPoolExecutor(5)


class WalmartProduct:
    def __init__(self):
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
        resp = requests.get(url)
        time.sleep(4)
        return resp.status_code

    def create_work(self, func, worker_executor1):
        @functools.wraps(func)
        async def worker():
            return await self.loop.run_in_executor(worker_executor1, func)

        return worker

    def request(self):
        worker = self.create_work(self.get_request, worker_executor)
        return self.loop.create_task(worker())

    async def __anext__(self):
        if self.temp1 <= 0:
            raise StopAsyncIteration()
        self.temp1 -= 1
        result_info = await self.request()
        print("func result code :", result_info)
        return self._parse_product_infos([1, 2, 3])

    def _parse_product_infos(self, infos):
        for _, info in enumerate(infos):
            parse_info = self._parse_product(info)
            if parse_info:
                yield parse_info

    def _parse_product(self, info):
        return info


async def sync_product():
    start = time.time()
    async for infos in WalmartProduct():
        for product_data in infos:
            print(product_data)
    print(time.time() - start)


if __name__ == '__main__':
    asyncio.run(sync_product())
