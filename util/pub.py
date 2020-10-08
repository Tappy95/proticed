import asyncio
import json

from aiohttp import ClientSession, ClientTimeout
from urllib.parse import ParseResult, urlunparse, urlencode
from util.log import logger


async def pub_to_nsq(address, topic, msg, timeout=60):
    url = urlunparse(ParseResult(scheme='http', netloc=address, path='/pub', params='',
                                 query=urlencode({'topic': topic}), fragment=''))
    print(url)
    async with ClientSession(timeout=ClientTimeout(total=timeout)) as session:
        async with session.request("POST", url, data=msg) as resp:
            if resp.status != 200:
                logger.error("[pub to nsq error] topic: {}".format(topic))


async def run(message):
    a = 0
    for i in range(3):
        await pub_to_nsq("106.53.85.158:4151", "amazon_minor_language_asin_info", msg=json.dumps(message))
        a += 1
    logger.info("push message{}".format(a))


async def mpub_to_nsq(address, topic, msgs, timeout=60):
    if any(map(lambda x: '\n' in x, msgs)):
        raise ValueError(r"msgs contain \n")
    url = urlunparse(ParseResult(scheme='http', netloc=address, path='/mpub', params='',
                                 query=urlencode({'topic': topic}), fragment=''))
    async with ClientSession(timeout=ClientTimeout(total=timeout)) as session:
        async with session.request("POST", url, data="\n".join(msgs)) as resp:
            if resp.status != 200:
                logger.error("[pub to nsq error] topic: {}".format(topic))


if __name__ == '__main__':
    message = {
        "data": {
            "platform": "amazon_us",
            "asin": "B01MD19OI2",
            "parent_asin": "B077GG9D5D",
            "current_asin": "B01MD19OI2",
            "new_version_asins": [],
            "brand": "Visit the PlayStation Store",
            "title": "DualShock 4 Wireless Controller for PlayStation 4 - Magma Red",
            "ori_price": 0,
            "price": 64.99,
            "img": "https://images-na.ssl-images-amazon.com/images/I/41kaOFDXzSL.jpg",
            "review_score": 0,
            "review_number": 0,
            "review_statistics": {
                "5": 83,
                "4": 8,
                "3": 3,
                "2": 1,
                "1": 5
            },
            "review_data": {
                "global": [
                    {
                        "review_id": "R1L6JHEG7AVSIX",
                        "rating": 5.0,
                        "verified_purchase": True
                    },
                    {
                        "review_id": "R35PTAQUOCP1T3",
                        "rating": 1.0,
                        "verified_purchase": True
                    }
                ],
                "local": [
                    {
                        "review_id": "REQ8PCCTSNB44",
                        "rating": 1.0,
                        "verified_purchase": True
                    },
                    {
                        "review_id": "RW7HR3P1CG78F",
                        "rating": 1.0,
                        "verified_purchase": True
                    }
                ]
            },
            "qa_number": 0,
            "follow_sellers_num": 0,
            "sku_info": {
                "B01MD19OI2": {
                    "Color": "MagmaRed"
                },
                "B07GQ6NN9M": {
                    "Color": "SunsetOrange"
                },
                "B01LWVX2RG": {
                    "Color": "JetBlack"
                },
                "B07VBBJ6KZ": {
                    "Color": "GlacierWhite"
                },
                "B01MTKXP31": {
                    "Color": "GreenCamouflage"
                },
                "B07WDS2CGW": {
                    "Color": "TitaniumBlue"
                },
                "B07WN1GZXP": {
                    "Color": "ElectricPurple"
                },
                "B07WK527B3": {
                    "Color": "RedCamo"
                },
                "B0799CLFYQ": {
                    "Color": "SteelBlack"
                },
                "B071RSSMLL": {
                    "Color": "Gold"
                },
                "B0799976M1": {
                    "Color": "MidnightBlue"
                },
                "B08HWGBNLJ": {
                    "Color": "FIFA21"
                },
                "B07WDSD7G7": {
                    "Color": "RoseGold"
                },
                "B07GQ6R2LR": {
                    "Color": "BerryBlue"
                }
            },
            "merchant_name": "Goldstar Tech",
            "merchant_id": "ARJ9CR5IBXBH3",
            "fba": True,
            "top_category_name": "Video Games",
            "top_category_rank": 142,
            "sub_category_ls": [
                {
                    "category_id": "10111036011",
                    "rank": 5,
                    "name": "PlayStation 4 Gamepads & Standard Controllers"
                }
            ],
            "package_length": None,
            "package_width": None,
            "package_height": None,
            "package_unit": None,
            "shipping_weight": None,
            "shipping_weight_unit": None,
            "product_length": 2.0,
            "product_width": 2.0,
            "product_height": 2.0,
            "product_unit": "inches",
            "product_weight": 12.0,
            "product_weight_unit": "Ounces",
            "date_first_available": "2016-12-20",
            "is_coupon": False,
            "is_withdeal": False,
            "is_dealoftheday": False
        }}
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(message))
