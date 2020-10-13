import requests

headers = {"asd": "ok"}
proxies = {
    "http": "http://lum-customer-onesiness-zone-static10:kz53twdp74rd@zproxy.lum-superproxy.io:22225"
}
resp = requests.get(url="http://www.baidu.com", headers=headers, proxies=proxies)
print(resp.status_code)
print(resp.text)
