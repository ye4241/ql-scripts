'''
new Env('btschool');
10 0 * * * btschool.py
'''

ENV_KEY = 'BTSCHOOL_COOKIE'


def add_bonus(cookie):
    import requests
    session = requests.Session()
    session.headers.update({
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        'refer': 'https://pt.btschool.club/index.php'
    })

    session.verify = False
    response = session.get('https://pt.btschool.club/index.php?action=addbonus').text
    if '欢迎回来' in response:
        print('签到成功')
    else:
        print(f'签到失败: {response}')


def main():
    import os
    cookies = os.environ.get(ENV_KEY).split('&')
    for cookie in cookies:
        add_bonus(cookie)


if __name__ == '__main__':
    main()
