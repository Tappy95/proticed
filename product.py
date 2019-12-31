import json

import nsq
import tornado.ioloop
import time
task = {
            "task": "amazon_category_sync",
            "data": {
                "site": 'US',
            }
        }

def pub_message():
    writer.pub('haiying.amazon.keyword', json.dumps(task), finish_pub)


def finish_pub(conn, data):
    print(data)


writer = nsq.Writer(['47.102.220.1:4150'])
tornado.ioloop.PeriodicCallback(pub_message, 4).start()
nsq.run()