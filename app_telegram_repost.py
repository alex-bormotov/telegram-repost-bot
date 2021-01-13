import spacy
import asyncio
from fs import read_json
from spacy.lang.ru import Russian
from spacy.matcher import PhraseMatcher
from telethon import TelegramClient, sync, events


# @Postingjobot
# 1464258088:AAHGulWTXf4fekw-Jj39Qt9HOfYCTk-EKc0


CONFIG = read_json('config/config.json')
CHANNELS = read_json('config/channels.json')['channels']
PHRASES_CONFIG = read_json('config/phrases.json')

CHANNEL_1_ENABLED_FILTERING = CONFIG['channel_1_enabled_filtering'].lower()
CHANNEL_CHAT_ID_1 = CONFIG['chat_id_1']

CHANNEL_1_PHRASES_1 = PHRASES_CONFIG['channel_1_phrases_1']
CHANNEL_1_PHRASES_2 = PHRASES_CONFIG['channel_1_phrases_2']
CHANNEL_1_PHRASES_2_1 = PHRASES_CONFIG['channel_1_phrases_2_1']
CHANNEL_1_PHRASES_3 = PHRASES_CONFIG['channel_1_phrases_3']
CHANNEL_1_PHRASES_3_1 = PHRASES_CONFIG['channel_1_phrases_3_1']


client = TelegramClient('my_session', CONFIG['app_id'], CONFIG['app_hash'])
client.start()

nlp = Russian()


channel_1_phrase_matcher_1 = PhraseMatcher(nlp.vocab, attr='LOWER')
channel_1_patterns_1 = [nlp(text_phase_1)
                        for text_phase_1 in CHANNEL_1_PHRASES_1]
channel_1_phrase_matcher_1.add('AI_INC_1', None, *channel_1_patterns_1)


channel_1_phrase_matcher_2 = PhraseMatcher(nlp.vocab, attr='LOWER')
channel_1_patterns_2 = [nlp(text_phase_2)
                        for text_phase_2 in CHANNEL_1_PHRASES_2]
channel_1_phrase_matcher_2.add('AI_INC_2', None, *channel_1_patterns_2)


channel_1_phrase_matcher_2_1 = PhraseMatcher(nlp.vocab, attr='LOWER')
channel_1_patterns_2_1 = [nlp(text_phase_2_1)
                          for text_phase_2_1 in CHANNEL_1_PHRASES_2_1]
channel_1_phrase_matcher_2_1.add('AI_INC_2_1', None, *channel_1_patterns_2_1)


channel_1_phrase_matcher_3 = PhraseMatcher(nlp.vocab, attr='LOWER')
channel_1_patterns_3 = [nlp(text_phase_3)
                        for text_phase_3 in CHANNEL_1_PHRASES_3]
channel_1_phrase_matcher_3.add('AI_INC_4', None, *channel_1_patterns_3)


channel_1_phrase_matcher_3_1 = PhraseMatcher(nlp.vocab, attr='LOWER')
channel_1_patterns_3_1 = [nlp(text_phase_3_1)
                          for text_phase_3_1 in CHANNEL_1_PHRASES_3_1]
channel_1_phrase_matcher_3_1.add(
    'AI_INC_3_1', None, *channel_1_patterns_3_1)


@client.on(events.NewMessage(chats=CHANNELS))
async def new_start(event):

    if CHANNEL_1_ENABLED_FILTERING == 'yes':

        sentence_1 = nlp(event.message.text)

        matched_phrases_1 = channel_1_phrase_matcher_1(sentence_1)
        matched_phrases_2 = channel_1_phrase_matcher_2(sentence_1)
        matched_phrases_3 = channel_1_phrase_matcher_3(sentence_1)
        matched_phrases_4 = channel_1_phrase_matcher_4(sentence_1)
        matched_phrases_4_1 = channel_1_phrase_matcher_4_1(sentence_1)
        if len(matched_phrases_1) != 0:
            if (len(matched_phrases_2) != 0 and len(matched_phrases_3) != 0) or (len(matched_phrases_4) != 0 and len(matched_phrases_4_1) != 0):
                await client.forward_messages(CHANNEL_CHAT_ID_1, event.message)

    else:
        await client.forward_messages(CHANNEL_CHAT_ID_1, event.message)


if __name__ == "__main__":
    client.run_until_disconnected()
