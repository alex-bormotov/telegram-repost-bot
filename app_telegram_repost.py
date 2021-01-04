import re
import spacy
import asyncio
from time import sleep
from fs import read_json
from datetime import datetime
from spacy.lang.ru import Russian
from spacy.matcher import PhraseMatcher
from telethon.tl import functions, types
from telethon import TelegramClient, sync, events


CONFIG = read_json('config/config.json')
ENABLED_FILTERING = CONFIG['enabled_filtering'].lower()

CHANNEL_1_ENABLED = CONFIG['channel_1_ebabled'].lower()
CHANNEL_2_ENABLED = CONFIG['channel_2_ebabled'].lower()

CHANNEL_CHAT_ID = CONFIG['chat_id']
CHANNEL_CHAT_ID_2 = CONFIG['chat_id_2']

CHANNELS = read_json('config/channels.json')['channels']

PHRASES_CONFIG = read_json('config/phrases.json')

GLOBAL_PHRASES = PHRASES_CONFIG['global_phrases']

PHRASES = PHRASES_CONFIG['phrases']
PHRASES_EXCLUDED = PHRASES_CONFIG['excluded']

PHRASES_2 = PHRASES_CONFIG['phrases_2']
PHRASES_EXCLUDED_2 = PHRASES_CONFIG['excluded_2']


client = TelegramClient('my_session', CONFIG['app_id'], CONFIG['app_hash'])
client.start()

nlp = Russian()

if len(GLOBAL_PHRASES) > 0:
    global_phrase_matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
    global_patterns = [nlp(text) for text in GLOBAL_PHRASES]
    global_phrase_matcher.add('AI_G', None, *global_patterns)


if len(PHRASES) > 0:
    phrase_matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
    patterns = [nlp(text_p) for text_p in PHRASES]
    phrase_matcher.add('AI', None, *patterns)


if ENABLED_FILTERING == 'yes':
    # global_pattern = re.compile('|'.join(GLOBAL_WORDS), re.IGNORECASE)
    if CHANNEL_1_ENABLED == 'yes':
        # # include_pattern = re.compile('|'.join(WORDS), re.IGNORECASE)
        # if len(PHRASES_EXCLUDED) != 0:
        #     exclude_pattern = re.compile(
        #         '|'.join(PHRASES_EXCLUDED), re.IGNORECASE)
        if len(PHRASES_EXCLUDED) > 0:
            exclude_patterns = [nlp(text_2) for text_2 in PHRASES_EXCLUDED]
            exclude_phrase_matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
            exclude_phrase_matcher.add('AI_EX', None, *exclude_patterns)

        # if CHANNEL_1_ENABLED == 'yes':
        #     include_pattern_2 = re.compile('|'.join(WORDS_2), re.IGNORECASE)
        #     if len(WORDS_EXCLUDED_2) != 0:
        #         exclude_pattern_2 = re.compile(
        #             '|'.join(WORDS_EXCLUDED_2), re.IGNORECASE)


@client.on(events.NewMessage(chats=CHANNELS))
async def new_start(event):
    # First channel
    if CHANNEL_1_ENABLED == 'yes':
        if ENABLED_FILTERING == 'yes':
            sentence = nlp(event.message.text)
            global_matched_phrases = global_phrase_matcher(
                sentence)
            if len(global_matched_phrases) > 0:
                if len(PHRASES) > 0:
                    matched_phrases = phrase_matcher(sentence)
                    if len(matched_phrases) > 0:
                        if len(PHRASES_EXCLUDED) > 0:
                            exclude_matched_phrases = exclude_phrase_matcher(
                                sentence)
                            if len(exclude_matched_phrases) == 0:
                                await client.forward_messages(CHANNEL_CHAT_ID, event.message)

                        if len(PHRASES_EXCLUDED) == 0:
                            await client.forward_messages(CHANNEL_CHAT_ID, event.message)

                if len(PHRASES) == 0:
                    if len(PHRASES_EXCLUDED) > 0:
                        exclude_matched_phrases = exclude_phrase_matcher(
                            sentence)
                        if len(exclude_matched_phrases) == 0:
                            await client.forward_messages(CHANNEL_CHAT_ID, event.message)
                    if len(PHRASES_EXCLUDED) == 0:
                        await client.forward_messages(CHANNEL_CHAT_ID, event.message)

        else:
            await client.forward_messages(CHANNEL_CHAT_ID, event.message)


if __name__ == "__main__":
    client.run_until_disconnected()
