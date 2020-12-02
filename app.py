import re
import asyncio
from time import sleep
from fs import read_json
from datetime import datetime
from telethon import TelegramClient
from telethon.tl import functions, types

CONFIG = read_json('config/config.json')


CHANNEL_CHAT_ID = CONFIG['chat_id']
CHANNEL_CHAT_ID_2 = CONFIG['chat_id_2']

CHANNELS = read_json('config/channels.json')['channels']

WORDS_CONFIG = read_json('config/words.json')

GLOBAL_WORDS = WORDS_CONFIG['global_words']

WORDS = WORDS_CONFIG['words']
WORDS_EXCLUDED = WORDS_CONFIG['excluded']

WORDS_2 = WORDS_CONFIG['words_2']
WORDS_EXCLUDED_2 = WORDS_CONFIG['excluded_2']

LAST_RUN_DATE = None
IS_FIRST_RUN = True

client = TelegramClient('my_session', CONFIG['app_id'], CONFIG['app_hash'])
client.start()


async def main():
    global LAST_RUN_DATE
    global IS_FIRST_RUN

    if LAST_RUN_DATE is None:
        LAST_RUN_DATE = datetime.utcnow()

    global_pattern = re.compile('|'.join(GLOBAL_WORDS), re.IGNORECASE)

    include_pattern = re.compile('|'.join(WORDS), re.IGNORECASE)
    if len(WORDS_EXCLUDED) != 0:
        exclude_pattern = re.compile('|'.join(WORDS_EXCLUDED), re.IGNORECASE)

    include_pattern_2 = re.compile('|'.join(WORDS_2), re.IGNORECASE)
    if len(WORDS_EXCLUDED_2) != 0:
        exclude_pattern_2 = re.compile(
            '|'.join(WORDS_EXCLUDED_2), re.IGNORECASE)

    for c in CHANNELS:
        await asyncio.sleep(3)
        messages = await client.get_messages(c, limit=10)
        last_msg_id = 0
        last_msg_id_2 = 0

        if len(messages) > 0:
            for message in messages:
                if type(message.text) == str:
                    # First channel
                    if bool(include_pattern.search(message.text)) and bool(global_pattern.search(message.text)):
                        if len(WORDS_EXCLUDED) != 0:
                            if not bool(exclude_pattern.search(message.text)):
                                if last_msg_id == 0 or last_msg_id != message.id:
                                    if message.date.replace(tzinfo=None) >= LAST_RUN_DATE or IS_FIRST_RUN:
                                        await client.forward_messages(CHANNEL_CHAT_ID, message, c)
                        if len(WORDS_EXCLUDED) == 0:
                            if last_msg_id == 0 or last_msg_id != message.id:
                                if message.date.replace(tzinfo=None) >= LAST_RUN_DATE or IS_FIRST_RUN:
                                    await client.forward_messages(CHANNEL_CHAT_ID, message, c)

                    # second channel
                    if bool(include_pattern_2.search(message.text)) and bool(global_pattern.search(message.text)):
                        if len(WORDS_EXCLUDED_2) != 0:
                            if not bool(exclude_pattern_2.search(message.text)):
                                if last_msg_id_2 == 0 or last_msg_id_2 != message.id:
                                    if message.date.replace(tzinfo=None) >= LAST_RUN_DATE or IS_FIRST_RUN:
                                        await client.forward_messages(CHANNEL_CHAT_ID_2, message, c)
                        if len(WORDS_EXCLUDED_2) == 0:
                            if last_msg_id_2 == 0 or last_msg_id_2 != message.id:
                                if message.date.replace(tzinfo=None) >= LAST_RUN_DATE or IS_FIRST_RUN:
                                    await client.forward_messages(CHANNEL_CHAT_ID_2, message, c)

    LAST_RUN_DATE = datetime.utcnow()
    IS_FIRST_RUN = False


def start():
    while True:
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
            sleep(10)
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    start()
