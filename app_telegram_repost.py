import spacy
import asyncio
from fs import read_json
from spacy.lang.ru import Russian
from spacy.matcher import PhraseMatcher
from telethon import TelegramClient, sync, events


CONFIG = read_json('config/config.json')
CHANNELS = read_json('config/channels.json')['channels']
PHRASES_CONFIG = read_json('config/phrases.json')
GLOBAL_PHRASES = PHRASES_CONFIG['global_phrases']

CHANNEL_1_ENABLED_FILTERING = CONFIG['channel_1_enabled_filtering'].lower()
CHANNEL_2_ENABLED_FILTERING = CONFIG['channel_2_enabled_filtering'].lower()
CHANNEL_3_ENABLED_FILTERING = CONFIG['channel_3_enabled_filtering'].lower()
CHANNEL_4_ENABLED_FILTERING = CONFIG['channel_4_enabled_filtering'].lower()
CHANNEL_5_ENABLED_FILTERING = CONFIG['channel_5_enabled_filtering'].lower()

CHANNEL_1_ENABLED = CONFIG['channel_1_ebabled'].lower()
CHANNEL_2_ENABLED = CONFIG['channel_2_ebabled'].lower()
CHANNEL_3_ENABLED = CONFIG['channel_3_ebabled'].lower()
CHANNEL_4_ENABLED = CONFIG['channel_4_ebabled'].lower()
CHANNEL_5_ENABLED = CONFIG['channel_5_ebabled'].lower()

CHANNEL_CHAT_ID_1 = CONFIG['chat_id_1']
CHANNEL_CHAT_ID_2 = CONFIG['chat_id_2']
CHANNEL_CHAT_ID_3 = CONFIG['chat_id_3']
CHANNEL_CHAT_ID_4 = CONFIG['chat_id_4']
CHANNEL_CHAT_ID_5 = CONFIG['chat_id_5']

PHRASES_1 = PHRASES_CONFIG['phrases_1']
PHRASES_2 = PHRASES_CONFIG['phrases_2']
PHRASES_3 = PHRASES_CONFIG['phrases_3']
PHRASES_4 = PHRASES_CONFIG['phrases_4']
PHRASES_5 = PHRASES_CONFIG['phrases_5']

PHRASES_EXCLUDED_1 = PHRASES_CONFIG['excluded_1']
PHRASES_EXCLUDED_2 = PHRASES_CONFIG['excluded_2']
PHRASES_EXCLUDED_3 = PHRASES_CONFIG['excluded_3']
PHRASES_EXCLUDED_4 = PHRASES_CONFIG['excluded_4']
PHRASES_EXCLUDED_5 = PHRASES_CONFIG['excluded_5']


client = TelegramClient('my_session', CONFIG['app_id'], CONFIG['app_hash'])
client.start()

nlp = Russian()

# Phrase matchers (include)
if len(GLOBAL_PHRASES) > 0:
    global_phrase_matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
    global_patterns = [nlp(text_global) for text_global in GLOBAL_PHRASES]
    global_phrase_matcher.add('AI_INC_G', None, *global_patterns)

if len(PHRASES_1) > 0:
    phrase_matcher_1 = PhraseMatcher(nlp.vocab, attr='LOWER')
    patterns_1 = [nlp(text_phase_1) for text_phase_1 in PHRASES_1]
    phrase_matcher_1.add('AI_INC_1', None, *patterns_1)

if len(PHRASES_2) > 0:
    phrase_matcher_2 = PhraseMatcher(nlp.vocab, attr='LOWER')
    patterns_2 = [nlp(text_phase_2) for text_phase_2 in PHRASES_2]
    phrase_matcher_2.add('AI_INC_2', None, *patterns_2)

if len(PHRASES_3) > 0:
    phrase_matcher_3 = PhraseMatcher(nlp.vocab, attr='LOWER')
    patterns_3 = [nlp(text_phase_3) for text_phase_3 in PHRASES_3]
    phrase_matcher_3.add('AI_INC_3', None, *patterns_3)

if len(PHRASES_4) > 0:
    phrase_matcher_4 = PhraseMatcher(nlp.vocab, attr='LOWER')
    patterns_4 = [nlp(text_phase_4) for text_phase_4 in PHRASES_4]
    phrase_matcher_4.add('AI_INC_4', None, *patterns_4)

if len(PHRASES_5) > 0:
    phrase_matcher_5 = PhraseMatcher(nlp.vocab, attr='LOWER')
    patterns_5 = [nlp(text_phase_5) for text_phase_5 in PHRASES_5]
    phrase_matcher_5.add('AI_INC_5', None, *patterns_5)


# Phrase matchers (exclude)
if CHANNEL_1_ENABLED_FILTERING == 'yes':
    if len(PHRASES_EXCLUDED_1) > 0:
        exclude_patterns_1 = [nlp(exclude_phase_1)
                              for exclude_phase_1 in PHRASES_EXCLUDED_1]
        exclude_phrase_matcher_1 = PhraseMatcher(nlp.vocab, attr='LOWER')
        exclude_phrase_matcher_1.add('AI_EX_1', None, *exclude_patterns_1)

if CHANNEL_2_ENABLED_FILTERING == 'yes':
    if len(PHRASES_EXCLUDED_2) > 0:
        exclude_patterns_2 = [nlp(exclude_phase_2)
                              for exclude_phase_2 in PHRASES_EXCLUDED_2]
        exclude_phrase_matcher_2 = PhraseMatcher(nlp.vocab, attr='LOWER')
        exclude_phrase_matcher_2.add('AI_EX_2', None, *exclude_patterns_2)

if CHANNEL_3_ENABLED_FILTERING == 'yes':
    if len(PHRASES_EXCLUDED_3) > 0:
        exclude_patterns_3 = [nlp(exclude_phase_3)
                              for exclude_phase_3 in PHRASES_EXCLUDED_3]
        exclude_phrase_matcher_3 = PhraseMatcher(nlp.vocab, attr='LOWER')
        exclude_phrase_matcher_3.add('AI_EX_3', None, *exclude_patterns_3)

if CHANNEL_4_ENABLED_FILTERING == 'yes':
    if len(PHRASES_EXCLUDED_4) > 0:
        exclude_patterns_4 = [nlp(exclude_phase_4)
                              for exclude_phase_4 in PHRASES_EXCLUDED_4]
        exclude_phrase_matcher_4 = PhraseMatcher(nlp.vocab, attr='LOWER')
        exclude_phrase_matcher_4.add('AI_EX_4', None, *exclude_patterns_4)

if CHANNEL_5_ENABLED_FILTERING == 'yes':
    if len(PHRASES_EXCLUDED_5) > 0:
        exclude_patterns_5 = [nlp(exclude_phase_5)
                              for exclude_phase_5 in PHRASES_EXCLUDED_5]
        exclude_phrase_matcher_5 = PhraseMatcher(nlp.vocab, attr='LOWER')
        exclude_phrase_matcher_5.add('AI_EX_5', None, *exclude_patterns_5)


@client.on(events.NewMessage(chats=CHANNELS))
async def new_start(event):
    # 1 channel
    if CHANNEL_1_ENABLED == 'yes':
        if CHANNEL_1_ENABLED_FILTERING == 'yes':
            sentence_1 = nlp(event.message.text)
            global_matched_phrases_1 = global_phrase_matcher(sentence_1)
            if len(global_matched_phrases_1) > 0:
                if len(PHRASES_1) > 0:
                    matched_phrases_1 = phrase_matcher_1(sentence_1)
                    if len(matched_phrases_1) > 0:
                        if len(PHRASES_EXCLUDED_1) > 0:
                            exclude_matched_phrases_1 = exclude_phrase_matcher_1(
                                sentence_1)
                            if len(exclude_matched_phrases_1) == 0:
                                await client.forward_messages(CHANNEL_CHAT_ID_1, event.message)
                        if len(PHRASES_EXCLUDED_1) == 0:
                            await client.forward_messages(CHANNEL_CHAT_ID_1, event.message)
                if len(PHRASES_1) == 0:
                    if len(PHRASES_EXCLUDED_1) > 0:
                        exclude_matched_phrases_1 = exclude_phrase_matcher_1(
                            sentence_1)
                        if len(exclude_matched_phrases_1) == 0:
                            await client.forward_messages(CHANNEL_CHAT_ID_1, event.message)
                    if len(PHRASES_EXCLUDED_1) == 0:
                        await client.forward_messages(CHANNEL_CHAT_ID_1, event.message)
        else:
            await client.forward_messages(CHANNEL_CHAT_ID_1, event.message)

    # 2 channel
    if CHANNEL_2_ENABLED == 'yes':
        if CHANNEL_2_ENABLED_FILTERING == 'yes':
            sentence_2 = nlp(event.message.text)
            global_matched_phrases_2 = global_phrase_matcher(sentence_2)
            if len(global_matched_phrases_2) > 0:
                if len(PHRASES_2) > 0:
                    matched_phrases_2 = phrase_matcher_2(sentence_2)
                    if len(matched_phrases_2) > 0:
                        if len(PHRASES_EXCLUDED_2) > 0:
                            exclude_matched_phrases_2 = exclude_phrase_matcher_2(
                                sentence_2)
                            if len(exclude_matched_phrases_2) == 0:
                                await client.forward_messages(CHANNEL_CHAT_ID_2, event.message)
                        if len(PHRASES_EXCLUDED_2) == 0:
                            await client.forward_messages(CHANNEL_CHAT_ID_2, event.message)
                if len(PHRASES_2) == 0:
                    if len(PHRASES_EXCLUDED_2) > 0:
                        exclude_matched_phrases_2 = exclude_phrase_matcher_2(
                            sentence_2)
                        if len(exclude_matched_phrases_2) == 0:
                            await client.forward_messages(CHANNEL_CHAT_ID_2, event.message)
                    if len(PHRASES_EXCLUDED_2) == 0:
                        await client.forward_messages(CHANNEL_CHAT_ID_2, event.message)
        else:
            await client.forward_messages(CHANNEL_CHAT_ID_2, event.message)

    # 3 channel
    if CHANNEL_3_ENABLED == 'yes':
        if CHANNEL_3_ENABLED_FILTERING == 'yes':
            sentence_3 = nlp(event.message.text)
            global_matched_phrases_3 = global_phrase_matcher(sentence_3)
            if len(global_matched_phrases_3) > 0:
                if len(PHRASES_3) > 0:
                    matched_phrases_3 = phrase_matcher_3(sentence_3)
                    if len(matched_phrases_3) > 0:
                        if len(PHRASES_EXCLUDED_3) > 0:
                            exclude_matched_phrases_3 = exclude_phrase_matcher_3(
                                sentence_3)
                            if len(exclude_matched_phrases_3) == 0:
                                await client.forward_messages(CHANNEL_CHAT_ID_3, event.message)
                        if len(PHRASES_EXCLUDED_3) == 0:
                            await client.forward_messages(CHANNEL_CHAT_ID_3, event.message)
                if len(PHRASES_3) == 0:
                    if len(PHRASES_EXCLUDED_3) > 0:
                        exclude_matched_phrases_3 = exclude_phrase_matcher_3(
                            sentence_3)
                        if len(exclude_matched_phrases_3) == 0:
                            await client.forward_messages(CHANNEL_CHAT_ID_3, event.message)
                    if len(PHRASES_EXCLUDED_3) == 0:
                        await client.forward_messages(CHANNEL_CHAT_ID_3, event.message)
        else:
            await client.forward_messages(CHANNEL_CHAT_ID_3, event.message)

    # 4 channel
    if CHANNEL_4_ENABLED == 'yes':
        if CHANNEL_4_ENABLED_FILTERING == 'yes':
            sentence_4 = nlp(event.message.text)
            global_matched_phrases_4 = global_phrase_matcher(sentence_4)
            if len(global_matched_phrases_4) > 0:
                if len(PHRASES_4) > 0:
                    matched_phrases_4 = phrase_matcher_4(sentence_4)
                    if len(matched_phrases_4) > 0:
                        if len(PHRASES_EXCLUDED_4) > 0:
                            exclude_matched_phrases_4 = exclude_phrase_matcher_4(
                                sentence_4)
                            if len(exclude_matched_phrases_4) == 0:
                                await client.forward_messages(CHANNEL_CHAT_ID_4, event.message)
                        if len(PHRASES_EXCLUDED_4) == 0:
                            await client.forward_messages(CHANNEL_CHAT_ID_4, event.message)
                if len(PHRASES_4) == 0:
                    if len(PHRASES_EXCLUDED_4) > 0:
                        exclude_matched_phrases_4 = exclude_phrase_matcher_4(
                            sentence_4)
                        if len(exclude_matched_phrases_4) == 0:
                            await client.forward_messages(CHANNEL_CHAT_ID_4, event.message)
                    if len(PHRASES_EXCLUDED_4) == 0:
                        await client.forward_messages(CHANNEL_CHAT_ID_4, event.message)
        else:
            await client.forward_messages(CHANNEL_CHAT_ID_4, event.message)

    # 5 channel
    if CHANNEL_5_ENABLED == 'yes':
        if CHANNEL_5_ENABLED_FILTERING == 'yes':
            sentence_5 = nlp(event.message.text)
            global_matched_phrases_5 = global_phrase_matcher(sentence_5)
            if len(global_matched_phrases_5) > 0:
                if len(PHRASES_5) > 0:
                    matched_phrases_5 = phrase_matcher_5(sentence_5)
                    if len(matched_phrases_5) > 0:
                        if len(PHRASES_EXCLUDED_5) > 0:
                            exclude_matched_phrases_5 = exclude_phrase_matcher_5(
                                sentence_5)
                            if len(exclude_matched_phrases_5) == 0:
                                await client.forward_messages(CHANNEL_CHAT_ID_5, event.message)
                        if len(PHRASES_EXCLUDED_5) == 0:
                            await client.forward_messages(CHANNEL_CHAT_ID_5, event.message)
                if len(PHRASES_5) == 0:
                    if len(PHRASES_EXCLUDED_5) > 0:
                        exclude_matched_phrases_5 = exclude_phrase_matcher_5(
                            sentence_5)
                        if len(exclude_matched_phrases_5) == 0:
                            await client.forward_messages(CHANNEL_CHAT_ID_5, event.message)
                    if len(PHRASES_EXCLUDED_5) == 0:
                        await client.forward_messages(CHANNEL_CHAT_ID_5, event.message)
        else:
            await client.forward_messages(CHANNEL_CHAT_ID_5, event.message)


if __name__ == "__main__":
    client.run_until_disconnected()
