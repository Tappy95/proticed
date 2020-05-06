import json
from collections import OrderedDict
from .base import BaseAPI


class GetShopeeCategory(BaseAPI):

    api = '/hysj_v2/shopee_api/cate_tree'

    def __init__(self, station):
        self.param = OrderedDict({
            "station": station
        })
