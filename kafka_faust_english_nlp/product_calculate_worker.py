import json
import sys
import time
import faust
import asyncio
from decimal import Decimal
from datetime import datetime

sys.path.append('..')

from config import *
from util.log import logger

engine = None

import faust
from typing import List, Dict, Optional, Any
from decimal import Decimal
from datetime import datetime
from config import *


class BaseState:

    def show_diff(self, state):
        dct = state.to_representation()
        for k, v in self.to_representation().items():
            if k == '__faust':
                continue
            print("{}:\t{}\t=>\t{}".format(k, v, dct.get(k)))


class ProductTask(faust.Record, serializer='json', coerce=True):
    batch_time: datetime
    site: str
    item_ids: list = []
    category_id: str = ''


class SdkProductTask(faust.Record, serializer='json', coerce=True, include_metadata=False):
    batch_time: datetime
    site: str
    item_id: str


class ProductData(faust.Record, serializer='json', coerce=True):
    timestamp: int = 0
    item_id: str = ''
    site: str = ''
    brand: str = ''
    seller: str = ''
    category_ids: List[str] = []
    leaf_category_ids: List[str] = []
    category_paths: List[str] = []
    category_l1_ids: List[str] = []
    category_l2_ids: List[str] = []
    category_l3_ids: List[str] = []
    price: Decimal = Decimal(0)
    visit: int = 0
    sold: int = 0
    img: str = ''
    title: str = ''
    item_location: str = ''
    item_location_country: str = ''
    store: str = ''
    store_location: str = ''
    marketplace: str = ''
    popular: bool = False
    update_time: datetime = datetime.strptime("1970-01-03", "%Y-%m-%d")
    gen_time: Optional[datetime] = None
    data_update_time: Optional[datetime] = None


class ProductState(faust.Record, BaseState, serializer='json', coerce=True):
    # item_id: str = ''
    # date: str = datetime.fromtimestamp(0, TZ_SH).strftime("%Y-%m-%d")
    date: str
    timestamp: int
    batch_num: int
    price: Decimal
    new_last: List[int]
    sold_total_last: List[int]
    sold_last: List[int]
    visit_total_last: List[int]
    visit_last: List[int]
    gmv_last: List[Decimal]
    first_date: Optional[str]


default_product_state = lambda: ProductState(
    date='',
    timestamp=0,
    batch_num=0,
    price=Decimal(0),
    new_last=[0] * PRODUCT_PERIODS,
    sold_total_last=[0] * PRODUCT_TOTAL_PERIODS,
    sold_last=[0] * PRODUCT_PERIODS,
    visit_total_last=[0] * PRODUCT_TOTAL_PERIODS,
    visit_last=[0] * PRODUCT_PERIODS,
    gmv_last=[Decimal(0)] * PRODUCT_PERIODS
)


class ProductResult(faust.Record, serializer='json', coerce=True):
    item_id: str
    site: str
    date: str
    brand: str
    seller: str
    category_ids: List[str]
    leaf_category_ids: List[str]
    category_paths: List[str]
    category_l1_ids: List[str]
    category_l2_ids: List[str]
    category_l3_ids: List[str]
    price: Decimal
    visit: int
    sold: int
    img: str
    title: str
    item_location: str
    item_location_country: str
    store: str
    store_location: str
    marketplace: str
    popular: bool
    update_time: datetime
    sold_total: int
    sold_last_1: int
    sold_last_3: int
    sold_last_7: int
    sold_last_30: int
    pre_sold_last_1: int
    pre_sold_last_3: int
    pre_sold_last_7: int
    sold_last_1_delta: int
    sold_last_3_delta: int
    sold_last_7_delta: int
    sold_last_1_pop: float
    sold_last_3_pop: float
    sold_last_7_pop: float
    sold_2_to_last: int
    sold_3_to_last: int
    sold_4_to_last: int
    sold_5_to_last: int
    sold_6_to_last: int
    sold_7_to_last: int
    gmv_last_1: Decimal
    gmv_last_3: Decimal
    gmv_last_7: Decimal
    gmv_last_30: Decimal
    pre_gmv_last_1: Decimal
    pre_gmv_last_3: Decimal
    pre_gmv_last_7: Decimal
    gmv_last_1_delta: Decimal
    gmv_last_3_delta: Decimal
    gmv_last_7_delta: Decimal
    gmv_last_1_pop: float
    gmv_last_3_pop: float
    gmv_last_7_pop: float
    gmv_2_to_last: Decimal
    gmv_3_to_last: Decimal
    gmv_4_to_last: Decimal
    gmv_5_to_last: Decimal
    gmv_6_to_last: Decimal
    gmv_7_to_last: Decimal
    visit_total: int
    visit_last_1: int
    visit_last_3: int
    visit_last_7: int
    cvr_total: float
    cvr_last_1: float
    cvr_last_3: float
    cvr_last_7: float
    new_last_1: int
    new_last_3: int
    new_last_7: int
    gen_time: Optional[datetime]
    data_update_time: Optional[datetime]


import copy
import time
import random
import functools
from decimal import Decimal
from datetime import datetime, timedelta
from config import *


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


class ProductCalculator(BaseCalculator):

    def __init__(self, state_table):
        self.state_table = state_table
        super().__init__()

    def initialize(self, key, product_data):
        self.state_key = key
        self.product_info = self.state_table[key]
        # completion
        original_periods_check = len(self.product_info.sold_last)
        if not self.product_info.first_date:
            self.product_info.first_date = ""
        if len(self.product_info.sold_last) != PRODUCT_PERIODS:
            for i in range(PRODUCT_PERIODS-original_periods_check):
                self.product_info.sold_last.insert(0, 0)
                self.product_info.visit_last.insert(0, 0)
                self.product_info.gmv_last.insert(0, Decimal('0.00'))
        original_periods = len(self.product_info.sold_last)
        sold_total_periods = len(self.product_info.sold_total_last)
        visit_total_periods = len(self.product_info.visit_total_last)
        print("ori:{},sold_total:{}, visit_total:{}".format(original_periods, sold_total_periods, visit_total_periods))
        self.product_info.date_ls = [self.product_info.date] * original_periods
        self.product_info.sold_total_last = [0] * (original_periods - sold_total_periods) \
                                            + self.product_info.sold_total_last
        self.product_info.visit_total_last = [0] * (original_periods - visit_total_periods) \
                                             + self.product_info.visit_total_last
        self.product_info.price_last = [self.product_info.price] * original_periods
        # set date
        self.product_data = product_data
        self.product_data.date = datetime.fromtimestamp(self.product_data.timestamp, TZ_SH) \
            .strftime("%Y-%m-%d")
        # self.product_data.batch_num = (int(time.time()) + 8 * 3600) // 86400
        self.product_data.batch_num = int(self.product_data.update_time.timestamp())
        self.calculate_indexes = set([])

    def all_product_data(self, product_data):
        product_data_ls = [product_data]
        if self.product_info.date:
            date_start = self.str_to_datetime(self.product_info.date)
            date_end = self.str_to_datetime(product_data.date)
            price_start = self.product_info.price
            sold_start = self.product_info.sold_total_last[-1]
            visit_start = self.product_info.visit_total_last[-1]
            date_ls = list(self.date_range(date_start, date_end))
            if len(date_ls) > 1:
                price_deltas = self.deltas_generator(price_start, product_data.price,
                                                     len(date_ls) - 1, 'decimal')
                sold_deltas = self.deltas_generator(sold_start, product_data.sold,
                                                    len(date_ls) - 1, 'int')
                visit_deltas = self.deltas_generator(visit_start, product_data.visit,
                                                     len(date_ls) - 1, 'int')
                for i, date in enumerate(date_ls[1:]):
                    date_str = self.datetime_to_str(date)
                    price_start += price_deltas[i]
                    sold_start += sold_deltas[i]
                    visit_start += visit_deltas[i]
                    if date_str != product_data.date:
                        data = ProductData(price=price_start, sold=sold_start,
                                           visit=visit_start)
                        data.date = date_str
                        product_data_ls.append(data)
        product_data_ls.sort(key=lambda x: x.date)
        return product_data_ls

    def update_state(self, product_data_ls):
        product_data = product_data_ls[-1]
        original_periods = len(self.product_info.sold_last)
        new_start = self.str_to_datetime(product_data.date)
        if self.product_info.date:
            new_start = self.str_to_datetime(self.product_info.date) + timedelta(days=1)
        else:
            self.product_info.sold_total_last[-1] = product_data.sold
            self.product_info.visit_total_last[-1] = product_data.visit
        new_end = self.str_to_datetime(product_data.date)
        for date in self.date_range(new_start, new_end):
            self.product_info.date_ls.append(self.datetime_to_str(date))
            self.product_info.new_last.append(0)
            self.product_info.sold_total_last.append(0)
            self.product_info.visit_total_last.append(0)
            self.product_info.price_last.append(Decimal(0))
            self.product_info.sold_last.append(0)
            self.product_info.visit_last.append(0)
            self.product_info.gmv_last.append(Decimal(0))
        for i in range(original_periods):
            date_str = self.datetime_to_str(new_start + timedelta(days=i - original_periods))
            self.product_info.date_ls[i] = date_str
        date_index_map = {date: i for i, date in enumerate(self.product_info.date_ls)}

        product_data_cnt = len(product_data_ls)
        for i, product_data in enumerate(product_data_ls):
            index = date_index_map[product_data.date]
            total_sold_delta = product_data.sold - self.product_info.sold_total_last[index]
            self.product_info.sold_total_last[index] = product_data.sold
            self.product_info.visit_total_last[index] = product_data.visit
            self.product_info.price_last[index] = product_data.price
            cur_sold = product_data.sold - self.product_info.sold_total_last[index - 1]
            print("cur_sold:{},product_data_sold:{},sold_total_list:{}".format(cur_sold, product_data.sold, self.product_info.sold_total_last))
            cur_visit = product_data.visit - self.product_info.visit_total_last[index - 1]
            cur_gmv = product_data.price * cur_sold
            # generate deltas and calculate result only on real data
            if i == product_data_cnt - 1:
                self.calculate_indexes.add(index)
                is_new = True if not self.product_info.date \
                                 or self.str_to_datetime(self.product_info.date) + timedelta(days=10) \
                                 < self.str_to_datetime(product_data.date) else False
                if is_new:
                    self.product_info.new_last[index] = 1
            self.product_info.sold_last[index] = cur_sold
            self.product_info.visit_last[index] = cur_visit
            self.product_info.gmv_last[index] = cur_gmv

    def calculate(self, key, product_data):
        self.incre()
        if EFFICIENT_SECOND_LIMIT + product_data.timestamp < time.time():
            print("efficient_limit")
            return
        self.initialize(key, product_data)
        # print("--------product data %s" % self.product_data)
        if self.product_info.batch_num == self.product_data.batch_num:
            print("batch_num")
            return
        if sum(self.product_info.sold_last[-3:]) > 3 \
                and self.product_data.timestamp + 86400 < time.time():
            yield SdkProductTask(batch_time=self.product_data.update_time,
                                 site=self.product_data.site,
                                 item_id=self.product_data.item_id)
            return
        if self.product_info.timestamp > self.product_data.timestamp:
            print("stable time:{} > data time".format(self.product_info.date))
            return
        ori_state = copy.deepcopy(self.product_info)
        if self.product_info.timestamp >= self.product_data.timestamp:
            self.calculate_indexes.add(len(self.product_info.sold_last) - 1)
        else:
            product_data_ls = self.all_product_data(self.product_data)
            self.update_state(product_data_ls)
        # TODO: if state is change or not
        print("update stable")
        print("stable sold_last_list:{}".format(self.product_info.sold_last))
        new_state = ProductState(date=self.product_info.date_ls[-1],
                                 timestamp=max(self.product_data.timestamp, self.product_info.timestamp),
                                 batch_num=self.product_data.batch_num,
                                 price=self.product_info.price_last[-1],
                                 new_last=self.product_info.new_last[-1 * PRODUCT_PERIODS:],
                                 sold_total_last=self.product_info.sold_total_last[-1 * PRODUCT_TOTAL_PERIODS:],
                                 visit_total_last=self.product_info.visit_total_last[-1 * PRODUCT_TOTAL_PERIODS:],
                                 sold_last=self.product_info.sold_last[-1 * PRODUCT_PERIODS:],
                                 visit_last=self.product_info.visit_last[-1 * PRODUCT_PERIODS:],
                                 gmv_last=self.product_info.gmv_last[-1 * PRODUCT_PERIODS:],
                                 first_date=self.product_info.first_date if self.product_info.first_date else self.product_info.date_ls[-1])
        # print("--------new product info")
        ori_state.show_diff(new_state)
        self.state_table[self.state_key] = new_state
        for result in map(self.convert_to_result, self.calculate_indexes):
            yield result

    def calculated_info(self, state, i, day_delta):
        print("before calculate stable:{}".format(self.product_info.sold_last))
        if day_delta < 30:
            ls = list(filter(lambda x:x[1]>0, enumerate(state.sold_last)))
            if ls:
                index = ls[0][0]
                sold = state.sold_last[index]
                gmv = state.gmv_last[index]
                for n in range(min(index, max(len(state.sold_last)-day_delta, 0))):
                    state.sold_last[n] = sold
                    state.gmv_last[n] = gmv
        print("last before calculate stable:{}".format(self.product_info.sold_last))
        sold_last_30 = sum(state.sold_last[i - 29:i + 1])
        gmv_last_30 = sum(state.gmv_last[i - 29:i + 1])
        pre_sold_last_1, sold_last_1 = state.sold_last[i - 1], state.sold_last[i],
        pre_sold_last_3, sold_last_3 = sum(state.sold_last[i - 3:i]), sum(state.sold_last[i - 2:i + 1])
        pre_sold_last_7, sold_last_7 = sum(state.sold_last[i - 7:i]), sum(state.sold_last[i - 6:i + 1])
        pre_gmv_last_1, gmv_last_1 = state.gmv_last[i - 1], state.gmv_last[i],
        pre_gmv_last_3, gmv_last_3 = sum(state.gmv_last[i - 3:i]), sum(state.gmv_last[i - 2:i + 1])
        pre_gmv_last_7, gmv_last_7 = sum(state.gmv_last[i - 7:i]), sum(state.gmv_last[i - 6:i + 1])
        visit_last_1 = state.visit_last[i]
        visit_last_3 = sum(state.visit_last[i - 2:i + 1])
        visit_last_7 = sum(state.visit_last[i - 6:i + 1])
        new_last_1 = int(any(state.new_last[i:i + 1]))
        new_last_3 = int(any(state.new_last[i - 2:i + 1]))
        new_last_7 = int(any(state.new_last[i - 6:i + 1]))
        return {
            "sold_total": state.sold_total_last[i],
            "sold_last_1": sold_last_1,
            "sold_last_3": sold_last_3,
            "sold_last_7": sold_last_7,
            "sold_last_30": sold_last_30,
            "pre_sold_last_1": pre_sold_last_1,
            "pre_sold_last_3": pre_sold_last_3,
            "pre_sold_last_7": pre_sold_last_7,
            "sold_last_1_delta": sold_last_1 - pre_sold_last_1,
            "sold_last_3_delta": sold_last_3 - pre_sold_last_3,
            "sold_last_7_delta": sold_last_7 - pre_sold_last_7,
            "sold_last_1_pop": round((sold_last_1 - pre_sold_last_1) / pre_sold_last_1 if pre_sold_last_1 else 0, 6),
            "sold_last_3_pop": round((sold_last_3 - pre_sold_last_3) / pre_sold_last_3 if pre_sold_last_3 else 0, 6),
            "sold_last_7_pop": round((sold_last_7 - pre_sold_last_7) / pre_sold_last_7 if pre_sold_last_7 else 0, 6),
            "sold_2_to_last": state.sold_last[i - 1],
            "sold_3_to_last": state.sold_last[i - 2],
            "sold_4_to_last": state.sold_last[i - 3],
            "sold_5_to_last": state.sold_last[i - 4],
            "sold_6_to_last": state.sold_last[i - 5],
            "sold_7_to_last": state.sold_last[i - 6],
            "gmv_last_1": gmv_last_1,
            "gmv_last_3": gmv_last_3,
            "gmv_last_7": gmv_last_7,
            "gmv_last_30": gmv_last_30,
            "pre_gmv_last_1": pre_gmv_last_1,
            "pre_gmv_last_3": pre_gmv_last_3,
            "pre_gmv_last_7": pre_gmv_last_7,
            "gmv_last_1_delta": gmv_last_1 - pre_gmv_last_1,
            "gmv_last_3_delta": gmv_last_3 - pre_gmv_last_3,
            "gmv_last_7_delta": gmv_last_7 - pre_gmv_last_7,
            "gmv_last_1_pop": round(float((gmv_last_1 - pre_gmv_last_1) / pre_gmv_last_1 if pre_gmv_last_1 else 0), 6),
            "gmv_last_3_pop": round(float((gmv_last_3 - pre_gmv_last_3) / pre_gmv_last_3 if pre_gmv_last_3 else 0), 6),
            "gmv_last_7_pop": round(float((gmv_last_7 - pre_gmv_last_7) / pre_gmv_last_7 if pre_gmv_last_7 else 0), 6),
            "gmv_2_to_last": state.gmv_last[i - 1],
            "gmv_3_to_last": state.gmv_last[i - 2],
            "gmv_4_to_last": state.gmv_last[i - 3],
            "gmv_5_to_last": state.gmv_last[i - 4],
            "gmv_6_to_last": state.gmv_last[i - 5],
            "gmv_7_to_last": state.gmv_last[i - 6],
            "visit_total": state.visit_total_last[i],
            "visit_last_1": visit_last_1,
            "visit_last_3": visit_last_3,
            "visit_last_7": visit_last_7,
            "cvr_total": round(state.sold_total_last[i] / state.visit_total_last[i] if state.visit_total_last[i] else 0,
                               6),
            "cvr_last_1": round(sold_last_1 / visit_last_1 if visit_last_1 else 0, 6),
            "cvr_last_3": round(sold_last_3 / visit_last_3 if visit_last_3 else 0, 6),
            "cvr_last_7": round(sold_last_7 / visit_last_7 if visit_last_7 else 0, 6),
            "new_last_1": new_last_1,
            "new_last_3": new_last_3,
            "new_last_7": new_last_7
        }

    def convert_to_result(self, i):
        date = self.product_info.date_ls[i]
        day_delta = 0
        if self.product_info.first_date:
            td = datetime.strptime(date, "%Y-%m-%d") - datetime.strptime(self.product_info.first_date, "%Y-%m-%d")
            day_delta = td.days
        info = self.calculated_info(self.product_info, i, day_delta)
        return ProductResult(
            item_id=self.product_data.item_id, site=self.product_data.site, date=date,
            brand=self.product_data.brand,
            seller=self.product_data.seller,
            category_ids=self.product_data.category_ids,
            leaf_category_ids=self.product_data.leaf_category_ids,
            category_paths=self.product_data.category_paths,
            category_l1_ids=self.product_data.category_l1_ids,
            category_l2_ids=self.product_data.category_l2_ids,
            category_l3_ids=self.product_data.category_l3_ids,
            price=self.product_info.price_last[i],
            visit=self.product_data.visit,
            sold=self.product_data.sold,
            img=self.product_data.img,
            title=self.product_data.title,
            item_location=self.product_data.item_location,
            item_location_country=self.product_data.item_location_country,
            store=self.product_data.store,
            store_location=self.product_data.store_location,
            marketplace=self.product_data.marketplace,
            popular=self.product_data.popular,
            update_time=self.product_data.update_time,
            gen_time=self.product_data.gen_time,
            data_update_time=self.product_data.data_update_time,
            **info)

    def deltas_generator(self, start, end, period_num, delta_type='int'):
        total_delta = end - start
        if delta_type == 'decimal':
            assert isinstance(total_delta, Decimal)
            delta = round(total_delta / period_num, 2)
            deltas = [delta] * (period_num - 1)
            deltas.append(total_delta - sum(deltas))
            return deltas
        elif delta_type == 'int':
            assert isinstance(total_delta, int)
            deltas = [total_delta // period_num] * period_num
            for i in random.sample(range(len(deltas)), total_delta % period_num):
                deltas[i] += 1
            return deltas


app = faust.App('ebay-product-calculate', broker="kafka://47.112.96.218:9092", store='rocksdb://',
                topic_replication_factor=1,
                topic_partitions=1)
'''
@app.on_configured.connect
def configure(app, conf, **kwargs):
    conf.topic_replication_factor = TOPIC_REPLICATION
    conf.topic_partitions = TOPIC_PARTITION
'''

product_data_topic = app.topic('ebay-product-data1', key_type=str,
                               value_type=ProductData)
product_info_table = app.Table('ebay-product-infos14',
                               default=default_product_state,
                               key_type=str, value_type=ProductState
                               )
product_result_topic = app.topic('ebay-product-result', value_type=ProductResult)


@app.agent(product_data_topic, concurrency=1)
async def product_calculate(stream):
    calculator = ProductCalculator(product_info_table)
    start_time = time.time()
    async for key, product_data in stream.items():
        for product_result in calculator.calculate(key, product_data):
            print(product_result)
            print(product_info_table['uk263548829995'])
            # if isinstance(product_result, ProductResult):
            #     await product_result_topic.send(value=product_result)
            # else:
            #     await sdk_task_topic.pub(product_result.dumps())
        now_time = time.time()
        if start_time + 10 < now_time:
            print("speed: {}".format(calculator.count / (now_time - start_time)))
            calculator.reset_count()
            start_time = now_time


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    app.main()
