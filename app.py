import re
import asyncio
from time import sleep
from fs import read_json
from datetime import datetime
from telethon import TelegramClient
from telethon.tl import functions, types


CONFIG = read_json('config/config.json')
ENABLED_FILTERING = CONFIG['enabled_filtering'].lower()
CHANNEL_1_ENABLED = CONFIG['channel_1_ebabled'].lower()
CHANNEL_2_ENABLED = CONFIG['channel_2_ebabled'].lower()
CHANNEL_CHAT_ID = CONFIG['chat_id']
CHANNEL_CHAT_ID_2 = CONFIG['chat_id_2']
SLEEP_TIMEOUT = CONFIG['sleep_timeout_seconds']
CHANNELS = read_json('config/channels.json')['channels']
WORDS_CONFIG = read_json('config/words.json')
GLOBAL_WORDS = WORDS_CONFIG['global_words']
WORDS = WORDS_CONFIG['words']
WORDS_EXCLUDED = WORDS_CONFIG['excluded']
WORDS_2 = WORDS_CONFIG['words_2']
WORDS_EXCLUDED_2 = WORDS_CONFIG['excluded_2']

FIRST_RUN = True
LAST_RUN_DATE = None


client = TelegramClient('my_session', CONFIG['app_id'], CONFIG['app_hash'])
client.start()


async def main():
    global FIRST_RUN
    global LAST_RUN_DATE

    if LAST_RUN_DATE is None:
        LAST_RUN_DATE = datetime.utcnow()

    if ENABLED_FILTERING == 'yes':
        global_pattern = re.compile('|'.join(GLOBAL_WORDS), re.IGNORECASE)

        if CHANNEL_1_ENABLED == 'yes':
            include_pattern = re.compile('|'.join(WORDS), re.IGNORECASE)
            if len(WORDS_EXCLUDED) != 0:
                exclude_pattern = re.compile(
                    '|'.join(WORDS_EXCLUDED), re.IGNORECASE)

        if CHANNEL_1_ENABLED == 'yes':
            include_pattern_2 = re.compile('|'.join(WORDS_2), re.IGNORECASE)
            if len(WORDS_EXCLUDED_2) != 0:
                exclude_pattern_2 = re.compile(
                    '|'.join(WORDS_EXCLUDED_2), re.IGNORECASE)

    for c in CHANNELS:
        await asyncio.sleep(5)
        messages = await client.get_messages(c, limit=20)

        if len(messages) > 0:
            for message in messages:
                if type(message.text) == str:
                    sleep(1)
                    # First channel
                    if CHANNEL_1_ENABLED == 'yes':
                        if ENABLED_FILTERING == 'yes':
                            if bool(include_pattern.search(message.text)) and bool(global_pattern.search(message.text)):
                                if len(WORDS_EXCLUDED) != 0:
                                    if not bool(exclude_pattern.search(message.text)):
                                        if message.date.replace(tzinfo=None) >= LAST_RUN_DATE or FIRST_RUN:
                                            await client.forward_messages(CHANNEL_CHAT_ID, message, c)
                                if len(WORDS_EXCLUDED) == 0:
                                    if message.date.replace(tzinfo=None) >= LAST_RUN_DATE or FIRST_RUN:
                                        await client.forward_messages(CHANNEL_CHAT_ID, message, c)
                        else:
                            if message.date.replace(tzinfo=None) >= LAST_RUN_DATE or FIRST_RUN:
                                await client.forward_messages(CHANNEL_CHAT_ID, message, c)

                    # second channel
                    if CHANNEL_2_ENABLED == 'yes':
                        if ENABLED_FILTERING == 'yes':
                            if bool(include_pattern_2.search(message.text)) and bool(global_pattern.search(message.text)):
                                if len(WORDS_EXCLUDED_2) != 0:
                                    if not bool(exclude_pattern_2.search(message.text)):
                                        if message.date.replace(tzinfo=None) >= LAST_RUN_DATE or FIRST_RUN:
                                            await client.forward_messages(CHANNEL_CHAT_ID_2, message, c)
                                if len(WORDS_EXCLUDED_2) == 0:
                                    if message.date.replace(tzinfo=None) >= LAST_RUN_DATE or FIRST_RUN:
                                        await client.forward_messages(CHANNEL_CHAT_ID_2, message, c)
                        else:
                            if message.date.replace(tzinfo=None) >= LAST_RUN_DATE or FIRST_RUN:
                                await client.forward_messages(CHANNEL_CHAT_ID, message, c)
    FIRST_RUN = False
    LAST_RUN_DATE = datetime.utcnow()


def start():
    while True:
        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
            sleep(SLEEP_TIMEOUT)
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    start()
