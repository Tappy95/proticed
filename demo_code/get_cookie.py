import redis

redis_conn = None

def set_cookies():
    with open('./2020-11-28.txt', mode='r') as file:
        cookies = file.read()
        cookies_list = cookies.split('\n')
        for idx, cookie in enumerate(cookies_list):
            if cookie:
                redis_conn.lpush('cookie_list', cookie)


def get_cookie():
    global redis_conn
    result = redis_conn.rpop('cookie_list')
    redis_conn.lpush('cookie_list', result)
    return result


def get_redis_conn():
    global redis_conn
    redis_conn = redis.Redis(host='47.105.131.58', port=6379, db=1, decode_responses=True)
    return redis_conn


if __name__ == '__main__':
    get_redis_conn()
    # set_cookies()
    get_cookie()
