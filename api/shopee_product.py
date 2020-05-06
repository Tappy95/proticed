import json
from collections import OrderedDict
from .base import BaseAPI


class GetShopeeProductBySearch(BaseAPI):

    api = '/hysj_v2/shopee_api/pro_infos'

    def __init__(self, station, current_page=None, pids=None, title=None,
                 merchant=None, price_start=None, price_end=None,
                 rating_min=None, rating_max=None, gen_time_from=None, gen_time_end=None,
                 p_l1_id=None, p_l2_id=None, p_l3_id=None,
                 favorite_start=None, favorite_end=None,
                 ratings_start=None, ratings_end=None,
                 shop_location=None, is_shopee_verified=None,
                 sold_start=None, sold_end=None, payment_start=None, payment_end=None,
                 historical_sold_start=None, historical_sold_end=None,
                 stat_time_start=None, stat_time_end=None,
                 shop_ids=None, order_by=None, order_by_type=None):
        self.param = OrderedDict({
            "current_page": current_page, "station": station,
            "title": title, "pid": ','.join(pids) if pids else None,
            "merchant": merchant, "price_start": price_start, "price_end": price_end,
            "rating_min": rating_min, "rating_max": rating_max,
            "gen_time_from": gen_time_from, "gen_time_end": gen_time_end,
            "p_l1_id": p_l1_id, "p_l2_id": p_l2_id, "p_l3_id": p_l3_id,
            "favorite_start": favorite_start, "favorite_end": favorite_end,
            "ratings_start": ratings_start, "ratings_end": ratings_end,
            "shop_location": shop_location, "is_shopee_verified": is_shopee_verified,
            "sold_start": sold_start, "sold_end": sold_end,
            "payment_start": payment_start, "payment_end": payment_end,
            "historical_sold_start": historical_sold_start,
            "historical_sold_end": historical_sold_end,
            "stat_time_start": stat_time_start, "stat_time_end": stat_time_end,
            "shop_ids": shop_ids, "order_by": order_by,
            "order_by_type": order_by_type,
        })
