import asyncio
import csv
import json

import aiohttp

from api.ebay_product import GetEbayProduct, GetEbayProductBySearch
from util.log import logger


async def get_ebay_product_sku():
    result = await GetEbayProduct(
        'UK', ['293861653313']
    ).aio_request(timeout=60, retry=4)
    print(json.dumps(result))


async def ana_request(url, params, timeout=30, retry=3):
    while retry:
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
                async with session.request("GET", url, params=params) as resp:
                    print(resp.url)
                    print(params)
                    if resp.status != 200:
                        logger.error("[status code error] code: {} url: {}".format(
                            resp.status, url))
                    else:
                        return await resp.json()
        except Exception as exc:
            exc_info = (type(exc), exc, exc.__traceback__)
            logger.error("[request error] url: {}".format(url), exc_info=exc_info)
            exc.__traceback__ = None
            retry -= 1


async def aio_pro_search(item_id, retry=20):
    while retry:
        hy_result = await GetEbayProductBySearch(
            'UK',
            item_ids=[item_id]
        ).aio_request(timeout=60, retry=6)
        if hy_result['code'] == 200:
            return hy_result
        else:
            retry -= 1
            return await aio_pro_search(item_id, retry)



async def create_items_csv():
    with open(f'./questions.csv', 'r') as csv_obj:
        reader = csv.reader(csv_obj)
        results = []
        for idx, row in enumerate(reader):
            if idx == 0:
                continue
            own_id = row[0]  # 内部ID
            url = row[1]
            item_id = str(row[1].split('/')[-1].split('?')[0])  # 商品ID
            print(item_id)
            es_result = await ana_request('http://106.55.75.122:8000/EbayApi/item_es', {"item_id": item_id})
            item_info = es_result['data'][0]['_source'] if es_result['data'] else {}

            if not es_result['data']:
                hy_result = await aio_pro_search(item_id)
                if hy_result and 'result' in hy_result and hy_result['result']:
                    hy_result = hy_result['result'][0]
                    item_info = {
                        "title": hy_result['title'],
                        "seller": hy_result['seller'],
                        "store_location": hy_result['store_location'],
                        "item_location": hy_result['item_location'],
                        "price": hy_result['price'],
                        "sold_last_3": hy_result['sales_three_day2'] - hy_result['sales_three_day1'],
                        "sold_last_7": hy_result['sales_week2'] - hy_result['sales_week1'],
                        "site": 'uk',
                    }
            title = item_info['title'] if item_info else '无此项数据'
            seller = item_info['seller'] if item_info else '-'
            seller_location = item_info['store_location'] if item_info else '-'
            item_location = item_info['item_location'] if item_info else '-'
            price = item_info['price'] if item_info else '-'
            sold_last_3 = item_info['sold_last_3'] if item_info else '-'
            sold_last_7 = item_info['sold_last_7'] if item_info else '-'
            site = item_info['site'].upper() if item_info else "-"
            hy_result = await GetEbayProduct(
                site, [item_id]
            ).aio_request(timeout=60, retry=4)
            if 'main_his' in hy_result and hy_result['result'][0]['main_his']:
                pricelist = [i['price'] for i in hy_result['result'][0]['main_his']]
                max_price = max(pricelist)
                min_price = min(pricelist)
                price_str = str(min_price) + '~' + str(max_price)
            else:
                price_str = str(price)
            result_item = [own_id, item_id, site, url, title, seller, seller_location, item_location, price, price_str,
                           sold_last_3, sold_last_7]
            results.append(result_item)

        with open('./results.csv', 'w', encoding='UTF-8') as write_obj:
            writer = csv.writer(write_obj)
            writer.writerows(results)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_items_csv())
    # loop.run_until_complete(get_ebay_product_sku())
