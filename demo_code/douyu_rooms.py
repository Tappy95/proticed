import json

import redis
import requests

redis_conn = None


def get_douyu_urls():
    for i in range(1, 5):
        resp = requests.get('https://www.douyu.com/gapi/rkc/directory/mixList/0_0/{}'.format(i))
        info = json.loads(resp.text)
        room_ids = [room['rid'] for room in info['data']['rl']]
        for room_id in room_ids:
            room_url = 'https://www.douyu.com/' + str(room_id)
            redis_conn.lpush('douyu_room_list', room_url)


def get_redis_conn():
    global redis_conn
    redis_conn = redis.Redis(host='47.105.131.58', port=6379, db=1, decode_responses=True)
    return redis_conn


if __name__ == '__main__':
    get_redis_conn()
    # set_cookies()
    get_douyu_urls()
