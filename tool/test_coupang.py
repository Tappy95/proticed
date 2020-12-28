from datetime import datetime, timedelta
import os
import time
import hmac, hashlib
import urllib.parse
import urllib.request
import ssl

# os.environ['TZ'] = 'GMT+{}'.format(i)
# print(time.strftime('%y%m%d'))
datetime1 = (datetime.now() - timedelta(hours=8)).strftime('%y%m%d') + 'T' + (datetime.now() - timedelta(hours=8)).strftime('%H%M%S') + 'Z'
print(datetime1)
method = "GET"
# replace with your own vendorId
path = "/v2/providers/seller_api/apis/api/v1/marketplace/meta/display-categories"
path = "/v2/providers/seller_api/apis/api/v1/marketplace/meta/category-related-metas/display-category-codes/78877"
path = "/v2/providers/seller_api/apis/api/v1/marketplace/meta/display-categories/186664"

message = datetime1 + method + path


# replace with your own accesskey
accesskey = "c086b960-8809-42c4-92f7-0415c8b9206b"
# replace with your own secretKey
secretkey = "d04c404d01df0d63c7300753a6591f4efa31a8b7"

# ********************************************************#
# authorize, demonstrate how to generate hmac signature here
signature = hmac.new(secretkey.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
authorization = "CEA algorithm=HmacSHA256, access-key=" + accesskey + ", signed-date=" + datetime1 + ", signature=" + signature
# print out the hmac key
# print(authorization)
# ********************************************************#

# ************* SEND THE REQUEST *************
url = "https://api-gateway.coupang.com" + path

req = urllib.request.Request(url)

req.add_header("Content-type", "application/json;charset=UTF-8")
req.add_header("Authorization", authorization)

req.get_method = lambda: method

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    resp = urllib.request.urlopen(req, context=ctx)
except urllib.request.HTTPError as e:
    print(e.code)
    print(e.reason)
    print(e.fp.read())
except urllib.request.URLError as e:
    print(e.errno)
    print(e.reason)
    print(e.fp.read())
else:
    # 200
    import json
    body = resp.read().decode(resp.headers.get_content_charset())
    body = json.loads(body)
    with open('./1.json', 'w', encoding="UTF-8") as file_obj:
        json.dump(body, file_obj, ensure_ascii=False)