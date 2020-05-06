import json
from collections import OrderedDict
from .base import BaseAPI


class AddAmazonRW(BaseAPI):

    api = '/hysj_v4/amazon_api/add_review_asins'

    def __init__(self, station, asins):
        self.param = OrderedDict({
            "station": station,
            "asins": ','.join(asins)
        })


class DelAmazonRW(BaseAPI):

    api = '/hysj_v4/amazon_api/del_review_asins'

    def __init__(self, station, asins):
        self.param = OrderedDict({
            "station": station,
            "asins": ','.join(asins)
        })


class GetAmazonRWResult(BaseAPI):

    api = '/hysj_v4/amazon_api/asin_reviews'

    def __init__(self, station, asin, review_date_start=None, review_date_end=None):
        self.param = OrderedDict({
            "station": station,
            "asin": asin,
            "review_date_start": review_date_start,
            "review_date_end": review_date_end
        })
