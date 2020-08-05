import os
from dateutil.tz import tz

PRODUCTION_ENV = True if os.environ.get('ENV_TYPE')=='PRODUCTION' else False


NSQ_LOOKUPD_HTTP_ADDR = 'bd-nsqlookupd:4161' if PRODUCTION_ENV else '134.73.133.2:25761'
NSQ_NSQD_TCP_ADDR = 'bd-nsqd:4150' if PRODUCTION_ENV else '134.73.133.2:25750'
NSQ_NSQD_HTTP_ADDR = 'bd-nsqd:4151' if PRODUCTION_ENV else '134.73.133.2:25751'

INPUT_NSQ_CONF = {
    'lookupd_http_addresses': [NSQ_LOOKUPD_HTTP_ADDR]
}
OUTPUT_NSQ_CONF = {
    'nsqd_tcp_addresses': NSQ_NSQD_TCP_ADDR
}

#
# DB_USER_NAME = "root" if PRODUCTION_ENV else "linkcool"
# DB_USER_PW = "@ie0bzy3!dlpq*d7" if PRODUCTION_ENV else "forconnect"
# DB_SEVER_ADDR = "10.0.1.4:4000" if PRODUCTION_ENV else "119.145.69.74:43021"
# DB_DATABASE_NAME = "bigdata"
# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{name:s}:{pw:s}@{addr:s}/{db:s}".format(
#     name=DB_USER_NAME,
#     pw=DB_USER_PW,
#     addr=DB_SEVER_ADDR,
#     db=DB_DATABASE_NAME)
# SQLALCHEMY_POOL_PRE_PING = True
# SQLALCHEMY_ECHO = False if PRODUCTION_ENV else True
# SQLALCHEMY_POOL_SIZE = 0
# SQLALCHEMY_POOL_MAX_OVERFLOW = -1
# SQLALCHEMY_POOL_RECYCLE = 120


# db config
# DB_USER_NAME = "root" if PRODUCTION_ENV else "linkcool"
# DB_USER_PW = "@ie0bzy3!dlpq*d7" if PRODUCTION_ENV else "forconnect"
# DB_SEVER_ADDR = "10.0.1.26" if PRODUCTION_ENV else "119.145.69.74"
# DB_SEVER_PORT = 4000 if PRODUCTION_ENV else 43021
# DB_DATABASE_NAME = "bigdata"

# DB_USER_NAME = "linkcool" if PRODUCTION_ENV else "root"
# DB_USER_PW = "forconnect" if PRODUCTION_ENV else "@ie0bzy3!dlpq*d7"
# DB_SEVER_ADDR = "119.145.69.74" if PRODUCTION_ENV else "134.175.210.192"
# DB_SEVER_PORT = 43021 if PRODUCTION_ENV else 4000
# DB_DATABASE_NAME = "bigdata"
DB_USER_NAME = "root" if PRODUCTION_ENV else "wind"
DB_USER_PW = "@ie0bzy3!dlpq*d7" if PRODUCTION_ENV else "!Syy950507"
DB_SEVER_ADDR = "10.0.1.7" if PRODUCTION_ENV else "47.102.220.1"
DB_SEVER_PORT = 4000 if PRODUCTION_ENV else 3306
DB_DATABASE_NAME = "bigdata"

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{name:s}:{pw:s}@{addr:s}:{port}/{db:s}".format(
    name=DB_USER_NAME,
    pw=DB_USER_PW,
    addr=DB_SEVER_ADDR,
    db=DB_DATABASE_NAME,
    port=DB_SEVER_PORT
)

# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{name:s}:{pw:s}@{addr:s}:{port}/{db:s}".format(
#     name=DB_USER_NAME,
#     pw=DB_USER_PW,
#     addr=DB_SEVER_ADDR,
#     port=DB_SEVER_PORT,
#     db=DB_DATABASE_NAME)
SQLALCHEMY_POOL_PRE_PING = True
SQLALCHEMY_ECHO = False if PRODUCTION_ENV else True
SQLALCHEMY_POOL_SIZE = 0
SQLALCHEMY_POOL_MAX_OVERFLOW = -1
SQLALCHEMY_POOL_RECYCLE = 120
AUTOCOMMIT = True


# faust config
# TZ_SH = tz.gettz('Asia/Shanghai')
# SITE = ""
# EFFICIENT_SECOND_LIMIT = 86400 * 14
# PRODUCT_PERIODS = 7 + 1
# PRODUCT_TOTAL_PERIODS = 1 + 1
# PRODUCT_CALCULATE_PERIODS = 7 + 1
#
# SAVE_TO_DB_MAX_COUNT = 3000 if PRODUCTION_ENV else 2000
# SAVE_TO_DB_MAX_WAIT = 10 if PRODUCTION_ENV else 4
# SAVE_TO_ES_MAX_COUNT = 4000 if PRODUCTION_ENV else 2000
# SAVE_TO_ES_MAX_WAIT = 15 if PRODUCTION_ENV else 4

# faust config
TZ_SH = tz.gettz('Asia/Shanghai')
SITE = ""
EFFICIENT_SECOND_LIMIT = 86400 * 14
PRODUCT_PERIODS = 30 + 1
PRODUCT_TOTAL_PERIODS = 1 + 1

SAVE_TO_DB_MAX_COUNT = 3000 if PRODUCTION_ENV else 2000
SAVE_TO_DB_MAX_WAIT = 10 if PRODUCTION_ENV else 4
SAVE_TO_ES_MAX_COUNT = 4000 if PRODUCTION_ENV else 2000
SAVE_TO_ES_MAX_WAIT = 15 if PRODUCTION_ENV else 4
