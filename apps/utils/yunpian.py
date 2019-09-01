import json
import os

import requests
import django

env = os.environ.get('PROJECT_ENV', 'dev')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mxshop.settings.{}'.format(env))
django.setup()

from django.conf import settings


class YunPian:
    def __init__(self, api_key):
        self.api_key = api_key
        self.signature = settings.YUNPIAN_SIGNATURE
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        params = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': "【{signature}】您的验证码是{code}。如非本人操作，请忽略本短信".format(signature=self.signature, code=code),
        }

        response = requests.post(self.single_send_url, data=params)
        ret_dict = json.loads(response.text)
        return ret_dict


if __name__ == '__main__':
    yun_pian = YunPian(settings.YUNPIAN_APIKEY)
    # yun_pian.send_sms('2019', '手机号')
    yun_pian.send_sms('2019', settings.YUNPIAN_TEST_MOBILE)
