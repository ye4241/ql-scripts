'''
new Env('simpsearch');
8 0 * * * simpsearch.py
'''
import os
import requests
import urllib3

urllib3.disable_warnings()

ENV_KEY = 'SIMPSEARCH_COOKIE'


def get_current_user(cookie):
    print('获取用户')
    response = requests.get('https://www.simpsearch.com/wp-admin/admin-ajax.php?action=get_current_user', headers={
        'cookie': cookie,
    }, verify=False).json()
    print(response)


def user_checkin(cookie):
    print('开始签到')
    response = requests.post('https://www.simpsearch.com/wp-admin/admin-ajax.php', data={
        'action': 'user_checkin'
    }, headers={
        'cookie': cookie,
    }, verify=False).json()
    print(response)


if __name__ == '__main__':
    users = [token for token in os.environ.get(ENV_KEY).split('&')]
    for user in users:
        get_current_user(user)
        user_checkin(user)
