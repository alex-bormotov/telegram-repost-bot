import re
import spacy
import asyncio
from time import sleep
from fs import read_json
from datetime import datetime
from spacy.lang.ru import Russian
from telethon import TelegramClient
from spacy.matcher import PhraseMatcher
from telethon.tl import functions, types


CONFIG = read_json('config/config.json')
ENABLED_FILTERING = CONFIG['enabled_filtering'].lower()

CHANNEL_1_ENABLED = CONFIG['channel_1_ebabled'].lower()
CHANNEL_2_ENABLED = CONFIG['channel_2_ebabled'].lower()

CHANNEL_CHAT_ID = CONFIG['chat_id']
CHANNEL_CHAT_ID_2 = CONFIG['chat_id_2']

SLEEP_TIMEOUT = CONFIG['sleep_timeout_seconds']

CHANNELS = read_json('config/channels.json')['channels']

PHRASES_CONFIG = read_json('config/phrases.json')

GLOBAL_PHRASES = PHRASES_CONFIG['global_phrases']

PHRASES = PHRASES_CONFIG['phrases']
PHRASES_EXCLUDED = PHRASES_CONFIG['excluded']

PHRASES_2 = PHRASES_CONFIG['phrases_2']
PHRASES_EXCLUDED_2 = PHRASES_CONFIG['excluded_2']

# FIRST_RUN = True # If True the Bot will posts a few "initial messages"
FIRST_RUN = False  # If False you will able to restart the bot "smoothly"
LAST_RUN_DATE = None


client = TelegramClient('my_session', CONFIG['app_id'], CONFIG['app_hash'])
client.start()


nlp = Russian()
phrase_matcher = PhraseMatcher(nlp.vocab, attr='LOWER')

phrases = GLOBAL_PHRASES

patterns = [nlp(text) for text in phrases]
phrase_matcher.add('AI', None, *patterns)


async def main():
    global FIRST_RUN
    global LAST_RUN_DATE

    if LAST_RUN_DATE is None:
        LAST_RUN_DATE = datetime.utcnow()

    for c in CHANNELS:
        await asyncio.sleep(5)
        messages = await client.get_messages(c, limit=100)

        if len(messages) > 0:
            for message in messages:
                if type(message.text) == str:
                    sleep(1)
                    # First channel
                    if CHANNEL_1_ENABLED == 'yes':
                        if ENABLED_FILTERING == 'yes':
                            sentence = nlp(message.text)
                            matched_phrases = phrase_matcher(sentence)
                            if len(matched_phrases) > 0:
                                if message.date.replace(tzinfo=None) >= LAST_RUN_DATE or FIRST_RUN:
                                    await client.forward_messages(CHANNEL_CHAT_ID, message, c)
                        else:
                            if message.date.replace(tzinfo=None) >= LAST_RUN_DATE or FIRST_RUN:
                                await client.forward_messages(CHANNEL_CHAT_ID, message, c)

                    # second channel
                    # if CHANNEL_2_ENABLED == 'yes':
                    #     if ENABLED_FILTERING == 'yes':
                    #         if bool(include_pattern_2.search(message.text)) and bool(global_pattern.search(message.text)):
                    #             if len(WORDS_EXCLUDED_2) != 0:
                    #                 if not bool(exclude_pattern_2.search(message.text)):
                    #                     if message.date.replace(tzinfo=None) >= LAST_RUN_DATE or FIRST_RUN:
                    #                         await client.forward_messages(CHANNEL_CHAT_ID_2, message, c)
                    #             if len(WORDS_EXCLUDED_2) == 0:
                    #                 if message.date.replace(tzinfo=None) >= LAST_RUN_DATE or FIRST_RUN:
                    #                     await client.forward_messages(CHANNEL_CHAT_ID_2, message, c)
                    #     else:
                    #         if message.date.replace(tzinfo=None) >= LAST_RUN_DATE or FIRST_RUN:
                    #             await client.forward_messages(CHANNEL_CHAT_ID, message, c)
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