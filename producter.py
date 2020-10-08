import nsq
import tornado.ioloop
import time


def pub_message():
    message = {"data": {
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
    writer.pub('amazon.minor.language.asin.info', message, finish_pub)


def finish_pub(conn, data):
    print(data)


writer = nsq.Writer(['106.53.85.158:4161'])
tornado.ioloop.PeriodicCallback(pub_message, 20).start()
nsq.run()
