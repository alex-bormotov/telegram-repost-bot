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
WORDS_CONFIG = read_json('config/words.json')

CHANNEL_1_ENABLED_FILTERING = CONFIG['channel_1_enabled_filtering'].lower()
CHANNEL_CHAT_ID_1 = CONFIG['chat_id_1']

WORDS_1 = WORDS_CONFIG['words_1']
WORDS_2 = WORDS_CONFIG['words_2']
WORDS_2_1 = WORDS_CONFIG['words_2_1']


client = TelegramClient('my_session', CONFIG['app_id'], CONFIG['app_hash'])
client.start()

nlp = Russian()


matcher_1 = PhraseMatcher(nlp.vocab, attr='LOWER')
matcher_1.add('AI_INC_1', None, *[nlp(text_phase_1)
                                  for text_phase_1 in WORDS_1])

matcher_2 = PhraseMatcher(nlp.vocab, attr='LOWER')
matcher_2.add('AI_INC_2', None, *[nlp(text_phase_2)
                                  for text_phase_2 in WORDS_2])

matcher_2_1 = PhraseMatcher(nlp.vocab, attr='LOWER')
matcher_2_1.add('AI_INC_2_1', None, *
                [nlp(text_phase_2_1) for text_phase_2_1 in WORDS_2_1])


@client.on(events.NewMessage(chats=CHANNELS))
async def new_start(event):
    try:
        # print(event.message.text)

        if CHANNEL_1_ENABLED_FILTERING == 'yes':

            sentence_1 = nlp(event.message.text)

            matched_1 = matcher_1(sentence_1)
            matched_2 = matcher_2(sentence_1)
            matched_2_1 = matcher_2_1(sentence_1)

            condition_1 = len(matched_1) != 0
            condition_2 = len(matched_2) != 0 and len(matched_2_1) != 0

            print(len(matched_1), len(matched_2), len(matched_2_1))
            print(condition_1, condition_2)

            if condition_1 or condition_2:

                print(event.message.text)

                await client.forward_messages(CHANNEL_CHAT_ID_1, event.message)

        else:
            await client.forward_messages(CHANNEL_CHAT_ID_1, event.message)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    client.run_until_disconnected()
