# -*- coding: utf-8 -*-

from fs import read_json

from pprint import pprint
from datetime import datetime

import asyncio
from telethon import TelegramClient
from telethon.tl import functions, types

CONFIG = read_json('config/config.json')

client = TelegramClient('my_session', CONFIG['app_id'], CONFIG['app_hash'])
client.start()

words = read_json('config/search_words.json')['words']


async def main():
    CHANNELS = read_json('config/channels.json')['channels']

    filtered_msg = []

    for c in CHANNELS:
        await asyncio.sleep(1)
        channel = await client.get_entity(f'@{c}')
        messages = await client.get_messages(channel, limit=1)

        last_msg_id = 0

        if len(messages) > 0:
            for x in messages:
                if x.text is not None:
                    for w in words:
                        if w in x.message:
                            if last_msg_id == 0 or last_msg_id != x.id:
                                filtered_msg.append([x.id, datetime.strftime(
                                    x.date, '%m-%d-%Y %H:%M:%S'), x.text])
                                last_msg_id = x.id

    for fm in filtered_msg:
        print(fm)

    print(len(filtered_msg))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
