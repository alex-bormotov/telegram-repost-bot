import json
import requests
from time import sleep


def telegram_send_message(telegram_token, chat_id, msg):
    while True:
        res = requests.get(
            f"https://api.telegram.org/bot{telegram_token}/sendMessage?text={msg}&chat_id={chat_id}&parse_mode=MARKDOWN")
        if res.json().get('ok'):
            break
        sleep(5)
