from config import *
import requests


class Bot:
    def __init__(self, TOKEN, CHAT_ID):
        self.token = TOKEN
        self.chat_id = CHAT_ID

    def send_message(self):
        url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        requests.post(url=url, data={"chat_id": self.chat_id, "text": f'Аккаунт запущен:\n{P20TToken}:{CSRFToken}'})


class Binance:
    pass


if __name__ == '__main__':
    bot = Bot(TOKEN_TG_BOT, YOUR_TG_ID)
    bot.send_message()
