'''
new Env('simpsearch');
8 0 * * * simpsearch.py
'''
import os
import requests
import urllib3

urllib3.disable_warnings()

ENV_KEY = 'SIMPSEARCH_COOKIE'


def login(cookie):
    session = requests.Session()
    session.headers.update({
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69'})
    session.verify = False
    return session


def get_current_user(session):
    print('获取用户')
    response = session.get('https://www.simpsearch.com/wp-admin/admin-ajax.php?action=get_current_user').json()
    print(response)


def user_checkin(session):
    print('开始签到')
    response = session.post('https://www.simpsearch.com/wp-admin/admin-ajax.php', headers={
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }, data='action=user_checkin').json()
    print(response)


if __name__ == '__main__':
    users = [token for token in os.environ.get(ENV_KEY).split('&')]
    for user in users:
        session = login(user)
        get_current_user(session)
        user_checkin(session)
