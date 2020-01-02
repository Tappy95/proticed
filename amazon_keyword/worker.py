import json
import operator
from datetime import datetime, timedelta

from sqlalchemy import create_engine, select, and_
from sqlalchemy.dialects.mysql import insert

import pipeflow
from pipeflow import NsqInputEndpoint
from config import *
from task_protocol import HYTask
from models.amazon_models import amazon_keyword_task, amazon_keyword_rank
from api.amazon_keyword import GetAmazonKWMStatus, AddAmazonKWM, GetAmazonKWMResult, DelAmazonKWM
from util.pub import pub_to_nsq

WORKER_NUMBER = 3
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

    def parse(self, info):
        parsed_info = {
            "asin": info["asin"],
            "keyword": info["keyword"],
            "site": KeywordTaskInfo.station_map.get(info['station']),
            "rank": info["keyword_rank"],
            "aid": info["aid"],
            "update_time": self.time_now,
        }
        return parsed_info

    def parsed_infos(self, batch=1000):
        info_cnt = len(self.infos)
        i = 0
        while i < info_cnt:
            yield list(map(self.parse, self.infos[i:i + batch]))
            i += batch


def handle(group, task):
    hy_task = HYTask(task)
    site = hy_task.task_data['site']
    asin = hy_task.task_data['asin']
    keyword = hy_task.task_data['keyword']

    with engine.connect() as conn:
        select_task = conn.execute(select([
            amazon_keyword_task.c.id
        ])
            .where(
            and_(
                amazon_keyword_task.c.station == site.upper(),
                amazon_keyword_task.c.asin == asin,
                amazon_keyword_task.c.keyword == keyword,
            )
        )).fetchall()

        if not select_task:
            result_newtask = AddAmazonKWM(
                station=site,
                asin_and_keywords=[{"asin": asin, "keyword": keyword}],
                num_of_days=NUM_OF_DAYS,
                monitoring_num=MONITORING_NUM,
            ).request()
            if result_newtask and result_newtask["msg"] == "success":
                for one_task in result_newtask['result']:
                    result_task = GetAmazonKWMStatus(
                        station=site,
                        capture_status=0,
                        ids=[one_task['id']],
                    ).request()
                    if result_task['msg'] == "success":
                        for total_task in result_task['result']['list']:
                            keyword_taskinfo = KeywordTaskInfo()
                            print(total_task)
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
                            return conn.execute(onduplicate_key_stmt, infos)
        else:
            effect_data = db_classification_effect()
            for a_result in select_task:
                if a_result['id'] in effect_data:
                    normal_always_update_rank()
                else:
                    normal_maintain_task_db()


def db_classification_invalid():
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

            if row['capture_status'] == None or \
                    row['capture_status'] == 6 or \
                    row['deleted_at'] is not None or \
                    (row['end_time'] - datetime.now()) < timedelta(days=5) or \
                    datetime.now() - row['last_update'] > timedelta(days=4):
                invalid_id.append(row['id'])

        print(invalid_id)
        for row in invalid_id:
            invalid_task = conn.execute(select([
                amazon_keyword_task.c.station,
                amazon_keyword_task.c.keyword,
                amazon_keyword_task.c.asin,
                amazon_keyword_task.c.id,
            ]).where(
                amazon_keyword_task.c.id == row,
            ))
            return invalid_task


def db_classification_effect():
    with engine.connect() as conn:
        select_effect_task = conn.execute((select([
            amazon_keyword_task.c.id,
            amazon_keyword_task.c.end_time,
            amazon_keyword_task.c.capture_status,
        ]))).fetchall()
        effect_id = []
    for one in select_effect_task:

        if one['end_time'] is not None and one['end_time'] - datetime.now() > timedelta(days=5) \
                and one['capture_status'] != 6:
            effect_id.append(one['id'])

    print(effect_id)
    return effect_id


def normal_always_update_rank():
    effect_data = db_classification_effect()
    for an_id in effect_data:

        result_rank = GetAmazonKWMResult(
            ids=[an_id],
            start_time=(datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),
            end_time=(datetime.now().replace(microsecond=0) - timedelta(days=7)) \
                .strftime('%Y-%m-%d %H:%M:%S'),
        ).request()

        if result_rank['result'] and result_rank['msg'] == "success":

            rank_time_sort = [rank_data for rank_data in result_rank['result'][0]['keyword_list']]
            rank_time_sort.sort(key=operator.itemgetter('start_time'))

            if rank_time_sort:
                with engine.connect() as conn:
                    keyword_rank = KeywordRankInfo(rank_time_sort[0])
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
                        return conn.execute(on_duplicate_key_stmt, infos)


def normal_maintain_task_db():
    invalid_data = db_classification_invalid()
    if invalid_data:
        for row in invalid_data:
            result_del = DelAmazonKWM(
                ids=[row['id']],
            ).request()
            print("del request")
            with engine.connect() as conn:
                conn.execute(amazon_keyword_task.delete() \
                             .where(amazon_keyword_task.c.id == row['id']))
            if result_del and result_del['msg'] == "success":
                result_newtask = AddAmazonKWM(
                    station=row['station'],
                    asin_and_keywords=[{"asin": row['asin'], "keyword": row['keyword']}],
                    num_of_days=NUM_OF_DAYS,
                    monitoring_num=MONITORING_NUM,
                ).request()

                if result_newtask and result_newtask["msg"] == "success":
                    for one_task in result_newtask['result']:

                        result_task = GetAmazonKWMStatus(
                            station=row['station'],
                            capture_status=0,
                            ids=[one_task['id']],
                        ).request()

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
                                    return conn.execute(onduplicate_key_stmt, infos)


async def always_update_rank():
    return normal_always_update_rank()


async def maintain_task_db():
    return normal_maintain_task_db()


def run():
    input_end = NsqInputEndpoint(TOPIC_NAME, 'haiying_crawler', WORKER_NUMBER, **INPUT_NSQ_CONF)

    server = pipeflow.Server()
    group = server.add_group('main', WORKER_NUMBER)
    group.set_handle(handle)
    group.add_input_endpoint('input', input_end)

    server.add_routine_worker(always_update_rank, interval=60 * 24, immediately=True)
    server.add_routine_worker(maintain_task_db, interval=60 * 24)
    server.run()



