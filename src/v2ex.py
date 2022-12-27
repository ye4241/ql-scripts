'''
new Env('v2ex');
10 0 0 * * * v2ex.py
'''
import os
import re

import requests
import urllib3

urllib3.disable_warnings()

ENV_KEY = 'V2EX_COOKIE'


def sign(cookie):
    session = requests.Session()
    session.headers.update({
        'authority': 'v2ex.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'cookie': cookie,
        'dnt': '1',
        'referer': 'https://v2ex.com/mission/daily',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54'
    })
    session.verify = False
    daily_body = session.get('https://www.v2ex.com/mission/daily').content.decode('utf-8')
    if '每日登录奖励已领取' in daily_body:
        print('已领取')
        return
    redeem_code = re.search(r'<input[^>]*\/mission\/daily\/redeem\?once=(\d+)[^>]*>', daily_body)[1]
    redeem_body = session.get(f'https://www.v2ex.com/mission/daily/redeem?once={redeem_code}').content.decode('utf-8')
    if '每日登录奖励已领取' in redeem_body:
        print('签到成功')
    else:
        print('签到失败')


if __name__ == '__main__':
    cookies = os.environ.get(ENV_KEY).split('&')
    for cookie in cookies:
        sign(cookie)
