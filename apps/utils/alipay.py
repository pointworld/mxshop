import json
import os
from datetime import datetime
from base64 import decodebytes, encodebytes
from base64 import b64encode, b64decode

import django

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from urllib.parse import quote_plus
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen

env = os.environ.get('PROJECT_ENV', 'dev')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mxshop.settings.{}'.format(env))
django.setup()

from django.conf import settings


class AliPay:
    """
    支付宝支付接口
    """

    def __init__(self, appid, app_notify_url, app_private_key_path,
                 alipay_public_key_path, return_url, debug=False):
        # 支付宝分配给开发者的应用 ID
        self.appid = appid
        # 支付宝服务器主动通知商户服务器里指定的页面 http/https 路径
        self.app_notify_url = app_notify_url
        # HTTP/HTTPS 开头字符串
        self.return_url = return_url

        # 私钥
        self.app_private_key_path = app_private_key_path
        with open(self.app_private_key_path) as fp:
            self.app_private_key = RSA.importKey(fp.read())

        # 公钥
        self.alipay_public_key_path = alipay_public_key_path
        with open(self.alipay_public_key_path) as fp:
            self.alipay_public_key = RSA.import_key(fp.read())

        if debug is True:
            # 支付宝网关（沙箱环境）
            self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        else:
            # 支付宝网关（正式环境）
            self.__gateway = "https://openapi.alipay.com/gateway.do"

    def direct_pay(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):
        """
        直接支付
        :param subject:
        :param out_trade_no:
        :param total_amount:
        :param return_url:
        :param kwargs:
        :return:
        """

        # 请求参数的集合，最大长度不限，除公共参数外所有请求参数都必须放在这个参数中传递
        biz_content = {
            # 订单标题
            "subject": subject,
            # 商户订单号, 64个字符以内、可包含字母、数字、下划线；需保证在商户端不重复
            "out_trade_no": out_trade_no,
            # 订单总金额，单位为元，精确到小数点后两位，取值范围[0.01,100000000]
            "total_amount": total_amount,
            # 销售产品码，与支付宝签约的产品码名称。
            # 注：目前仅支持FAST_INSTANT_TRADE_PAY
            "product_code": "FAST_INSTANT_TRADE_PAY",
            # PC扫码支付的方式，支持前置模式和跳转模式
            # "qr_pay_mode":4
        }

        # 允许传递更多参数，放到 biz_content
        biz_content.update(kwargs)
        # 构建请求参数
        data = self.build_body("alipay.trade.page.pay", biz_content, self.return_url)
        # 返回生成的签名字符串
        return self.sign_data(data)

    def build_body(self, method, biz_content, return_url=None):
        """
        构建请求参数
        build_body 主要生产消息的格式
        :param method:
        :param biz_content:
        :param return_url:
        :return:
        """

        # 公共请求参数
        data = {
            # 支付宝分配给开发者的应用 ID
            "app_id": self.appid,
            # 接口名称
            "method": method,
            # 请求使用的编码格式，如 utf-8
            "charset": "utf-8",
            # 商户生成签名字符串所使用的签名算法类型，目前支持RSA2和RSA，推荐使用RSA2
            "sign_type": "RSA2",
            # 发送请求的时间，格式"yyyy-MM-dd HH:mm:ss"
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            # 调用的接口版本，固定为：1.0
            "version": "1.0",
            # 请求参数的集合，最大长度不限，除公共参数外所有请求参数都必须放在这个参数中传递
            "biz_content": biz_content
        }

        if return_url is not None:
            # 支付宝服务器主动通知商户服务器里指定的页面http/https路径
            data["notify_url"] = self.app_notify_url
            # HTTP/HTTPS开头字符串
            data["return_url"] = self.return_url

        return data

    def sign_data(self, data):
        """
        生成签名字符串
        :param data:
        :return:
        """

        # 签名
        data.pop("sign", None)
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        # 排序后拼接起来
        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        # 这里得到签名的字符串
        sign = self.sign(unsigned_string.encode("utf-8"))
        # 对 url 进行处理
        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in unsigned_items)

        # 获得最终的订单信息字符串
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    def ordered_data(self, data):
        """
        参数传进来一定要排序
        :param data:
        :return:
        """

        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据 dump 出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    def sign(self, unsigned_string):
        # 开始计算签名
        key = self.app_private_key
        # 签名的对象
        signer = PKCS1_v1_5.new(key)
        # 生成签名
        signature = signer.sign(SHA256.new(unsigned_string))
        # base64 编码，转换为 unicode 表示并移除回车
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
            data.pop("sign_type")
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
        return self._verify(message, signature)


if __name__ == "__main__":
    app_notify_url = "http://shop.pointborn.com/alipay/return/"

    # 测试用例
    alipay = AliPay(
        # appid 在沙箱环境中就可以找到
        appid=settings.ALIPAY_APP_ID,
        # notify_url 是异步的 url
        app_notify_url=app_notify_url,
        # 我们自己商户的密钥
        app_private_key_path=settings.ALIPAY_PRI_KEY_PATH,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥
        alipay_public_key_path=settings.ALIPAY_PUB_KEY_PATH,
        # 先不用管，后面 vue 解释
        return_url=app_notify_url,
        # debug 为 true 时使用沙箱的 url。如果不是则用正式环境的 url，默认 False
        debug=True,
    )

    # 直接支付: 生成请求的字符串
    url = alipay.direct_pay(
        # 订单标题
        subject="测试订单 pointborn",
        # 我们商户自行生成的订单号
        out_trade_no="20181226016",
        # 订单金额
        total_amount=888,
        # 成功付款后跳转到的页面
        return_url=app_notify_url
    )
    # 将生成的请求字符串拿到我们的 url 中进行拼接
    re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)

    print(re_url)
