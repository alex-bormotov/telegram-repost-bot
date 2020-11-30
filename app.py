import re
import asyncio
from time import sleep
from fs import read_json
from datetime import datetime
from telethon import TelegramClient
from telethon.tl import functions, types
from send_to_telegram_api import telegram_send_message

CONFIG = read_json('config/config.json')
BOT_API = CONFIG['bot_api_key']
CHANNEL_CHAT_ID = CONFIG['chat_id']
CHANNELS = read_json('config/channels.json')['channels']
WORDS = read_json('config/search_words.json')['words']
WORDS_EXCLUDED = read_json('config/excluded_words.json')['excluded']

LAST_RUN_DATE = None
IS_FIRST_RUN = True

client = TelegramClient('my_session', CONFIG['app_id'], CONFIG['app_hash'])
client.start()

CHANNELS_ENTITY = []


async def main():
    global LAST_RUN_DATE
    global CHANNELS_ENTITY
    global IS_FIRST_RUN

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

    if len(CHANNELS_ENTITY) == 0:
        for ch in CHANNELS:
            channel = await client.get_entity(f'@{ch}')
            CHANNELS_ENTITY.append(channel)
            await asyncio.sleep(5)

    for c in CHANNELS_ENTITY:
        await asyncio.sleep(5)
        messages = await client.get_messages(c, limit=1)
        last_msg_id = 0
        if len(messages) > 0:
            for x in messages:
                if x.text is not None:
                    for w in WORDS:
                        if len(WORDS_EXCLUDED) > 0:
                            for ex_w in WORDS_EXCLUDED:
                                if w in x.message and ex_w not in x.message:
                                    if last_msg_id == 0 or last_msg_id != x.id:
                                        if x.date.replace(tzinfo=None) >= LAST_RUN_DATE or IS_FIRST_RUN:
                                            filtered_msg.append(format_msg(x.text))
                                            last_msg_id = x.id
                        else:
                            if w in x.message:
                                if last_msg_id == 0 or last_msg_id != x.id:
                                    if x.date.replace(tzinfo=None) >= LAST_RUN_DATE or IS_FIRST_RUN:
                                        filtered_msg.append(format_msg(x.text))
                                        last_msg_id = x.id

    LAST_RUN_DATE = datetime.utcnow()
    IS_FIRST_RUN = False
    for fm in filtered_msg:
        telegram_send_message(BOT_API, CHANNEL_CHAT_ID, fm)


def start():
    while True:
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
            sleep(600)
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    start()
