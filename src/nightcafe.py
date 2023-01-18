'''
new Env('nightcafe');
5 8 * * * nightcafe.py
'''
import os
import requests
import urllib3

urllib3.disable_warnings()

ENV_KEY = 'NIGHTCAFE_TOKEN'


def get_daily_credits(email, password):
    session = requests.Session()
    session.verify = False
    session.headers.update({
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
        'referer': 'https://creator.nightcafe.studio/',
    })
    print(f'login user: {email}')
    login = session.post(
        'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyD_bN4JwaaUIuYIOZ2cTvHrh0LRUYTXnfI',
        json={'returnSecureToken': True, 'email': email, 'password': password}
    ).json()
    print(login)
    print('get daily credits')
    topup = session.post(
        'https://us-central1-nightcafe-creator.cloudfunctions.net/api/credits/topup',
        headers={'x-auth-token': login['idToken']}
    ).json()
    print(topup)


if __name__ == '__main__':
    users = [token.split(';') for token in os.environ.get(ENV_KEY).split('&')]
    for user in users:
        get_daily_credits(user[0], user[1])
