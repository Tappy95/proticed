import asyncio
import json
from datetime import datetime, timedelta

from sqlalchemy import create_engine, select, and_, or_
from sqlalchemy.dialects.mysql import insert

import pipeflow
from pipeflow import NsqInputEndpoint, NsqOutputEndpoint
from config_1 import *
from task_protocol import HYTask
from models.amazon_models import amazon_keyword_task, amazon_keyword_rank
from api.amazon_keyword import GetAmazonKWMStatus, AddAmazonKWM, GetAmazonKWMResult, DelAmazonKWM
from util.pub import pub_to_nsq

WORKER_NUMBER = 2
TOPIC_NAME = 'haiying.amazon.keyword'
NUM_OF_DAYS = 30
MONITORING_NUM = 4

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=SQLALCHEMY_POOL_PRE_PING,
    echo=SQLALCHEMY_ECHO,
    pool_size=SQLALCHEMY_POOL_SIZE,
    max_overflow=SQLALCHEMY_POOL_MAX_OVERFLOW,
    pool_recycle=SQLALCHEMY_POOL_RECYCLE,
)


class KeywordTaskInfo:
    station_map = {
        1: 'US',
        2: 'IT',
        3: 'JP',
        4: 'GE',
        5: 'UK',
        6: 'FR',
        7: 'ES',
        8: 'CA',
        9: 'AU',
    }

    def __init__(self):
        self.time_now = (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')

    def parse(self, info):
        parsed_info = {
            "id": info["id"],
            "asin": info["asin"],
            "keyword": info["keyword"],
            "status": info["status"],
            "monitoring_num": info["monitoring_num"],
            "monitoring_count": info["monitoring_count"],
            "monitoring_type": info["monitoring_type"],
            "station": self.station_map.get(info["station"]),
            "start_time": info["start_time"],
            "end_time": info["end_time"],
            "created_at": info["created_at"],
            "deleted_at": info["deleted_at"],
            "is_add": 1,
            "last_update": self.time_now,
            "capture_status": info["capture_status"],
        }
        return parsed_info


class KeywordRankInfo:

    def __init__(self, infos):
        self.infos = infos
        self.time_now = (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')

    # TODO: API不可用,这里写死了测试
    def parse(self, info):
        parsed_info = {
            "asin": info["asin"],
            "keyword": info["keyword"],
            # "site": KeywordTaskInfo.station_map.get(info['station']),
            "site": 'US',
            # "rank": info["keyword_rank"],
            "rank": 1,
            # "aid": info["aid"],
            "aid": 1,
            "update_time": self.time_now,
        }
        return parsed_info

    def parsed_infos(self, batch=1000):
        info_cnt = len(self.infos)
        i = 0
        while i < info_cnt:
            yield list(map(self.parse, self.infos[i:i + batch]))
            i += batch


# TODO:写完了,没优化...
def handle(group, task):
    # 获取NSQ中的任务参数(虚拟爬虫已经检查过rankdb中没有数据)
    hy_task = HYTask(task)
    site = hy_task.task_data['site']
    asin = hy_task.task_data['asin']
    keyword = hy_task.task_data['keyword']
    # 用任务参数查DB中的task表
    with engine.connect() as conn:
        select_task = select([amazon_keyword_task]) \
            .where(
            and_(
                amazon_keyword_task.c.station == site.upper(),
                amazon_keyword_task.c.asin == asin,
                amazon_keyword_task.c.keyword == keyword
            )
        )
        select_task_info = conn.execute(select_task)
        # 若task中存在此关键词监控任务
        if select_task_info:
            pass


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
            if row['capture_status'] ==6 or\
                (row['end_time'] - datetime.now()) <timedelta(days=5) or\
                datetime.now() - row['last_update'] > timedelta(days=4) or\
                    row['deleted_at'] is not None:
                invalid_id.append(row['id'])
        print(invalid_id)
        invalid_task = conn.execute(select([
            amazon_keyword_task.c.id,
            amazon_keyword_task.c.station,
            amazon_keyword_task.c.asin,
            amazon_keyword_task.c.keyword,
        ]).where(
            amazon_keyword_task.c.id.in_(invalid_id),
        )
        )
        return invalid_task

def db_classification_effect():
    # 返回有效任务对象
    with engine.connect() as conn:
        select_effect_task = conn.execute((select([
            amazon_keyword_task.c.id,
            amazon_keyword_task.c.end_time,
            amazon_keyword_task.c.capture_status,
        ]))).fetchall()
        effect_id = []
    for one in select_effect_task:
        # 距离任务结束大于五天
        if one['end_time'] is not None and one['end_time'] - datetime.now() > timedelta(days=5) \
                and one['capture_status'] != 6:
            # 状态不为已删除的任务
            effect_id.append(one['id'])
    return effect_id



def update_rank_db_by_effecttask(effect_data):
    # 更新rank表根据有效任务对象
    # effect_data = db_classification_effect()
    for an_id in effect_data:
        result_rank = GetAmazonKWMResult(
            ids=an_id,
            start_time=(datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),
            end_time=(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
        ).request()
        if result_rank and result_rank['msg'] == "success":
            print("获取关键词排名", result_rank['result'])
            with engine.connect() as conn:
                keyword_rank = KeywordRankInfo(result_rank.get("result", []))
                for infos in keyword_rank.parsed_infos():
                    insert_stmt = insert(amazon_keyword_rank)
                    on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
                        asin=insert_stmt.inserted.asin,
                        keyword=insert_stmt.inserted.keyword,
                        site=insert_stmt.inserted.site,
                        rank=insert_stmt.inserted.rank,
                        aid=insert_stmt.inserted.aid,
                        update_time=insert_stmt.inserted.update_time,
                    )
                    conn.execute(on_duplicate_key_stmt, infos)
                    print("更新amazon_rank成功")



def new_task_db_by_invalidtask(invalid_data):
    # 获取无效任务的参数,先删除API任务,再下新监控任务,再更新task_DB
    # invalid_data = db_classification_invalid()
    result_del = DelAmazonKWM(
        ids=[row['id'] for row in invalid_data],
    ).request()
    if result_del and result_del['msg'] == "success":
        for row in invalid_data:
            result_newtask = AddAmazonKWM(
                station=row['station'],
                asin_and_keywords=[{"asin": row['asin'], "keyword": row['keyword']}],
                num_of_days=NUM_OF_DAYS,
                monitoring_num=MONITORING_NUM,
            ).request()
            print("在HY创建监控任务", result_newtask)
            # 获取添加任务的ID,向海鹰获取监控商品信息
            if result_newtask and result_newtask["msg"] == "success":
                for one_task in result_newtask['result']:
                    result_task = GetAmazonKWMStatus(
                        station=row['station'],
                        capture_status=0,
                        ids=[one_task['id']],
                    ).request()
                    print("获取 任务ID", result_task)
                    if result_task['msg'] == "success":
                        for total_task in result_task['result']['list']:
                            keyword_taskinfo = KeywordTaskInfo()
                            print(total_task)
                            with engine.connect() as conn:
                                print(keyword_taskinfo.parse(total_task))
                                infos = keyword_taskinfo.parse(total_task)
                                insert_stmt = insert(amazon_keyword_task)
                                onduplicate_key_stmt = insert_stmt.on_duplicate_key_update(
                                    id=insert_stmt.inserted.id,
                                    asin=insert_stmt.inserted.asin,
                                    keyword=insert_stmt.inserted.keyword,
                                    status=insert_stmt.inserted.status,
                                    monitoring_num=insert_stmt.inserted.monitoring_num,
                                    monitoring_count=insert_stmt.inserted.monitoring_count,
                                    monitoring_type=insert_stmt.inserted.monitoring_type,
                                    station=insert_stmt.inserted.station,
                                    start_time=insert_stmt.inserted.start_time,
                                    end_time=insert_stmt.inserted.end_time,
                                    created_at=insert_stmt.inserted.created_at,
                                    deleted_at=insert_stmt.inserted.deleted_at,
                                    is_add=insert_stmt.inserted.start_time,
                                    last_update=insert_stmt.inserted.last_update,
                                    capture_status=insert_stmt.inserted.capture_status,
                                )
                                conn.execute(onduplicate_key_stmt, infos)
                        print("更新amazon_task成功{}".format(one_task['id']))



async def always_update_task():
    print("how to use")
    await create_hy_task()
    print("how totototo")

async def asy_test():
    print('asy_test')
    await print("aaa")




# 测试在nsq上发布任务
async def create_hy_task():
    sites = ['US']
    for site in sites:
        task = {
            "task": "haiying.amazon.keyword",
            "data": {
                "site": site,
                "asin": "B07KMM96GV",
                "keyword": "airjordans 11",
            }
        }
        print(json.dumps(task))
        await pub_to_nsq(NSQ_NSQD_HTTP_ADDR, TOPIC_NAME, json.dumps(task))

def run():
    input_end = NsqInputEndpoint(TOPIC_NAME, 'haiying_crawler', WORKER_NUMBER, **INPUT_NSQ_CONF)
    output_end = NsqOutputEndpoint(**OUTPUT_NSQ_CONF)

    server = pipeflow.Server()
    group = server.add_group('main', WORKER_NUMBER)
    group.set_handle(handle, "thread")
    group.add_input_endpoint('input', input_end)
    group.add_output_endpoint('output', output_end)

    # server.add_routine_worker(update_rank_db_by_effecttask, interval=2, immediately=True)
    server.add_routine_worker(create_hy_task, interval=2, immediately=True)
    print("run server")
    server.run()
    print("end")

if __name__ == '__main__':
    run()
