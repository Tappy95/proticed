import operator
from datetime import datetime, timedelta

from sqlalchemy import create_engine, select, and_, or_, update
from sqlalchemy.dialects.mysql import insert

import pipeflow
from pipeflow import NsqInputEndpoint
from config import *
from task_protocol import HYTask
from models.amazon_models import amazon_keyword_task, amazon_keyword_rank
from api.amazon_keyword import GetAmazonKWMStatus, AddAmazonKWM, GetAmazonKWMResult, DelAmazonKWM

WORKER_NUMBER = 3
TOPIC_NAME = 'haiying.amazon.keyword'
NUM_OF_DAYS = 30
MONITORING_NUM = 24

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
            "is_effect": 1,
        }
        if info["status"] == -1 \
                or info["status"] == -2\
                or info["deleted_at"] is not None\
                or info["capture_status"] == 6:
            parsed_info["is_effect"] = 0

        return parsed_info


class KeywordRankInfo:

    def __init__(self):
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


class DataBaseSession:
    def __init__(self):
        self.conn = engine.connect()

    def __del__(self):
        self.conn.close()

    def update_rank_db(self, total_rank):
        keyword_rank = KeywordRankInfo()
        infos = keyword_rank.parse(total_rank)
        insert_stmt = insert(amazon_keyword_rank)
        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
            asin=insert_stmt.inserted.asin,
            keyword=insert_stmt.inserted.keyword,
            site=insert_stmt.inserted.site,
            rank=insert_stmt.inserted.rank,
            aid=insert_stmt.inserted.aid,
            update_time=insert_stmt.inserted.update_time,
        )
        return self.conn.execute(on_duplicate_key_stmt, infos)

    def update_task_db(self, total_task):
        keyword_taskinfo = KeywordTaskInfo()
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
            is_effect=insert_stmt.inserted.is_effect,
        )
        return self.conn.execute(onduplicate_key_stmt, infos)

    def effect(self):
        select_effect = self.conn.execute(select([
            amazon_keyword_task.c.id,
            amazon_keyword_task.c.station,
        ])
            .where(
            and_(
                amazon_keyword_task.c.is_effect == 1,
            )
        )).fetchall()
        return select_effect

    def invalid(self):
        max_time = datetime.now() + timedelta(days=5)
        update_before = datetime.now() - timedelta(days=4)
        select_invalid = self.conn.execute(select(
            [
                amazon_keyword_task.c.id,
                amazon_keyword_task.c.asin,
                amazon_keyword_task.c.keyword,
                amazon_keyword_task.c.station
            ]
        ).where(
            or_(
                amazon_keyword_task.c.end_time < max_time,
                amazon_keyword_task.c.last_update < update_before,
            )
        )).fetchall()
        return select_invalid


db_session = DataBaseSession()


def handle(group, task):
    hy_task = HYTask(task)
    site = hy_task.task_data['site']
    asins = hy_task.task_data['asin']
    keyword = hy_task.task_data['keyword']

    with engine.connect() as conn:
        select_tasks = conn.execute(select([
            amazon_keyword_task.c.asin,
        ])
            .where(
            and_(
                amazon_keyword_task.c.station == site.upper(),
                amazon_keyword_task.c.asin.in_(asins),
                amazon_keyword_task.c.keyword == keyword,
                amazon_keyword_task.c.is_effect == 1,
            )
        )).fetchall()
        update_asin = set([select_task["asin"] for select_task in select_tasks])
        add_asin = set(asins) - update_asin
        if add_asin:
            for a_asin in add_asin:
                result_newtask = AddAmazonKWM(
                    station=site,
                    asin_and_keywords=[{"asin": a_asin, "keyword": keyword}],
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
                                db_session.update_task_db(total_task)


async def get_result():
    select_effect = db_session.effect()
    for an_result in select_effect:
        an_id = an_result['id']
        result_rank = GetAmazonKWMResult(
            ids=[an_id],
            start_time=(datetime.now().replace(microsecond=0) - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S'),
            end_time=(datetime.now()).strftime('%Y-%m-%d %H:%M:%S'),
        ).request()
        if result_rank['result'] and result_rank['msg'] == "success":
            rank_time_sort = [rank_data for rank_data in result_rank['result'][0]['keyword_list']]
            rank_time_sort.sort(key=operator.itemgetter('start_time'))
            if rank_time_sort:
                db_session.update_rank_db(rank_time_sort[0])


async def maintain_task():
    select_effect = db_session.effect()

    for effect_data in select_effect:

        result_task = GetAmazonKWMStatus(
            station=effect_data['station'],
            capture_status=0,
            ids=[effect_data['id']]
        ).request()

        if result_task['msg'] == "success":
            for total_task in result_task['result']['list']:
                db_session.update_task_db(total_task)

    select_invalid = db_session.invalid()

    if select_invalid:
        for invalid_data in select_invalid:
            result_del = DelAmazonKWM(
                ids=[invalid_data['id']],
            ).request()
            with engine.connect() as conn:
                conn.execute(
                    update(amazon_keyword_task).where(
                        amazon_keyword_task.c.id == invalid_data["id"],
                    ).values(is_effect=0)
                )
            if result_del and result_del['msg'] == "success":
                result_newtask = AddAmazonKWM(
                    station=invalid_data['station'],
                    asin_and_keywords=[{"asin": invalid_data['asin'], "keyword": invalid_data['keyword']}],
                    num_of_days=NUM_OF_DAYS,
                    monitoring_num=MONITORING_NUM,
                ).request()

                if result_newtask and result_newtask["msg"] == "success":
                    for one_task in result_newtask['result']:

                        result_task = GetAmazonKWMStatus(
                            station=invalid_data['station'],
                            capture_status=0,
                            ids=[one_task['id']],
                        ).request()

                        if result_task['msg'] == "success":
                            for total_task in result_task['result']['list']:
                                db_session.update_task_db(total_task)


def run():
    input_end = NsqInputEndpoint(TOPIC_NAME, 'haiying_crawler', WORKER_NUMBER, **INPUT_NSQ_CONF)

    server = pipeflow.Server()
    group = server.add_group('main', WORKER_NUMBER)
    group.set_handle(handle)
    group.add_input_endpoint('input', input_end)

    server.add_routine_worker(maintain_task, interval=60, immediately=True)
    server.add_routine_worker(get_result, interval=60 * 12, immediately=True)
    server.run()

