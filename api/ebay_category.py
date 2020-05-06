import json
from collections import OrderedDict
from .base import BaseAPI


class GetEbayCategory(BaseAPI):

    api = '/hysj_v2/ebay_api/cate_tree'

    def __init__(self, station):
        self.param = OrderedDict({
            "station": station
        })
