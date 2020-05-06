import json
from collections import OrderedDict
from .base import BaseAPI


class GetEbayProductBySearch(BaseAPI):

    api = '/hysj_v2/ebay_api/item_infos'

    def __init__(self, station, current_page=None, item_ids=None, title=None,
                 title_type=None, item_location=None, seller=None, store=None,
                 store_location=None, sold_start=None, sold_end=None,
                 sold_the_previous_day_start=None, sold_the_previous_day_end=None,
                 payment_the_previous_day_start=None, payment_the_previous_day_end=None,
                 sales_three_day1_start=None, sales_three_day1_end=None,
                 payment_three_day1_start=None, payment_three_day1_end=None,
                 sales_three_day_growth_start=None, sales_three_day_growth_end=None,
                 p_l1_id=None, sub_cate_id=None, gen_time_start=None, gen_time_end=None,
                 price_start=None, price_end=None, watchers_start=None, watchers_end=None,
                 sold_the_previous_growth_start=None, sold_the_previous_growth_end=None,
                 visit_start=None, visit_end=None, sales_three_day_flag=None,
                 sales_week1_start=None, sales_week1_end=None, sales_week_growth_start=None,
                 sales_week_growth_end=None, popular_status=None, marketplace=None,
                 last_modi_time_start=None, last_modi_time_end=None,
                 order_by=None, order_by_type=None):
        self.param = OrderedDict({
            "station": station, "current_page": current_page,
            "item_ids": ','.join(item_ids) if item_ids else None,
            "title": title, "title_type": title_type, "item_location": item_location,
            "seller": seller,"store": store, "store_location": store_location,
            "sold_start": sold_start, "sold_end": sold_end,
            "sold_the_previous_day_start": sold_the_previous_day_start,
            "sold_the_previous_day_end": sold_the_previous_day_end,
            "payment_the_previous_day_start": payment_the_previous_day_start,
            "payment_the_previous_day_end": payment_the_previous_day_end,
            "sales_three_day1_start": sales_three_day1_start,
            "sales_three_day1_end": sales_three_day1_end,
            "payment_three_day1_start": payment_three_day1_start,
            "payment_three_day1_end": payment_three_day1_end,
            "sales_three_day_growth_start": sales_three_day_growth_start,
            "sales_three_day_growth_end": sales_three_day_growth_end,
            "p_l1_id": p_l1_id, "sub_cate_id": sub_cate_id, "gen_time_start": gen_time_start,
            "gen_time_end": gen_time_end, "price_start": price_start, "price_end": price_end,
            "watchers_start": watchers_start, "watchers_end": watchers_end,
            "sold_the_previous_growth_start": sold_the_previous_growth_start,
            "sold_the_previous_growth_end": sold_the_previous_growth_end,
            "visit_start": visit_start, "visit_end": visit_end,
            "sales_three_day_flag": sales_three_day_flag,
            "sales_week1_start": sales_week1_start, "sales_week1_end": sales_week1_end,
            "sales_week_growth_start": sales_week_growth_start,
            "sales_week_growth_end": sales_week_growth_end,
            "popular_status": popular_status, "marketplace": marketplace,
            "last_modi_time_start": last_modi_time_start.strftime("%Y-%m-%d %H:%M:%S") \
                                    if last_modi_time_start else None,
            "last_modi_time_end": last_modi_time_end.strftime("%Y-%m-%d %H:%M:%S") \
                                if last_modi_time_end else None,
            "order_by": order_by, "order_by_type": order_by_type,
        })


class GetEbayProduct(BaseAPI):

    api = '/hysj_v2/ebay_api/item_info'

    def __init__(self, station, item_ids):
        self.param = OrderedDict({
            "station": station,
            "item_ids": ','.join(item_ids)
        })


class AddEbayProductDetail(BaseAPI):

    api = '/hysj_v2/ebay_api/add_item_ids'

    def __init__(self, station, item_ids):
        self.param = OrderedDict({
            "station": station,
            "item_ids": ','.join(item_ids)
        })


class AddEbayShopMonitor(BaseAPI):

    api = '/hysj_v2/ebay_api/add_monitor_shop'

    def __init__(self, station, seller):
        self.param = OrderedDict({
            "station": station,
            "seller": seller
        })
