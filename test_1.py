import json
import operator
from datetime import datetime, timedelta

from sqlalchemy import create_engine, select, and_, or_
from sqlalchemy.dialects.mysql import insert

import pipeflow
from amazon_keyword.worker import KeywordTaskInfo
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


class Classification:
    def __init__(self):
        self.conn = engine.connect()

    def __del__(self):
        self.conn.close()


    def update_task_db(self, total_task):
        keyword_taskinfo = KeywordTaskInfo()
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
        return self.conn.execute(onduplicate_key_stmt, infos)

    def effect(self):
        select_effect_task = self.conn.execute(select([
            amazon_keyword_task.c.id,
            amazon_keyword_task.c.end_time,
            amazon_keyword_task.c.capture_status,
        ])).fetchall()
        effect_id = []
        for one in select_effect_task:

            if one['end_time'] is not None and one['end_time'] - datetime.now() > timedelta(days=5) \
                    and one['capture_status'] != 6:
                effect_id.append(one['id'])

        select_effect_data = self.conn.execute(select([
            amazon_keyword_task.c.id,
            amazon_keyword_task.c.station,
        ]).where(
            amazon_keyword_task.c.id.in_(effect_id),
        ))
        return select_effect_data

    def invalid(self):
        select_invalid_task = self.conn.execute(select([
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
            invalid_task = self.conn.execute(select([
                amazon_keyword_task.c.station,
                amazon_keyword_task.c.keyword,
                amazon_keyword_task.c.asin,
                amazon_keyword_task.c.id,
            ]).where(
                amazon_keyword_task.c.id == row,
            ))
            return invalid_task


a = Classification()
b = a.effect()
# print(b)

def sdfsd():
    print(b)

sdfsd()