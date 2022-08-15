import requests
import json
import time

from config import *


class Bot:
    def __init__(self, TOKEN, CHAT_ID):
        self.token = TOKEN
        self.chat_id = CHAT_ID

    def send_message(self, *data, lower):
        if lower:
            message = f'The account is running:\nFirst name: {data[0]}\nUser ID: {data[1]}'
        else:
            message = f'The account is not running:\nP20TToken: {data[0]}\nCSRFToken: {data[1]}'
        url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        requests.post(url=url, data={"chat_id": self.chat_id, "text": message})


class Binance(Bot):
    # Add your code or replace the file
    def __init__(self, url, headers, TOKEN, CHAT_ID):
        super().__init__(TOKEN, CHAT_ID)
        self.headers = headers
        self.url = url

    def get_name(self):
        for i in range(5):
            authResponse = requests.post(url=self.url, headers=self.headers)
            if authResponse:
                if json.loads(authResponse.text)["success"]:
                    first_name = json.loads(authResponse.text)["data"]["firstName"]
                    user_id = json.loads(authResponse.text)["data"]["userId"]
                    self.send_message(first_name, user_id, lower=True)
                    return
                elif i == 4:
                    self.send_message(P20TToken, CSRFToken, lower=False)
            elif i == 4:
                self.send_message(P20TToken, CSRFToken, lower=False)
            time.sleep(2)


def main():
    url = 'https://www.binance.com/bapi/accounts/v1/private/account/user/base-detail'
    useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    headers = {'clienttype': 'web',
               'content-type': 'application/json',
               'cookie': f'p20t={P20TToken}; lang=en',
               'csrftoken': CSRFToken,
               'user-agent': useragent
               }
    binance = Binance(url, headers, TG_BOT, TG_ID)
    binance.get_name()


if __name__ == '__main__':
    main()
