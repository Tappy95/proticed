# redis
import asyncio

import aioredis

REDIS_ADDRESS = "redis://45.35.226.130:13111"
REDIS_PASSWORD = "c18d1ba0f01f15b2168297663a85abf5"
REDIS_DB = 0
REDIS_ENCODING = 'utf-8'
redis = None
AMAZON_BATCH_DATE_KEY = "test:product:batch_date"


async def ts_redis():
    cache_info = await redis.hgetall(AMAZON_BATCH_DATE_KEY)
    print(cache_info)


async def redis_init():
    global redis
    redis = await aioredis.create_redis_pool(REDIS_ADDRESS, db=REDIS_DB,
                                             password=REDIS_PASSWORD,
                                             encoding=REDIS_ENCODING)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(redis_init())
    loop.run_until_complete(ts_redis())
