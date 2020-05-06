import json
from collections import OrderedDict
from .base import BaseAPI


class GetWishProductBySearch(BaseAPI):

    api = '/hysj_v2/wish_api/pro_infos'

    def __init__(self, current_page=None, pids=None,
                 sales_week1_from=None, sales_week1_end=None,
                 sales_week2_from=None, sales_week2_end=None,
                 m_sales_week1_from=None, m_sales_week1_end=None,
                 total_price_from=None, total_price_end=None,
                 num_bought_from=None, num_bought_end=None,
                 num_entered_from=None, num_entered_end=None,
                 is_hwc=None, is_verified=None, is_promo=None,
                 gen_time_from=None, gen_time_end=None,
                 approved_date_from=None, approved_date_end=None,
                 cid_status=None, cid=None, pname_words=None, pname_flag=None,
                 daily_bought_start=None, daily_bought_end=None,
                 last_upd_date_start=None, last_upd_date_end=None,
                 is_pb=None,
                 view_rate1_start=None, view_rate1_end=None,
                 view_rate_growth_start=None, view_rate_growth_end=None,
                 interval_rating_start=None, interval_rating_end=None,
                 max_num_bought_start=None, max_num_bought_end=None,
                 rating_start=None, rating_end=None,
                 mids=None,
                 total_sales_arrival_date_start=None, total_sales_arrival_date_end=None,
                 daily_sales_accuracy_start=None, daily_sales_accuracy_end=None,
                 last_modi_time_start=None, last_modi_time_end=None,
                 order_by=None, order_by_type=None):
        self.param = OrderedDict({
            "current_page": current_page,
            "pid_or_pname": ','.join(pids) if pids else None,
            "sales_week1_from": sales_week1_from,
            "sales_week1_end": sales_week1_end,
            "sales_week2_from": sales_week2_from,
            "sales_week2_end": sales_week2_end,
            "m_sales_week1_from": m_sales_week1_from,
            "m_sales_week1_end": m_sales_week1_end,
            "total_price_from": total_price_from,
            "total_price_end": total_price_end,
            "num_bought_from": num_bought_from,
            "num_bought_end": num_bought_end,
            "num_entered_from": num_entered_from,
            "num_entered_end": num_entered_end,
            "is_hwc": is_hwc,
            "is_verified": is_verified,
            "is_promo": is_promo,
            "gen_time_from": gen_time_from,
            "gen_time_end": gen_time_end,
            "approved_date_from": approved_date_from,
            "approved_date_end": approved_date_end,
            "cid_status": cid_status,
            "cid": cid,
            "pname_words": pname_words,
            "pname_flag": pname_flag,
            "daily_bought_start": daily_bought_start,
            "daily_bought_end": daily_bought_end,
            "last_upd_date_start": last_upd_date_start,
            "last_upd_date_end": last_upd_date_end,
            "is_pb": is_pb,
            "view_rate1_start": view_rate1_start,
            "view_rate1_end": view_rate1_end,
            "view_rate_growth_start": view_rate_growth_start,
            "view_rate_growth_end": view_rate_growth_end,
            "interval_rating_start": interval_rating_start,
            "interval_rating_end": interval_rating_end,
            "max_num_bought_start": max_num_bought_start,
            "max_num_bought_end": max_num_bought_end,
            "rating_start": rating_start,
            "rating_end": rating_end,
            "mids": ','.join(mids) if mids else None,
            "total_sales_arrival_date_start": total_sales_arrival_date_start,
            "total_sales_arrival_date_end": total_sales_arrival_date_end,
            "daily_sales_accuracy_start": daily_sales_accuracy_start,
            "daily_sales_accuracy_end": daily_sales_accuracy_end,
            "last_modi_time_start": last_modi_time_start,
            "last_modi_time_end": last_modi_time_end,
            "order_by": order_by,
            "order_by_type": order_by_type,
        })


class GetWishProduct(BaseAPI):

    api = '/hysj_v2/wish_api/pro_info'
    sign_sequence = "wish_product"

    def __init__(self, pids):
        self.param = OrderedDict({
            "pids": ','.join(pids) if pids else None
        })


class GetWishProductSold(BaseAPI):

    api = '/hysj_v2/wish_api/pro_sale_info'
    sign_sequence = "wish_product"

    def __init__(self, pids):
        self.param = OrderedDict({
            "pids": ','.join(pids) if pids else None
        })


class GetWishProductView(BaseAPI):

    api = '/hysj_v2/wish_api/pro_view_info'
    sign_sequence = "wish_product"

    def __init__(self, pids):
        self.param = OrderedDict({
            "pids": ','.join(pids) if pids else None
        })


class GetWishProductViewDaily(BaseAPI):

    api = '/hysj_v2/wish_api/pro_view_daily'
    sign_sequence = "wish_product"

    def __init__(self, pids):
        self.param = OrderedDict({
            "pids": ','.join(pids) if pids else None
        })
