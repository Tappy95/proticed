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
            "last_update": "",
            "capture_status": info["capture_status"],
            "is_effect": 1,
            "update_time": "",
        }

        if info["status"] == -1 \
                or info["status"] == -2 \
                or info["deleted_at"] is not None \
                or info["capture_status"] == 6:
            parsed_info["is_effect"] = 0

        # if status == "add_task":
        #     parsed_info["last_update"] = self.time_now
        #     parsed_info["update_time"] = self.time_now
        # elif status == "update_task":
        #     parsed_info["update_time"] = self.time_now
        #     del parsed_info["last_update"]

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
            "update_time": info["start_time"]
        }
        return parsed_info


def task_db(result_task, status):
    if result_task['msg'] == "success":
        with engine.connect() as conn:
            total_task = result_task['result']['list'][0]
            keyword_taskinfo = KeywordTaskInfo()
            infos = keyword_taskinfo.parse(total_task, status)
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
                update_time=insert_stmt.inserted.update_time,
            )
            conn.execute(onduplicate_key_stmt, infos)


def handle(group, task):
    hy_task = HYTask(task)
    site = hy_task.task_data['site']
    asin = hy_task.task_data['asin']
    keyword = hy_task.task_data['keyword']

    # 查有效任务并对比
    with engine.connect() as conn:
        select_tasks = conn.execute(select([
            # index
            amazon_keyword_task.c.asin,
        ])
            .where(
            and_(
                amazon_keyword_task.c.station == site.upper(),
                amazon_keyword_task.c.asin == asin,
                amazon_keyword_task.c.keyword == keyword,
                amazon_keyword_task.c.is_effect == 1,
            )
        )).fetchall()
        # 无有效任务,重新下发任务
        if select_tasks == None:
            print("无此任务")
            result_newtask = AddAmazonKWM(
                station=site,
                asin_and_keywords=[{"asin": asin, "keyword": keyword}],
                num_of_days=NUM_OF_DAYS,
                monitoring_num=MONITORING_NUM,
            ).request()
            if result_newtask and result_newtask["msg"] == "success":
                get_id = result_newtask['result'][0]["id"]
                result_task = GetAmazonKWMStatus(
                    station=site,
                    ids=[get_id],
                ).request()
                task_db(result_task, "add_task")


async def get_result():
    with engine.connect() as conn:
        # 查有效任务拉rank结果
        select_effect = conn.execute(select([
            amazon_keyword_task.c.id,
            amazon_keyword_task.c.station,
        ])
            .where(
            and_(
                amazon_keyword_task.c.is_effect == 1,
            )
        )).fetchall()
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
                    keyword_rank = KeywordRankInfo()
                    infos = keyword_rank.parse(rank_time_sort[0])
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


async def maintain_task():
    with engine.connect() as conn:
        # 更新db中的有效task状态
        select_effect_task = conn.execute(select(
            [
                amazon_keyword_task.c.station,
                amazon_keyword_task.c.id,
            ]
        ).where(
            amazon_keyword_task.c.is_effect == 1
        )
        ).fetchall()
        if select_effect_task:
            for one_task in select_effect_task:
                result_task = GetAmazonKWMStatus(
                    station=one_task['station'],
                    ids=[one_task['id']]
                ).request()
                task_db(result_task, "update_task")

            # 远程删除HY所有无效task,并添加新task
            max_time = datetime.now() + timedelta(days=5)
            update_before = datetime.now() - timedelta(days=10)
            select_invalid = conn.execute(select(
                [
                    amazon_keyword_task.c.id,
                    amazon_keyword_task.c.asin,
                    amazon_keyword_task.c.keyword,
                    amazon_keyword_task.c.station
                ]
            ).where(
                and_(
                    amazon_keyword_task.c.is_effect == 1,
                    amazon_keyword_task.c.end_time < max_time,
                    amazon_keyword_task.c.last_update < update_before,
                )
            )).fetchall()
            if select_invalid:
                for invalid_data in select_invalid:
                    result_del = DelAmazonKWM(
                        ids=[invalid_data['id']],
                    ).request()
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
                                    ids=[one_task['id']],
                                ).request()
                                task_db(result_task, "add_task")


def run():
    input_end = NsqInputEndpoint(TOPIC_NAME, 'haiying_crawler', WORKER_NUMBER, **INPUT_NSQ_CONF)

    server = pipeflow.Server()
    group = server.add_group('main', WORKER_NUMBER)
    group.set_handle(handle)
    group.add_input_endpoint('input', input_end)

    server.add_routine_worker(maintain_task, interval=10, immediately=True)
    server.add_routine_worker(get_result, interval=60, immediately=True)
    server.run()


if __name__ == '__main__':
    run()