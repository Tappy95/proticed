# import asyncio
#
# import aiohttp
#
#
# async def assfdss():
#     async with aiohttp.ClientSession() as session:
#         async with session.get('http://www.songyixian.top:5000/nlp/keywords',
#                                params={"title": "asdfadf"}) as resp:
#             rate_info = await resp.json()
#             print(rate_info['result'])
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     result = loop.run_until_complete(assfdss())
#     loop.close()
import asyncio
import aio_pika


async def main(loop):
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@192.168.6.198/", loop=loop, port=5672
    )

    async with connection:
        routing_key = "test_queue"

        channel = await connection.channel()
        while True:
            await channel.default_exchange.publish(
                aio_pika.Message(body="Hello {}".format(routing_key).encode()),
                routing_key=routing_key,
            )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()