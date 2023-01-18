'''
new Env('pttime');
10 0 * * * pttime.py
'''
import os

import urllib3
import requests

ENV_KEY = 'PTTIME_TOKEN'

urllib3.disable_warnings()


def attend(username, password):
    session = requests.Session()
    session.verify = False
    session.headers.update({
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9',
        'authority': 'www.pttime.org',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76',
        'origin': 'https://www.pttime.org',
    })
    url = "https://www.pttime.org/takelogin.php"
    response = session.request("POST", url, data={
        'username': username,
        'password': password,
        'returnto': 'attendance.php'
    })
    if username in response.text:
        print('登录成功')
    url = "https://www.pttime.org/attendance.php"
    response = session.request("GET", url)
    if '获得魔力值' in response.text:
        print('签到成功')


if __name__ == '__main__':
    users = [token.split(';') for token in os.environ.get(ENV_KEY).split('&')]
    for user in users:
        attend(user[0], user[1])
