import json
import time
import hashlib
import aiohttp
import requests
from util.log import logger


class BaseAPI:

    u_name = 'bailun'
    skey = '88UN2AZ1kUfi1HAg'
    address = 'http://114.67.80.59:38080'
    api = None
    param = None
    sign_sequence = None

    def sign(self):
        k_ls = [k for k, v in self.param.items() if v is None or v == '']
        for k in k_ls:
            self.param.pop(k)
        timestamp = str(int(time.time()))
        if self.sign_sequence == 'wish_product':
            raw_data = self.u_name + self.skey + timestamp + ''.join(str(v) for v in self.param.values())
        else:
            raw_data = self.u_name + self.skey + ''.join(str(v) for v in self.param.values()) + timestamp
        md5 = hashlib.md5(raw_data.encode('utf-8'))
        signature = md5.hexdigest()
        dct = {"u_name": self.u_name, "time": timestamp, "sign": signature}
        dct.update(self.param)
        return dct

    def request(self, timeout=30, retry=3):
        while retry:
            param = self.sign()
            try:
                url = self.address + self.api
                resp = requests.post(url=url, data=param, timeout=timeout)
                if resp.status_code != 200:
                    logger.error("[status code error] code: {} url: {}".format(
                                resp.status_code, url))
                else:
                    return json.loads(resp.text)
            except Exception as exc:
                exc_info = (type(exc), exc, exc.__traceback__)
                logger.error("[request error] url: {}".format(url), exc_info=exc_info)
                exc.__traceback__ = None
                retry -= 1

    async def aio_request(self, timeout=30, retry=3):
        while retry:
            param = self.sign()
            try:
                url = self.address + self.api
                async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
                    async with session.request("POST", url, data=param) as resp:
                        if resp.status != 200:
                            logger.error("[status code error] code: {} url: {}".format(
                                        resp.status, url))
                        else:
                            return json.loads(await resp.text())
            except Exception as exc:
                exc_info = (type(exc), exc, exc.__traceback__)
                logger.error("[request error] url: {}".format(url), exc_info=exc_info)
                exc.__traceback__ = None
                retry -= 1
