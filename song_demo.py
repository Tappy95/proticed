import asyncio
import json
import operator
import time
from datetime import datetime, timedelta

import nsq
import tornado.ioloop
from sqlalchemy import create_engine, or_, update
from sqlalchemy.dialects.mysql import insert

from HY_keyword import TOPIC_NAME
from amazon_keyword.worker import KeywordTaskInfo
from api.amazon_keyword import GetAmazonKWMStatus, AddAmazonKWM, GetAmazonKWMAllResult, GetAmazonKWMResult, DelAmazonKWM
from api.amazon_product import GetAmazonProductBySearch
from api.ebay_product import GetEbayProduct, GetEbayProductBySearch
from api.shopee_product import GetShopeeProductBySearch
from models.amazon_models import amazon_keyword_task
from task_protocol import HYTask
from sqlalchemy import select
from config import *
from util.pub import pub_to_nsq

engine = create_engine(
    # 链接地址
    SQLALCHEMY_DATABASE_URI,
    # 连接池
    pool_pre_ping=SQLALCHEMY_POOL_PRE_PING,
    # 日志等级
    echo=SQLALCHEMY_ECHO,
    # 连接池大小
    pool_size=SQLALCHEMY_POOL_SIZE,
    # 连接池溢出,仅限于queuepool
    max_overflow=SQLALCHEMY_POOL_MAX_OVERFLOW,
    # 池回收时间
    pool_recycle=SQLALCHEMY_POOL_RECYCLE,
)


def getstatus():
    # with engine.connect() as conn:
    #     result_from_db = select(([amazon_keyword_task]))
    #     conn.execute()
    result = GetAmazonKWMStatus(ids=[424945]).request()
    print(result, "getstatus")


def addmonkwasins():
    result = AddAmazonKWM(
        station='US',
        asin_and_keywords=[{"asin": "B07PY52GVP", "keyword": "XiaoMi"}],
        num_of_days=31,
        monitoring_num=24,
    ).request()
    print(result, "add_a_kw_watch")


def getallresult():
    # with engine.connect() as conn:
    #     idss = conn.execute(select([amazon_keyword_task.c.id])).fetchall()
    # print(idss)
    ids = [424945]
    result = GetAmazonKWMStatus(
        # station='US',
        # capture_status='4',
        ids=ids

    ).request()
    # print(result['result']['total'])
    # with engine.connect() as conn:
    #
    #     conn.execute(amazon_keyword_task.insert(), [{'id': value['id'],'is_effect': 1} for value in result['result']['list']])
    print(result)


def getallkwasin():
    result = GetAmazonKWMAllResult(
        station='US',
    ).request()
    print(result)


class add_crawler():
    def __init__(self, ):
        pass


def getkwrank():
    a = (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
    print(a)
    b = (datetime.now().replace(microsecond=0) - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    print(b)
    result_rank = GetAmazonKWMResult(
        ids=[514350],
        start_time=(datetime.now().replace(microsecond=0) - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S'),
        end_time=(datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),
    ).request()
    print(result_rank['result'][0]['keyword_list'])


def map_test(info):
    parsed_info = {
        "id": info["id"],
        "asin": info["asin"],
        "keyword": info["keyword"],
        "status": info["status"],
        "monitoring_num": info["monitoring_num"],
        "monitoring_count": info["monitoring_count"],
        "monitoring_type": info["monitoring_type"],
        "station": info["station"],
        "start_time": info["start_time"],
        "end_time": info["end_time"],
        "created_at": info["created_at"],
        "deleted_at": info["deleted_at"],
        "is_add": 1,
        "last_update": datetime.now(),
    }
    return list(map(parsed_info, info))


# def pub_message():
#     message = {"task": "haiying.amazon.keyword", "data": {"site": "JP", "asin": "B072M34RQC", "keyword": "Monitor&qid"}}
#     writer.pub('haiying.amazon.keyword',json.dumps(message))

def db():
    with engine.connect() as conn:
        select_task = select([amazon_keyword_task]) \
            .where(
            or_(
                amazon_keyword_task.c.monitoring_count == 12,
                amazon_keyword_task.c.station != 'US',
            )
        )
        select_db = conn.execute(select_task).fetchall()
        for one in select_db:
            print(one['monitoring_count'], one['station'])
            interval_db = one['end_time'] - datetime.now()
            print(interval_db)
            # if interval_db < timedelta(days=5):
            #     print(one['end_time'])
            #     print(datetime.now() - one['last_update'])


def db_classification_invalid():
    with engine.connect() as conn:
        select_effect_task = conn.execute((select([
            amazon_keyword_task.c.id,
        ]).where(
            # 监控状态不为6(已删除)
            amazon_keyword_task.c.capture_status != 6,
            # 距离结束时间大于五天
            (amazon_keyword_task.c.end_time - datetime.now()) > timedelta(days=5),
        )
        )
        ).fetchall()
    print(select_effect_task)


def db_classification_effect():
    with engine.connect() as conn:
        select_effect_task = conn.execute((select([
            amazon_keyword_task.c.id,
            amazon_keyword_task.c.end_time,
            amazon_keyword_task.c.capture_status,
        ]))).fetchall()
        effect_id = []
    for one in select_effect_task:
        # 距离任务结束大于五天
        if one['end_time'] - datetime.now() > timedelta(days=5) \
                and one['capture_status'] != 3:
            effect_id.append(one['id'])
    return effect_id


def db_classification_invalid():
    # 返回失效任务对象
    with engine.connect() as conn:
        select_invalid_task = conn.execute(select([
            amazon_keyword_task.c.id,
            amazon_keyword_task.c.capture_status,
            amazon_keyword_task.c.end_time,
            amazon_keyword_task.c.last_update,
            amazon_keyword_task.c.deleted_at,
        ])).fetchall()
        print(select_invalid_task)
        invalid_id = []
        for row in select_invalid_task:
            # 装态为已删除,任务结束时间不足五天,超过四天未更新(最小频率为四天一次)
            if row['capture_status'] == 6 or \
                    row['deleted_at'] is not None or \
                    (row['end_time'] - datetime.now()) < timedelta(days=5) or \
                    datetime.now() - row['last_update'] > timedelta(days=4):
                invalid_id.append(row['id'])
        print(invalid_id)


def delete_all_task():
    # with engine.connect() as conn:
    #     select_invalid_task = conn.execute(select([
    #         amazon_keyword_task.c.id,
    #     ]).where(
    #         amazon_keyword_task.c.station == "ge"
    #     )
    #         ).fetchall()
    #     print(select_invalid_task)
    count = 0
    for i in ["DE", "US", "UK", "FR", "JP", "IT", "ES", "CA", "AU"]:

        result_task = GetAmazonKWMStatus(
            station=i,
            # capture_status=0,
            # ids=[j for j in range(265900,26600)],
            # ids=["265984"]
        ).request()

        if result_task['result']:
            count += int(result_task['result']['total'])
            k = 0
            list_id = [get_id["id"] for get_id in result_task["result"]["list"]]
            for j in list_id:
                k += 1
    print(count)
    # print(i, "task_count",k,"capture_status = 0")
    # print(result_task['result'])
    # for j in list_id:
    #     del_id = DelAmazonKWM(
    #         ids=[j]
    #     ).request()
    #     print(del_id)

    # # print(result_task)
    # with engine.connect() as conn:
    #     for total_task in result_task['result']['list']:
    #         keyword_taskinfo = KeywordTaskInfo()
    #         infos = keyword_taskinfo.parse(total_task)
    #         insert_stmt = insert(amazon_keyword_task)
    #         onduplicate_key_stmt = insert_stmt.on_duplicate_key_update(
    #             id=insert_stmt.inserted.id,
    #             asin=insert_stmt.inserted.asin,
    #             keyword=insert_stmt.inserted.keyword,
    #             status=insert_stmt.inserted.status,
    #             monitoring_num=insert_stmt.inserted.monitoring_num,
    #             monitoring_count=insert_stmt.inserted.monitoring_count,
    #             monitoring_type=insert_stmt.inserted.monitoring_type,
    #             station=insert_stmt.inserted.station,
    #             start_time=insert_stmt.inserted.start_time,
    #             end_time=insert_stmt.inserted.end_time,
    #             created_at=insert_stmt.inserted.created_at,
    #             deleted_at=insert_stmt.inserted.deleted_at,
    #             is_add=insert_stmt.inserted.start_time,
    #             last_update=insert_stmt.inserted.last_update,
    #             capture_status=insert_stmt.inserted.capture_status,
    #             is_effect=insert_stmt.inserted.is_effect,
    #         )
    #         conn.execute(onduplicate_key_stmt, infos)


# def test_params(status):
#     if status == "jobs":
#         print("bingo")

# def update_db():
#     with engine.connect() as conn:
#         kar1 = KeywordTaskInfo()
#         kar = kar1.parse()
#         conn.execute(amazon_keyword_task.update().values(fullname=kar))
#


# def compare():
#     dict1 ={'code': 200, 'msg': 'success', 'result': [{'asin': 'B07V99B4Q1', 'keyword': 'iPhone 11 ケース クリア', 'keyword_list': [{'start_time': '2020-05-22 00:05:41.0', 'station': 3, 'asin': 'B07V99B4Q1', 'keyword': 'iPhone 11 ケース クリア', 'keyword_rank': 21, 'aid': 2774316}, {'start_time': '2020-05-22 12:18:04.0', 'station': 3, 'asin': 'B07V99B4Q1', 'keyword': 'iPhone 11 ケース クリア', 'keyword_rank': 34, 'aid': 2774416}]}]}
#
#     key = dict1['result'][0]['keyword_list']
#     key.sort(key=operator.itemgetter('start_time'), reverse=True)
#     print(key)


def get_shopee_pd():
    # with engine.connect() as conn:
    #     result_from_db = select(([amazon_keyword_task]))
    #     conn.execute()
    result = GetShopeeProductBySearch(
        station='MY',
        pids=['2450502604']
    ).request()
    print(result, "getstatus")


def get_amazon_pd():
    # with engine.connect() as conn:
    #     result_from_db = select(([amazon_keyword_task]))
    #     conn.execute()
    result = GetAmazonProductBySearch(
        station='US',
        asin='B00MJ7VL1O'
    ).request()
    print(json.dumps(result), "getstatus")


async def get_ebay_product():
    result = await GetEbayProductBySearch(
        'UK', current_page=2,
        item_ids=[], p_l1_id='2624',
        sales_week1_start=1,
        last_modi_time_start=datetime.now() - timedelta(days=14)
    ).aio_request(timeout=60, retry=4)
    print(json.dumps(result))


async def get_ebay_product_sku():
    result = await GetEbayProduct(
        'US', ['184593886423']
    ).aio_request(timeout=60, retry=4)
    print(json.dumps(result))


async def get_ebay_product_info():
    result = await GetEbayProductBySearch(
        'UK',
        item_ids=['363088900390']
    ).aio_request(timeout=60, retry=4)
    print(json.dumps(result))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_ebay_product_sku())