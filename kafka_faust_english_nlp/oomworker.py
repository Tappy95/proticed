import asyncio
import json

import sys
from concurrent.futures import ThreadPoolExecutor

import requests

sys.path.append('../')

import faust
import httpx
from pympler import tracker, summary, muppy, refbrowser

from util.log import logger

# tr = tracker.SummaryTracker()

app = faust.App(
    'hello-world',
    broker='kafka://47.112.96.218:9092'
)

greetings_topic = app.topic('mykafka')

a = 0


def task(url, headers):
    session = requests.Session()
    response = session.get(url=url, headers=headers)
    if response.status_code == 200:
        return response.text, url
    else:
        return response.status_code, url


pool = ThreadPoolExecutor(4)


def get_return(obj):
    print((len(obj.result()[0])))
    print(obj.result()[1])
    return obj.result()[0]


url_list = [
    'http://www.baidu.com',
    'http://www.JD1.com',
    'http://www.JD2.com',
    'http://www.JD3.com',
    'http://www.JD4.com',
    'http://www.JD5.com',
]


def create_work(func, task_q, loop, worker_executor, result_q):
    """ Wrap func into coroutine, func will run as a coroutine
    """
    import functools

    @functools.wraps(func)
    async def worker():
        task = await task_q.get()
        task = await loop.run_in_executor(worker_executor, func, task)
        await result_q.put(task)

    return worker


def get_requests(url):
    print(22222222222222222222222222222222)
    resp = requests.get(url)
    info = None
    if resp.status_code != 200:
        logger.error("[status code error] {} {}"
                     .format(resp.status_code, url))
    else:
        info = json.loads(resp.text)
    result_info = {"product_ls": [], "count_info": {}, "page_info": {}}
    if info is not None:
        result_info["product_ls"] = info.get("items", [])
        result_info["count_info"] = info.get("requestContext", {}).get("itemCount", {})
        result_info["page_info"] = info.get("pagination", {})
    return result_info


@app.timer(interval=5)
async def every_minute():
    print('WAKE UP')
    # tr.print_diff()
    # for url in url_list:
    import time
    import concurrent.futures
    start = time.time()
    try:
        loop = asyncio.get_event_loop()
        task_q = asyncio.Queue(5, loop=loop)
        result_q = asyncio.Queue(5, loop=loop)
        executor = concurrent.futures.ThreadPoolExecutor(5)
        task_ls = []
        for _ in range(5):
            await task_q.put("https://www.baidu.com")
            worker = create_work(get_requests, task_q, loop, executor, result_q)
            task_ls.append(loop.create_task(worker()))
        await asyncio.gather(*task_ls)

        for _ in range(5):
            result_info = await result_q.get()
            print(result_info)
    except Exception as exc:
        exc_info = (type(exc), exc, exc.__traceback__)
        logger.error("[request error] url: {}".format("https://www.baidu.com"), exc_info=exc_info)
        exc.__traceback__ = None
    print(time.time() - start)
    # tr.print_diff()


if __name__ == '__main__':
    app.main()
