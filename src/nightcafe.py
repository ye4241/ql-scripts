'''
new Env('nightcafe');
5 8 * * * nightcafe.py
'''
import os
import random
import time

import requests
import urllib3

urllib3.disable_warnings()

ENV_KEY = 'NIGHTCAFE_TOKEN'


def login(email, password):
    session = requests.Session()
    proxy = os.environ.get('NIGHTCAFE_PROXY')
    session.proxies = {
        'http': proxy,
        'https': proxy,
    }
    session.verify = False
    session.headers.update({
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
        'referer': 'https://creator.nightcafe.studio/',
    })
    print(f'login user: {email}')
    user = session.post(
        'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyD_bN4JwaaUIuYIOZ2cTvHrh0LRUYTXnfI',
        json={'returnSecureToken': True, 'email': email, 'password': password}
    ).json()
    session.headers.update({
        'x-auth-token': user['idToken'],
    })
    print(user)
    return (session, user['localId'])


def get_connect_credits(session: requests.Session, user_id: str):
    print('get connect credits')
    result = session.post(
        f'https://us-central1-nightcafe-creator.cloudfunctions.net/api/inboxMessage/user-{user_id}:message-userReceivedBadge-connectAnonymous:subject-connectAnonymous/action',
    ).json()
    print(result)


def get_daily_credits(session: requests.Session):
    print('get daily credits')
    result = session.post(
        'https://us-central1-nightcafe-creator.cloudfunctions.net/api/credits/topup',
    ).json()
    print(result)


def get_vote_daily_credits(session: requests.Session, user_id: str):
    print('get vote daily credits')
    count = 20
    resp = session.get('https://creator.nightcafe.studio/game/daily-challenge-vote', allow_redirects=True)
    game_id = resp.url.split('/')[-1]
    print('game_id', game_id)
    game_page = session.get(
        f'https://us-central1-nightcafe-creator.cloudfunctions.net/api/challenge/{game_id}/entries/voting?page=1').json()
    if 'entries' not in game_page:
        print(game_page)
        return
    entries = game_page['entries']
    for entry in entries[:count]:
        entry_id = entry['id']
        rating = random.randint(1, 5)
        print('vote', entry_id, rating)
        vote = session.post(
            f'https://us-central1-nightcafe-creator.cloudfunctions.net/api/challenge/{game_id}/entry/{entry_id}/vote',
            json={
                'voteKey': entry['voteKey'],
                'rating': rating
            }).json()
        print(vote['status'])
    time.sleep(1)
    claim = session.post(
        f'https://us-central1-nightcafe-creator.cloudfunctions.net/api/inboxMessage/user-{user_id}:message-userReceivedBadge-dailyChallengeVoter:subject-dailyChallengeVoter:unique-1/action',
        json={}
    ).json()
    print(claim)


def main():
    users = [token.split(';') for token in os.environ.get(ENV_KEY).split('&')]
    for user in users:
        (session, user_id) = login(user[0], user[1])
        get_daily_credits(session)
        # get_connect_credits(session, user_id)
        get_vote_daily_credits(session, user_id)


if __name__ == '__main__':
    main()
