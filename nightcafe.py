"""
0 22 * * * nightcafe.py
"""
import os
import requests

if __name__ == '__main__':
    url = "https://us-central1-nightcafe-creator.cloudfunctions.net/api/credits/topup"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "x-auth-token": os.environ.get("NIGHTCAFE_TOKEN")
    }
    response = requests.request("POST", url, headers=headers)
    print(response.json())
