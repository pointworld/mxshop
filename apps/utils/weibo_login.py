#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

__author__ = 'point'
__date__ = '2018-12-27'


def get_auth_url():
    weibo_auth_url = 'https://api.weibo.com/oauth2/authorize'
    redirect_url = 'http://132.232.184.182:8000/complete/weibo/'
    auth_url = weibo_auth_url + "?client_id={client_id}&redirect_uri={redirect_uri}".format(
        client_id=545785279,
        redirect_uri=redirect_url
    )

    print(auth_url)


def get_access_token(code='e6e483df807562a41ac0c281f6602cd9'):
    access_token_url = 'https://api.weibo.com/oauth2/access_token'
    import requests
    ret_dict = requests.post(access_token_url, data={
        'client_id': 545785279,
        'client_secret': 'd0e9b79451bc50237a38bf42c71be563',
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://132.232.184.182:8000/complete/weibo/'
    })
    # b'{"access_token":"2.00zESHZD04gDwaf77f718866ozXRPD","remind_in":"157679999","expires_in":157679999,"uid":"3267308053","isRealName":"true"}'
    print(ret_dict)


def get_user_info(access_token='', uid=''):
    user_url = 'https://api.weibo.com/2/users/show.json?access_token={access_token}&uid={uid}'.format(
        access_token=access_token,
        uid=uid
    )
    print(user_url)


if __name__ == '__main__':
    # get_auth_url()
    # get_access_token(code='e6e483df807562a41ac0c281f6602cd9')

    get_user_info(
        access_token='2.00zESHZD04gDwaf77f718866ozXRPD',
        uid="3267308053"
    )
