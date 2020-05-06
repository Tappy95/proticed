import json
from collections import OrderedDict
from .base import BaseAPI


class GetWishCategory(BaseAPI):

    api = '/hysj_v2/wish_api/cate_tree'

    def __init__(self):
        self.param = OrderedDict()
