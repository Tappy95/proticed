import json
import operator
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


class classification():
    def __init__(self):
        self.conn = engine.connect()

    def task_result(self):
        select_task = self.conn.execute(select(
            [amazon_keyword_task]
        )).fetchall()
        return select_task

    def effect(self):
        selected_data = self.task_result()
        select_effect = self.conn.execute(select(
            [selected_data.c.id]
        ).where(
            and_(
                selected_data.c.capture_status != 6,
                selected_data.c.deleted_at is None,
                selected_data.c.end_time - datetime.now() > timedelta(days=5),
            )
        )).fetchall()
        return select_effect.alias()

    def invalid(self):
        select_invalid = self.conn.execute(select(
            [
                amazon_keyword_task.c.id,
                amazon_keyword_task.c.capture_status,
                amazon_keyword_task.c.end_time,
                amazon_keyword_task.c.last_update,
                amazon_keyword_task.c.deleted_at,
            ]
        ).where(
            or_(
                amazon_keyword_task.c.capture_status is None,
                amazon_keyword_task.c.capture_status == 2,
                # (amazon_keyword_task.c.end_time - datetime.now()) < timedelta(days=5),
                # (datetime.now() - amazon_keyword_task.c.last_update) > timedelta(days=4),
            )
        )).fetchall()
        return select_invalid


def db_classification_effect():
    with engine.connect() as conn:
        select_effect_task = conn.execute(select([
            amazon_keyword_task.c.id,
            amazon_keyword_task.c.end_time,
            amazon_keyword_task.c.capture_status,
        ])).fetchall()
        effect_id = []
        for one in select_effect_task:

            if one['end_time'] is not None and one['end_time'] - datetime.now() > timedelta(days=5) \
                    and one['capture_status'] != 6:
                effect_id.append(one['id'])
        print(effect_id)
        select_effect_data = conn.execute(select([
            amazon_keyword_task.c.id,
            amazon_keyword_task.c.station,
        ],
            amazon_keyword_task.c.id.in_(effect_id)
        )).fetchall()
        return select_effect_data


print(db_classification_effect())
