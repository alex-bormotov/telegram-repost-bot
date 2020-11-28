import re
import asyncio
from fs import read_json
from datetime import datetime
from telethon import TelegramClient
from telethon.tl import functions, types

CONFIG = read_json('config/config.json')


client = TelegramClient('my_session', CONFIG['app_id'], CONFIG['app_hash'])
client.start()


CHANNELS = read_json('config/channels.json')['channels']
words = read_json('config/search_words.json')['words']
excluded_words = read_json('config/excluded_words.json')['excluded']


LAST_MESSAGE_DATE = None  # save it to json, for loading if bot restated
# import telegram func from snippet and use MARKDOWN format
# all messages example in jupyer notebook


async def main():
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
                                    filtered_msg.append([x.id, datetime.strftime(
                                        x.date, '%m-%d-%Y %H:%M:%S'), format_msg(x.text)])
                                    last_msg_id = x.id

    for fm in filtered_msg:
        print(fm)

    print(len(filtered_msg))


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
