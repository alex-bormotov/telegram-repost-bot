import re
import pytz
import asyncio
from time import sleep
from fs import read_json
from datetime import datetime
from telethon import TelegramClient
from telethon.tl import functions, types

CONFIG = read_json('config/config.json')
CHANNELS = read_json('config/channels.json')['channels']
words = read_json('config/search_words.json')['words']
excluded_words = read_json('config/excluded_words.json')['excluded']

LAST_RUN_DATE = None

client = TelegramClient('my_session', CONFIG['app_id'], CONFIG['app_hash'])
client.start()


async def main():
    global LAST_RUN_DATE

    if LAST_RUN_DATE is None:
        LAST_RUN_DATE = datetime.utcnow()

    filtered_msg = []

    def format_msg(msg):
        # remove copyright
        msg = re.sub(r"\[(.+)\]\(.+\)", r"", msg)
        if '\n—————————\n' in msg:
            msg = re.sub(
                r"\(?https?://(t.me/inwork_collection|t.me/InWork_team_bot|t.me/inwork_udalenka_bot).+?\)?", r"", msg)
            msg = msg[:msg.find('\n—————————\n')]
        return msg

    for c in CHANNELS:
        await asyncio.sleep(1)
        channel = await client.get_entity(f'@{c}')
        messages = await client.get_messages(channel, limit=1)

        last_msg_id = 0

        if len(messages) > 0:
            for x in messages:
                if x.text is not None:
                    for w in words:
                        for ex_w in excluded_words:
                            if w in x.message and ex_w not in x.message:
                                if last_msg_id == 0 or last_msg_id != x.id:
                                    if x.date.replace(tzinfo=None) >= LAST_RUN_DATE:
                                        filtered_msg.append([x.id, datetime.strftime(
                                            x.date, '%m-%d-%Y %H:%M:%S'), format_msg(x.text)])
                                        last_msg_id = x.id

    LAST_RUN_DATE = datetime.utcnow()
    for fm in filtered_msg:
        print(fm)

    print(len(filtered_msg))


while True:
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        sleep(60)
        print('RUN AGAIN')
    except Exception as e:
        print(str(e))
