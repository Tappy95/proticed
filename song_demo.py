import asyncio
import json
import time
from datetime import datetime, timedelta

import nsq
import tornado.ioloop
from sqlalchemy import create_engine, or_

from HY_keyword import TOPIC_NAME
from api.amazon_keyword import GetAmazonKWMStatus, AddAmazonKWM, GetAmazonKWMAllResult, GetAmazonKWMResult
from models.amazon_models import amazon_keyword_task
from task_protocol import HYTask
from sqlalchemy import  select
from config_1 import *
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
    result = GetAmazonKWMStatus(
        ids=[234624],
        station='JP',
        capture_status=6,
    ).request()
    print(result,"getstatus")


def addmonkwasins():
    result = AddAmazonKWM(
        station = 'US',
        asin_and_keywords =[{"asin":"B07PY52GVP","keyword":"XiaoMi"}],
        num_of_days = 31,
        monitoring_num = 24,
    ).request()
    print(result,"add_a_kw_watch")

def getallresult():
    with engine.connect() as conn:
        idss = conn.execute(select([amazon_keyword_task.c.id])).fetchall()
    print(idss)
    ids = [x for x in idss]
    result = GetAmazonKWMStatus(
        station='US',
        capture_status = '6',
        ids = ids

    ).request()
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
    result =  GetAmazonKWMResult(
        # ids = [x for x in range(234615,234630)],
        ids = [235672],
        start_time= a,
        end_time=  b,
        # start_time='1',
        # end_time='1',
    ).request()
    print(result)




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
        select_task = select([amazon_keyword_task])\
            .where(
            or_(
                    amazon_keyword_task.c.monitoring_count ==12,
                    amazon_keyword_task.c.station != 'US',
            )
        )
        select_db = conn.execute(select_task).fetchall()
        for one in select_db:
            print(one['monitoring_count'],one['station'])
            interval_db =  one['end_time'] - datetime.now()
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
        if one['end_time'] - datetime.now() > timedelta(days=5)\
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
            if row['capture_status'] ==6 or \
                row['deleted_at'] is not None or\
                    (row['end_time'] - datetime.now()) <timedelta(days=5) or \
                    datetime.now() - row['last_update'] > timedelta(days=4):
                invalid_id.append(row['id'])
        print(invalid_id)

if __name__ == '__main__':
    getkwrank()
    # db_classification_invalid()
    # print(db_classification_effect())
    # getstatus()
    # getallresult()
    # writer = nsq.Writer(['127.0.0.1:4150'])
    # tornado.ioloop.PeriodicCallback(pub_message, 2000).start()
    # nsq.run()
    # start_time = datetime.now()
    # str = start_time.strftime('%Y-%m-%d %H:%M:%S')
    # # getkwrank()
    # # getstatus()
    # end_time = time.strftime('%Y-%m-%d %H:%M:%S')
    # end_time_2 = (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
    # print(start_time,"\n",end_time, "\n", end_time_2)
    # a= datetime.now() - timedelta(days=1)
    # print(a)
    # getallresult()
    # getallkwasin()'%Y-%m-%d %H:%M:%S'
    # info = {'id': 235664, 'asin': 'B002JOO448', 'keyword': 'football', 'status': 'NormalAsin', 'monitoring_num': 4, 'monitoring_count': 0, 'monitoring_type': 3, 'station': 'US', 'start_time': '2019-12-26 12:12:55', 'end_time': '2020-01-25 12:01:55', 'created_at': '2019-12-26 12:12:17', 'deleted_at': None, 'is_add': 1, 'last_update': '2019-12-26 13:23:30'}
    # print(map_test(info))