#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

__author__ = 'point'
__date__ = '2018-12-26'

from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
from urllib.parse import quote_plus
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
from base64 import decodebytes, encodebytes

import json


class AliPay(object):
    """
    支付宝支付接口
    """

    def __init__(self, appid, app_notify_url, app_private_key_path,
                 alipay_public_key_path, return_url, debug=False):
        self.appid = appid
        self.app_notify_url = app_notify_url
        self.app_private_key_path = app_private_key_path
        self.app_private_key = None
        self.return_url = return_url
        with open(self.app_private_key_path) as fp:
            self.app_private_key = RSA.importKey(fp.read())

        self.alipay_public_key_path = alipay_public_key_path
        with open(self.alipay_public_key_path) as fp:
            self.alipay_public_key = RSA.import_key(fp.read())

        if debug is True:
            self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        else:
            self.__gateway = "https://openapi.alipay.com/gateway.do"

    def direct_pay(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):
        biz_content = {
            "subject": subject,
            "out_trade_no": out_trade_no,
            "total_amount": total_amount,
            "product_code": "FAST_INSTANT_TRADE_PAY",
            # "qr_pay_mode":4
        }

        biz_content.update(kwargs)
        data = self.build_body("alipay.trade.page.pay", biz_content, self.return_url)
        return self.sign_data(data)

    def build_body(self, method, biz_content, return_url=None):
        data = {
            "app_id": self.appid,
            "method": method,
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "biz_content": biz_content
        }

        if return_url is not None:
            data["notify_url"] = self.app_notify_url
            data["return_url"] = self.return_url

        return data

    def sign_data(self, data):
        data.pop("sign", None)
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        sign = self.sign(unsigned_string.encode("utf-8"))
        # ordered_items = self.ordered_data(data)
        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in unsigned_items)

        # 获得最终的订单信息字符串
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    def ordered_data(self, data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    def sign(self, unsigned_string):
        # 开始计算签名
        key = self.app_private_key
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA256.new(unsigned_string))
        # base64 编码，转换为unicode表示并移除回车
        sign = encodebytes(signature).decode("utf8").replace("\n", "")
        return sign

    def _verify(self, raw_content, signature):
        # 开始计算签名
        key = self.alipay_public_key
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(raw_content.encode("utf8"))
        if signer.verify(digest, decodebytes(signature.encode("utf8"))):
            return True
        return False

    def verify(self, data, signature):
        if "sign_type" in data:
            sign_type = data.pop("sign_type")
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
        return self._verify(message, signature)


if __name__ == "__main__":
    return_url = "http://132.232.184.182:8000/alipay/return/?charset=utf-8&out_trade_no=20181226007&method=alipay.trade.page.pay.return&total_amount=9999.00&sign=BALdfrSw04jkZZPAzj7WZU3Pg%2Bf2CQyn%2BG1JwV%2BimFLwWFFJOGGkMnldKfRAeTHx%2F7bglFJKW5r4nWWYcXbQjp3o8EpCqi2GBMmt11bOEqdCp8i8ewbnugvgm%2FuYs7QfZtpyANk2Ee0xromVH1sG2mUuki%2B0DM%2FU%2F19BJvYTtrneSYQZn7QZTXODOyeEgMyRBC5IRRJ3FJlY86gj3FNRPpYWuyxESEIBgljV7mDl32DwOX9ae4umd%2BjaqBiAJo%2FkuTFOptgTskgYCwgshda8NJDOak%2FL6t3ONzRBGCcWbzLBeratoHVx2%2BoGeRq2gGiAaY%2BGX04HApZl9HOTVZ%2BvFA%3D%3D&trade_no=2018122622001471000501680048&auth_app_id=2016092300575055&version=1.0&app_id=2016092300575055&sign_type=RSA2&seller_id=2088102176859612&timestamp=2018-12-26+14%3A41%3A55"
    # return_url = ''
    o = urlparse(return_url)
    query = parse_qs(o.query)
    processed_query = {}
    ali_sign = query.pop("sign", [''])[0]

    # 测试用例
    alipay = AliPay(
        # appid 在沙箱环境中就可以找到
        appid="2016092300575055",
        # 这个值先不管，在与 vue 的联调中介绍
        app_notify_url="http://132.232.184.182:8000/alipay/return/",
        # 我们自己商户的密钥
        app_private_key_path="../trade/keys/private_2048.txt",
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        alipay_public_key_path="../trade/keys/alipay_key_2048.txt",
        # 先不用管，后面 vue 解释
        return_url="http://132.232.184.182:8000/alipay/return/",
        # debug 为 true 时使用沙箱的 url。如果不是则用正式环境的 url，默认 False
        debug=True,
    )

    for key, value in query.items():
        processed_query[key] = value[0]
    print(alipay.verify(processed_query, ali_sign))

    # 直接支付:生成请求的字符串。
    url = alipay.direct_pay(
        # 订单标题
        subject="测试订单",
        # 我们商户自行生成的订单号
        out_trade_no="20181226011",
        # 订单金额
        total_amount=9999,
        return_url="http://132.232.184.182:8000/alipay/return/"
    )
    # 将生成的请求字符串拿到我们的url中进行拼接
    re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

    print(re_url)
