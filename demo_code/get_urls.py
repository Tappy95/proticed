import redis

redis_conn = None
def get_curl():
    global redis_conn
    result = redis_conn.rpop('curl_list')
    redis_conn.lpush('curl_list', result)
    return result


def get_redis_conn():
    global redis_conn
    redis_conn = redis.Redis(host='47.105.131.58', port=6379, db=1, decode_responses=True)
    return redis_conn


if __name__ == '__main__':
    get_redis_conn()
    # set_curls()
    get_curl()
