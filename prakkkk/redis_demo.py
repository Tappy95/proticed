# -*- coding: utf-8 -*-

# @File Name：      redis_demo.py
# @Description:
# @Author:        lipeng
# @Time:           2020/5/18 15:08

__author__ = 'lipeng'

import redis
import json
import re

# IP 代理池 redis
proxy_config = {
    # "host": "45.34.33.156",
    "host": "45.34.49.226",
    "port": 12111,
    "db": 0,
    "password": "33fa5bf446e431cf263cc29c8eec0fbb",
}

proxy_config_save = {
    "host": "45.34.33.156",
    "port": 12111,
    "db": 10,
    "password": "513f21fbc55d446186c7f1daa9dae626",
}

redis_db = redis.StrictRedis(**proxy_config)
redis_db_save = redis.StrictRedis(**proxy_config_save)


def add(host):
    redis_db_save.zadd("proxy_pool_us_2", {host: 10})


def get():
    result_ls = redis_db.zrange("proxy3", start=0, end=-1, desc=False)
    # result2 = redis_db.zrange("7", start=0, end=1, desc=False)
    print(type(result_ls))
    # print(result2)
    if result_ls:
        for i in result_ls:
            proxy = json.loads(i)  # # 'http://103.15.140.138:44759'
            matchObj = re.match(r"http://(\d+.\d+.\d+.\d+:\d+)", proxy.get("http"))
            if matchObj:
                host = matchObj.group(1)
                print(host)
                # yield host
                add(host)


# add()
# get()

import asyncio
import aioredis
import re


# REDIS_CONF = {'host': '104.217.128.26', 'port': 12111, 'db': 15, 'password': '33fa5bf446e431cf263cc29c8eec0fbb'}


class AsyncRedis:
    # 异步 操作redis
    #

    # @staticmethod
    # async def handle():
    #
    #     # Redis client bound to single connection (no auto reconnection).
    #
    #     # await redis.set('my-key', 'value')
    #     # val = await redis.get('my-key')
    #     # print(val)
    #     await AsyncRedis.parse(r)
    #
    #     # gracefully closing underlying connection
    #     r.close()
    #     await r.wait_closed()
    def __init__(self):
        self.semaphore = asyncio.Semaphore(15)  # 限制最大并发量

    # @staticmethod
    async def async_add(self, host, r_save):
        async with self.semaphore:  # 并发量限制
            # r_save = await aioredis.create_redis_pool(
            #     'redis://45.34.33.156:12111', db=10, password='513f21fbc55d446186c7f1daa9dae626')
            await r_save.zadd(key="proxy_pool_us_2", score=10, member=host)

            # r_save.close()
            # await r_save.wait_closed()

    async def async_get(self):
        r_read = await aioredis.create_redis_pool(
            'redis://45.34.49.226:12111', db=0, password='33fa5bf446e431cf263cc29c8eec0fbb')
        r_save = await aioredis.create_redis_pool(
            'redis://45.34.33.156:12111', db=10, password='513f21fbc55d446186c7f1daa9dae626')
        result_ls = await r_read.zrange("proxy3", start=0, stop=-1, withscores=True)
        # print(result_ls)
        # result2 = redis_db.zrange("7", start=0, end=1, desc=False)
        # print(type(result_ls))
        # # print(result2)
        # async with self.semaphore:  # 并发量限制
        coros = []
        if result_ls:
            for i in result_ls:
                # print(i)
                proxy = json.loads(i[0])  # # 'http://103.15.140.138:44759'
                matchObj = re.match(r"http://(\d+.\d+.\d+.\d+:\d+)", proxy.get("http"))
                if matchObj:
                    host = matchObj.group(1)
                    print(host)
        #             # yield host
        #             await self.async_add(host)
                    coros.append(asyncio.ensure_future(self.async_add(host, r_save)))
        await asyncio.gather(*coros)
        # await asyncio.wait(coros)

        r_save.close()
        await r_save.wait_closed()

        r_read.close()
        await r_read.wait_closed()


def main():
    red = AsyncRedis()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(red.async_get())
    loop.close()


if __name__ == '__main__':
    main()
