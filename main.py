import csv
import random

import yaml
from telegram.ext import MessageHandler, filters, Application

import re
import logging


logging.basicConfig(
    format='%(asctime)s [%(levelname)s] - %(name)s - %(message)s',
    encoding='utf-8',
    level=logging.INFO)


def read_config():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)


replies = 0


async def process_full_message_triggers(update):
    text = update.message.text
    pattern_with_optional_punctuation = "{}([!?.,;:\"'])*$"
    with open('triggers_and_replies.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            trigger = row[0]
            pattern = pattern_with_optional_punctuation.format(trigger)
            if re.match(pattern, text, re.IGNORECASE):
                reply = row[1]
                global replies
                replies += 1
                await update.message.reply_text(text=reply, quote=True)


async def process_snippet_message_triggers(update):
    text = update.message.text
    with open('trigger_words.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            trigger = row[0]
            if re.search(trigger, text, re.IGNORECASE):
                reply = row[1]
                global replies
                replies += 1
                await update.message.reply_text(text=reply, quote=True)


async def reply_to_sanya(update):
    message = update.message
    sanya_pattern_eng = "(^Ale(x|ks)and(e?r$|ro)$)|(^San(dro|[yi]a|[yi]ok)$)|(^Sash(k?a|ok)$)|(^Shur(a|ic*k)$)"
    sanya_pattern_rus = "(^Александр$)|(^Саш[ау].*)|(^Сан(я([гр]а)*|[её]к)$)|(^Шур(а|ик)$)"
    message_sender_name = message.from_user.first_name
    if re.match(sanya_pattern_eng, message_sender_name, re.IGNORECASE) or re.match(sanya_pattern_rus, message_sender_name, re.IGNORECASE):
        await message.reply_voice("sanya.mp3", quote=True)


async def message_handler(update, context):
    global replies
    replies = 0
    await process_full_message_triggers(update)
    await process_snippet_message_triggers(update)
    if replies == 0 and random.randint(1, 4) == 1:
        await reply_to_sanya(update)


def main():
    config_map = read_config()
    api_token = config_map['telegram']['api-key']
    dp = Application.builder().token(api_token).build()
    dp.add_handler(MessageHandler(filters.TEXT, message_handler))
    dp.run_polling()


if __name__ == '__main__':
    main()
