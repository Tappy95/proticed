# i = []
# s = "\n".join(i)
# a = {}
# d = [i for i in a.values()]
# print("-----{}----".format(d))
# print(a.values())
# print(len(s))
# print("------{}--------".format(s))
import asyncio
import json

import httpx as httpx


async def run_httpx():
    async with httpx.AsyncClient() as client:
        r = await client.get('http://www.baidu.com')
        assert r.status_code == 200
        a = json.loads(r.text)
        print(a)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_httpx())
