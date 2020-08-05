import os
import sys

from sqlalchemy import text

sys.path.append('..')
from kafka_faust.product_calculate_worker import ProductData

import time
from decimal import Decimal
from typing import List

import faust
import asyncio
from datetime import datetime, timedelta
from collections import defaultdict
from aiomysql.sa import create_engine
from sqlalchemy.sql import select, and_, bindparam
from sqlalchemy.dialects.mysql import insert

from config import *
from models.amazon_models import amazon_category_history, wish_category_history, ebay_category_history


class BaseState:

    def show_diff(self, state):
        dct = state.to_representation()
        for k, v in self.to_representation().items():
            if k == '__faust':
                continue
            print("{}:\t{}\t=>\t{}".format(k, v, dct.get(k)))


class ProductResult(faust.Record, serializer='json', coerce=True, include_metadata=False):
    asin: str
    site: str
    date: str
    category_ids: List[str]
    sold_last_1: int
    sold_last_3: int
    sold_last_7: int
    sold_last_30: int
    gmv_last_1: Decimal
    gmv_last_3: Decimal
    gmv_last_7: Decimal
    gmv_last_30: Decimal


class CategoryResult(faust.Record, BaseState, serializer='json', coerce=True, include_metadata=False):
    # asin: str = ''
    # date: str = datetime.fromtimestamp(0, TZ_SH).strftime("%Y-%m-%d")
    date: str
    site: str
    category_id: str
    gmv_last_1: Decimal
    gmv_last_7: Decimal
    gmv_last_30: Decimal
    sold_last_1: int
    sold_last_7: int
    sold_last_30: int


class BaseCalculator:

    def __init__(self):
        self.count = 0

    def date_range(self, start, end):
        date = start
        while date <= end:
            yield date
            date = date + timedelta(days=1)

    def str_to_datetime(self, date_str):
        return datetime.strptime(date_str, "%Y-%m-%d")

    def datetime_to_str(self, date):
        return date.strftime("%Y-%m-%d")

    def incre(self):
        self.count += 1

    def reset_count(self):
        self.count = 0


class CategoryCalculator(BaseCalculator):
    def __init__(self, state_table):
        self.state_table = state_table
        super().__init__()

    def initialize(self, key, category_data):
        self.state_key = key
        self.category_info = self.state_table[key]
        self.category_data = category_data

    def update_state(self, category_data):
        if self.category_info.date:
            if self.category_info.date == category_data.date:
                self.category_info.gmv_last_1 += category_data.gmv_last_1
                self.category_info.gmv_last_7 += category_data.gmv_last_7
                self.category_info.gmv_last_30 += category_data.gmv_last_30
                self.category_info.sold_last_1 += category_data.sold_last_1
                self.category_info.sold_last_7 += category_data.sold_last_7
                self.category_info.sold_last_30 += category_data.sold_last_30

    def calculate(self, key, category_data):
        self.incre()
        self.initialize(key, category_data)
        # print("--------shop data %s" % self.category_data)
        if self.category_info.date > self.category_data.date:
            return
        # ori_state = copy.deepcopy(self.category_info)
        self.update_state(category_data)
        # TODO: if state is change or not
        new_state = CategoryResult(
            date=category_data.date,
            site=category_data.site,
            category_id=key,
            gmv_last_1=self.category_info.gmv_last_1,
            gmv_last_7=self.category_info.gmv_last_7,
            gmv_last_30=self.category_info.gmv_last_30,
            sold_last_1=self.category_info.sold_last_1,
            sold_last_7=self.category_info.sold_last_7,
            sold_last_30=self.category_info.sold_last_30,
        )
        # print("--------new product info")
        # ori_state.show_diff(new_state)
        self.state_table[self.state_key] = new_state
        yield new_state


default_category_state = lambda: CategoryResult(
    date='',
    site='',
    category_id='',
    gmv_last_1=Decimal(0),
    gmv_last_7=Decimal(0),
    gmv_last_30=Decimal(0),
    sold_last_1=0,
    sold_last_7=0,
    sold_last_30=0,
)

engine = None

app = faust.App('amazon-category-into-db', broker='kafka://47.112.96.218:9092',
                topic_partitions=1, topic_replication_factor=1)

product_result_topic = app.topic('amazon-product-result', value_type=ProductResult)
category_result_topic = app.topic('amazon-category-result', value_type=CategoryResult)
category_info_table = app.Table('amazon-category-infos',
                                default=default_category_state,
                                key_type=str, value_type=CategoryResult)

# @app.agent(product_result_topic, concurrency=2)
# async def category_calculate(stream):
#     # 创建计算对象
#     calculator = CategoryCalculator(category_info_table)
#
#     # 标记起始时间
#     start_time = time.time()
#
#     # 获取流
#     async for product_info in stream:
#         dct = product_info.to_representation()
#         # 处理stream data
#         for category_id in dct['category_ids']:
#             for category_result in calculator.calculate(category_id, product_info):
#                 # 发送result到另一topic
#                 await category_result_topic.send(value=category_result)
#         now_time = time.time()
#         if start_time + 10 < now_time:
#             # 计算处理速度
#             print("speed: {}".format(calculator.count / (now_time - start_time)))
#             start_time = now_time
#
#
# @app.agent(category_result_topic, concurrency=2)
# async def save_category_result(stream):
#     parsed_results = []
#     async for results in stream.take(10, within=10):
#         parsed_results.clear()
#         for result in results:
#             dct = result.to_representation()
#             parsed_results.append(dct)
#         # save category result
#         async with engine.acquire() as conn:
#             # save category history
#             insert_stmt = insert(amazon_category_history)
#             on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
#                 category_id=insert_stmt.inserted.category_id,
#                 site=insert_stmt.inserted.site,
#                 date=insert_stmt.inserted.date,
#                 sold_last_1=insert_stmt.inserted.sold_last_1,
#                 # sold_last_3=insert_stmt.inserted.sold_last_3,
#                 sold_last_7=insert_stmt.inserted.sold_last_7,
#                 sold_last_30=insert_stmt.inserted.sold_last_30,
#                 gmv_last_1=insert_stmt.inserted.gmv_last_1,
#                 # gmv_last_3=insert_stmt.inserted.gmv_last_3,
#                 gmv_last_7=insert_stmt.inserted.gmv_last_7,
#                 gmv_last_30=insert_stmt.inserted.gmv_last_30
#             )
#             await conn.execute(on_duplicate_key_stmt, parsed_results)


# @app.agent(product_result_topic, concurrency=1)
# async def save_category_statistics(stream):
#     category_map = {}
#     async for results in stream.take(10, within=10):
#         category_map.clear()
#         for result in results:
#             for category_id in result.category_ids:
#                 ls = category_map.setdefault((category_id, result.site, result.date),
#                                              [0, 0, 0, Decimal('0.00'), Decimal('0.00'), Decimal('0.00')])
#                 ls[0] += result.sold_last_1
#                 ls[1] += result.sold_last_3
#                 ls[2] += result.sold_last_7
#                 ls[3] += result.gmv_last_1
#                 ls[4] += result.gmv_last_3
#                 ls[5] += result.gmv_last_7
#         parsed_results = [
#             {
#                 "category_id": category_id,
#                 "site": site,
#                 "date": date,
#                 "sold_last_1": ls[0],
#                 "sold_last_3": ls[1],
#                 "sold_last_7": ls[2],
#                 "gmv_last_1": ls[3],
#                 "gmv_last_3": ls[4],
#                 "gmv_last_7": ls[5]
#             }
#             for (category_id, site, date), ls in category_map.items()
#         ]
#         # save product result
#         async with engine.acquire() as conn:
#             # save product history
#             insert_stmt = insert(ebay_category_history)
#             on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
#                 sold_last_1=text("sold_last_1+VALUES(sold_last_1)"),
#                 sold_last_3=text("sold_last_3+VALUES(sold_last_3)"),
#                 sold_last_7=text("sold_last_7+VALUES(sold_last_7)"),
#                 gmv_last_1=text("gmv_last_1+VALUES(gmv_last_1)"),
#                 gmv_last_3=text("gmv_last_3+VALUES(gmv_last_3)"),
#                 gmv_last_7=text("gmv_last_7+VALUES(gmv_last_7)")
#             )
#             await conn.execute(on_duplicate_key_stmt, parsed_results)

# @app.timer(interval=0.1)
# async def example_sender(app):
#     await product_result_topic.send(
#         value=ProductResult(
#             asin="B0075AJW0M",
#             site="us",
#             date="2020-07-10",
#             category_ids=[
#                 "12898451",
#                 "12898561",
#                 "2617941011"
#             ],
#             sold_last_1=21,
#             sold_last_3=44,
#             sold_last_7=62,
#             sold_last_30=176,
#             gmv_last_1=3002.19,
#             gmv_last_3=1230.12,
#             gmv_last_7=25467.78,
#             gmv_last_30=49376.82,
#         )
#     )


product_data_topic = app.topic('ebay-product-data1', key_type=str,
                               value_type=ProductData)

update_time = datetime(2020, 7, 29, 0, 1)
data_update_time = datetime(2020, 7, 30, 0, 32, 21)
timestamp = 1596181575
sold = 99
@app.timer(interval=4)
async def example_sender(app):
    global update_time, data_update_time, timestamp,sold
    update_time += timedelta(days=1)
    data_update_time += timedelta(days=1)
    timestamp += 86400
    sold += 10
    print(data_update_time)
    message = ProductData(
            timestamp=timestamp, item_id='263548829995', site='uk', brand='Unbranded', seller='anjoe1990',
            category_ids=['63862', '11450', '15724'], leaf_category_ids=['63862'],
            category_paths=["Clothing, Shoes & Accessories - Men's Clothing - Activewear - Activewear Tops",
                            "Clothing, Shoes & Accessories - Women's Clothing - Intimates & Sleep - Shapewear"],
            category_l1_ids=["1233", "222"],
            category_l2_ids=["444"],
            category_l3_ids=["9384", "11"],
            price=Decimal('74.01'), visit=sold, sold=sold,
            img="https://i.ebayimg.com/00/s/NzUwWDc1MA==/z/8egAAOSwwz9dLB6A/$_12.JPG?set_id=880000500F",
            title="Womens Winter  Long Woolen Coat Ladies Loose Sheep Sheared Overcoat Hot Jacket",
            item_location="CN,Cheng Du",
            item_location_country="CN",
            store="anjoe1990", store_location="CN", marketplace="EBAY-GB", popular=False,
            update_time=update_time,
            gen_time=datetime(2019, 10, 5, 11, 1, 43),
            data_update_time=data_update_time)
    print(message)
    await product_data_topic.send(
        value=message,
        key='uk' + '263548829995'
    )


# async def db_engine_init():
#     global engine
#     engine = await create_engine(echo=SQLALCHEMY_ECHO, pool_recycle=SQLALCHEMY_POOL_RECYCLE,
#                                  user=DB_USER_NAME, db=DB_DATABASE_NAME,
#                                  host=DB_SEVER_ADDR, port=DB_SEVER_PORT, password=DB_USER_PW,
#                                  autocommit=AUTOCOMMIT,
#                                  maxsize=10)


# @app.on_before_shutdown.connect
# async def close(app, **kwargs):
#     engine.close()
#     await engine.wait_closed()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(db_engine_init())
    app.main()
